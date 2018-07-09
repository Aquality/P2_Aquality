#==============================================================================================================
#=== Imports ===
#==============================================================================================================

import serial
import time
import json
import threading
import pymysql
from subprocess import call
import pdfkit
import asyncio
import websockets
import re
from operator import itemgetter, attrgetter


#==============================================================================================================
#=== Klassen ===
#==============================================================================================================

class Food:
    def __init__(self, name, count, water, startCount):
        self.name = name
        self.count = count
        self.water = water
        self.startCount = startCount

#==============================================================================================================
#=== Initialisierung ===
#==============================================================================================================

#=== Variables ===
productNameList = []
products = []
totalWater = 0
actualProduct= "nothing"
jsonString = ""
jsonData = []
locked = False
sendProductsArray = False
worseProducts = []

#=== SQL Connection ===
sqlConn = pymysql.connect(host='127.0.0.1',
                       user='python',password='pythonsql',
                       db='aquality_database')
cursor = sqlConn.cursor()

#=== Arduino Serial Connection ===
arduinoSerial = serial.Serial('/dev/ttyACM0', 9600, timeout=100)


#==============================================================================================================
#=== Threads ===
#==============================================================================================================



    #==============================================================================================================
    #=== Input Reader ===
    #==============================================================================================================

class InputReader(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):

        global arduinoSerial
        global productNameList
        global products
        global actualProduct
        global jsonString

        global jsonData

        global sendProductsArray

        global worseProducts

        while 1:

            #liest den arduino aus
            actualInput = arduinoSerial.readline()
            #überprüft, ob der Arduino etwas gesendet hat
            if len(actualInput) > 0:
                

                #verarbeitet den Input
                actualInput = actualInput[:-2]
                actualInput = actualInput.decode("utf-8")
                actualInput = str(actualInput)
                
                print(actualInput)

                #waehlt Eintrag aus der Datenbak aus

                sql = "SELECT * FROM `food` WHERE rfid=\'" + actualInput + "\'"
                cursor.execute(sql)

                data = cursor.fetchone()

                #verarbeitet den SQL Eintrag, und schreibt ihn in das Products-Array
                if data:
                    actualName = data[1]
                    if actualName not in productNameList:
                        productNameList.append(actualName)
                        products.append(Food(data[1], 0, data[6], data[7]))
                    
                    #Setzt das zuletzt eingescannte Produkt als actualProduct
                    actualProduct = actualName
                    
                    #berechnet totalWater
                    totalWater = 0
                    for product in products:
                        totalWater = totalWater + product.water * product.count

                #Ueberfuehrt das products array in ein JSON Objekt
                
                jsonData = []
                for product in products:
                    product.count = int(product.count)
                    jsonData.append(json.dumps(product.__dict__))
                
                jsonString = json.dumps(jsonData)


                #Gibt den Websocket den Befehl das Products Array zu übermitteln
                sendProductsArray = True
                print(products)



#==============================================================================================================
#=== Thread Controll ===
#==============================================================================================================

inputReaderThread = InputReader()

inputReaderThread.start()




#==============================================================================================================
#=== WebSocket ===
#==============================================================================================================

async def backendSocket(websocket, path):


    global actualProduct
    global jsonString
    global jsonData
    global locked
    global products

    global sendProductsArray

    global totalWater

    while True:

        if sendProductsArray == True:
            await websocket.send(jsonString)
            sendProductsArray = False
        
    
        value = await websocket.recv()

        #Teilt den empfangenen String an den Leerzeichen auf, und schreibt ihn in ein Array
        valueSplitted = value.split()
        
        if value == "unlockScann":
            locked = False


        elif value == "getActualProduct":
            await websocket.send(json.dumps(actualProduct))
        

        elif value == "resetBackendActualProduct":
            actualProduct = "nothing"


        elif value == "getTotalWater":
            await websocket.send(json.dumps(totalWater))


        elif value == "getProducts":
            await websocket.send(jsonString)


        elif valueSplitted[0] == "add":

            actualName = valueSplitted[1]
            actualCount = int(valueSplitted[2])

            if actualName not in productNameList:
                
                productNameList.append(actualName)

                sql = "SELECT * FROM `food` WHERE name=\'" + actualName + "\'"
                cursor.execute(sql)

                data = cursor.fetchone()

                #verarbeitet den SQL Eintrag, und schreibt ihn in das Products-Array
                if data:
                    products.append(Food(data[1], actualCount, data[6], data[7]))
            
            #erhoeht die Anzahl des jeweiligen Produkts um die angegebene Zahl

            else:
                for product in products:
                    if actualName == product.name:
                        product.count = product.count + actualCount
                print(products[0].count)
            
            #Ueberfuehrt das products array in ein JSON Objekt
            jsonData = []
            for product in products:
                product.count = int(product.count)
                jsonData.append(json.dumps(product.__dict__))
            
            jsonString = json.dumps(jsonData)

            #berechnet totalWater
            totalWater = 0
            for product in products:
                totalWater = totalWater + product.water * product.count

            await websocket.send(jsonString)
            await websocket.send(json.dumps(totalWater))



        elif valueSplitted[0] == "delete":

            actualName = valueSplitted[1]
            actualCount = int(valueSplitted[2])

            for product in list(products):
                if product.name == actualName:
                    product.count = product.count - actualCount


                
                    #Ueberfuehrt das products array in ein JSON Objekt

                    jsonData = []
                    for product in products:
                        product.count = int(product.count)
                        jsonData.append(json.dumps(product.__dict__))

                    #berechnet totalWater
                    totalWater = 0
                    for product in products:
                        totalWater = totalWater + product.water * product.count
                    
                    jsonString = json.dumps(jsonData)

                    await websocket.send(jsonString)
                    await websocket.send(json.dumps(totalWater))
        
        elif value == "printBill":

            #erstellt das html dokument

            preWorseProducts = sorted(products, key=lambda food: food.water, reverse=True)

            for product in preWorseProducts:
                if len(worseProducts) < 3:
                    worseProducts.append(product)

            with open('/home/pi/Desktop/prototype_v3/print_data/data.html', 'w+') as outfile:


#======================================================================================================
                outfile.write("""
<!DOCTYPE html>
<html lang=\"en\">

<head>
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <meta http-equiv=\"X-UA-Compatible\" content=\"ie=edge\">
    <title>AQUALITY</title>
    <meta charset=\"UTF-8\" />
    <style>
        * {
            padding: 0;
            margin: 0;
            font-family: arial, sans-serif;
        }

        .grid-container {
            grid-template-columns: 50vw 50vw;
            display: grid;
            align-content: center;
        }

        body {
            font-size: 12pt;
            width: 100%;
            padding: 0;
            height: 36cm;
        }

        table {
            border-collapse: collapse;
            width: 100%;
        }

        td {
            padding-left: 8px;
            padding-right: 8px;
        }

        .tableHeading {
            padding: 8px;
            border-bottom: 1px solid black;
        }

        p {
            font-size: 10pt;
        }

        #logo {
            width: 200px;
            padding-top: 5%;
            padding-bottom: 10%;
        }

        .center {
            text-align: center;
        }

        .productTable {
            margin: 0 auto;
            width: 80%;
            margin-bottom: 5%;
        }

        .right {
            text-align: right;
        }

        .icon {
            width: 8%;
        }

        .anzahl {
            text-align: left;
            width: 15%;
        }

        .produkt {
            text-align: left;
        }

        .liter {
            text-align: right;

        }

        .ergebnis {
            border-top: 1px solid black;
            padding-top: 3%;

        }

        .left {
            text-align: left;
            padding: 2%;
        }

        .footer {
            position: absolute;
            bottom: 3%;
            width: 100%;
        }

        .imgIcon {
            width: 65%
        }

        .tipp {
            width: 80%;
            margin:1% auto;
            display: grid;
            align-content: center;
            border: 1px solid black;
            height: auto;
            border-radius: 5px;
            grid-template-columns: auto auto;
        }

        .iconTipp {
            width: 30%;
            padding: 5%;
        }

        .iconTipp img {
            margin: 0 auto;
            width: 150px;
        }

        .textTipp {
            font-size: 12pt;
            padding: 4%;

        }
    </style>
</head>

<body>
    <div class=\"center\">
        <img src=\"logo/aquality_logo_sw.svg\" alt=\"\" id=\"logo\">
    </div>

    <div class=\"productTable\">
        <table>
                """)
                
                outfile.write("""
                <tr>
                    <th class=\"icon tableHeading\"></th>
                    <th class=\"anzahl tableHeading\">Anzahl</th>
                    <th class=\"produkt tableHeading\">Produkt</th>
                    <th class=\"liter tableHeading\">Liter</th>
                </tr>
                """)

                #fuegt produkte hinzu

                for product in products:
                    outfile.write("<tr>")
                    outfile.write("<td class=\"icon\"><img class=\"imgIcon\" src=\"icons/" + str(product.name) + ".svg\" alt=\"\"></td>")
                    outfile.write("<td class=\"anzahl\">" + str(product.count) + "</td>")
                    outfile.write("<td class=\"produkt\">" + str(product.name) + "</td>")
                    outfile.write("<td class=\"liter\">" + str(product.count * product.water) + "</td>")
                    outfile.write("</tr>")

                #gesamter wasserverbrauch

                outfile.write("""
                <tr>
                <td class=\"icon ergebnis\"></td>
                <td class=\"ergebnis\"></td>
                <td class=\"ergebnis\"></td>
                <td class=\"liter ergebnis\">
                """)

                outfile.write("<b>" + str(totalWater) + "</b>")

                outfile.write("""
                </td>
                </tr>

        </table>
    </div>
    <div class=\"tipps\">
    """)

                for product in worseProducts:
                    outfile.write("""
                        <div class=\"tipp\">
                            <div class=\"iconTipp\">
                    """)

                    outfile.write("<img src=\"icons/Nudeln.svg\" alt=\"\">")

                    outfile.write("""
                        </div>
                            <div class=\"textTipp\">
                    """)

                    outfile.write("<h1>Nudeln</h1>")
                    outfile.write("<br>")
                    outfile.write("""<p>ipsum dolor sit amet consectetur adipisicing elit. Beatae, eaque est inventore sint, tempora vitae tenetur delectus
                            magni enim mollitia dicta animi, ea eligendi? Nulla sit velit modi repudiandae eos magni voluptate temporibus,
                            veritatis consectetur eveniet. Quae amet explicabo, ut sed consequuntur velit in ratione enim ea ipsam iste
                            molestiae?</p>""")
                    outfile.write("""
                        </div>
                    </div>
                    """)

                outfile.write("""
            <div class=\"footer\">

                <div class=\"center\">
                    <img src=\"frame.png\" alt="" style=\"width:100px\">

                </div>
                <div class=\"center\">
                    <p>
                        Projekt von: 
                        <br>
                        Helene Lehmann, Nicolas Martin und Alesandra Piazza
                    </p>
                </div>

            </div>
        </body>
        </html>
                    """)

#========================================================================================================


            #erstellt ein pdf aus der html datei
            pdfkit.from_file("/home/pi/Desktop/prototype_v3/print_data/data.html", "/home/pi/Desktop/prototype_v3/data.pdf")
            #sendet dem Drucker den Befehl zum Drucken
            call(['lp', '-d', 'Epson_Stylus_SX420W', '/home/pi/Desktop/prototype_v3/data.pdf'])

            print("printing Bill")

        elif value == "resetBackend":
            print("Backend wurde resettet")


        else:
            await websocket.send(value)


start_server = websockets.serve(backendSocket, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

