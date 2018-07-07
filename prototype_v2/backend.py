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

        while 1:

            #liest den arduino aus
            actualInput = arduinoSerial.readline()
            #überprüft, ob der Arduino etwas gesendet hat
            if len(actualInput) > 0:
                

                #verarbeitet den Input
                actualInput = actualInput[:-2]
                actualInput = actualInput.decode("utf-8")
                actualInput = str(actualInput)

                #waehlt Eintrag aus der Datenbak aus

                sql = "SELECT * FROM `food` WHERE rfid=\'" + actualInput + "\'"
                cursor.execute(sql)

                data = cursor.fetchone()

                #verarbeitet den SQL Eintrag, und schreibt ihn in das Products-Array
                if data:
                    actualName = data[1]
                    if actualName not in productNameList:
                        productNameList.append(actualName)
                        products.append(Food(data[1], data[7], data[6], data[7]))
                    
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
                    await websock.send(json.dumps(totalWater))
        
        elif value == "printBill":

            #erstellt das html dokument
            with open('/home/pi/Desktop/prototype_v3/print_data/data.html', 'w+') as outfile:
                outfile.write("""
                    <!DOCTYPE html>
                    <html lang=\"en\">

                    <head>
                        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
                        <meta http-equiv=\"X-UA-Compatible\" content=\"ie=edge\">
                        <script src=\"p5/p5.min.js\"></script>
                        <script src=\"jsBackend/backend_platzhalter.js\"></script>
                        <script src=\"js/main.js\"></script>
                        <title>AQUALITY</title>
                        <meta charset=\"UTF-8\" />
                        <link rel=\"stylesheetß\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css\">
                        <script src=\"https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js\"></script>
                        <script src=\"https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.0/umd/popper.min.js\"></script>
                        <script src=\"https://maxcdn.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js\"></script>
                        <script src=\"https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js\"></script>
                        <style>
                            .grid-container {
                                grid-template-columns: 50vw 50vw;
                                display: grid;
                                align-content: center;
                            }
                            body {
                                font-size: 12pt;
                            }
                            table {
                                font-family: arial, sans-serif;
                                border-collapse: collapse;
                                width: 100%;
                            }
                            td {
                                padding: 8px;
                            }
                            th {
                                padding: 8px;
                                border-bottom: 1px solid black;
                            }
                            tr:nth-child(even) {
                                /*background-color: #dddddd;*/
                            }
                            
                            p {
                                font-size:10pt;
                            }
                            .logo {
                                text-align: left;
                                margin-left: 10%;
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
                                padding-left: 10%;
                                width: 90vw;
                            }
                            .right {
                                text-align: right;
                            }
                            .anzahl {
                                width: 15vw;
                            }
                            .produkt {}
                            .liter {
                                text-align: right;
                            }
                            .ergebnis {
                                border-top: 1px solid black;
                            }
                            .contact {
                                width: 100%;
                                position: absolute;
                                bottom: 5%;
                            }
                            .left {
                                text-align: left;
                                padding: 2%;
                            }
                        </style>
                    </head>

                    <body>
                        <div class=\"center\">
                            <img src=\"aquality_logo_sw.svg\" alt=\"\" id=\"logo\">
                        </div>

                        <div class=\"productTable\">
                            <table>
                                <tr>
                                    <th class=\"anzahl\">Anzahl</th>
                                    <th class=\"produkt\">Produkt</th>
                                    <th class=\"liter\">Liter</th>
                                </tr>
                """)

                #einzelnen produkte hinzufügen

                for product in products:
                    outfile.write("<tr>")
                    
                    outfile.write("<td class=\"anzahl\">" + str(product.count) + "</td>")
                    outfile.write("<td class=\"produkt\">" + str(product.name) + "</td>")
                    outfile.write("<td class=\"liter\">" + str(product.water * product.count) + "</td>")

                    outfile.write("</tr>")

                outfile.write("""
                            <tr>
                <td class=\"ergebnis\"></td>
                <td class=\"ergebnis\"></td>
                <td class=\"liter ergebnis\">
                    <!--Ergebnis Gesamtwasserverbrauch-->
                """)

                #gesamt Wasser

                outfile.write(str(totalWater))

                #
                
                #schließt die tabelle
                outfile.write("""
                            </td>
                            </tr>

                        </table>
                    </div>

                    <div class=\"grid-container contact\">

                        <div class=\"right\">
                            <img src=\"frame.png\" alt=\"\" style=\"width:100px\">

                        </div>
                        <div class=\"left\">
                            <p>
                                Projekt von: 
                                <br>
                                Helene Lehmann, 
                                <br>
                                Nicolas Martin und 
                                <br> 
                                Alesandra Piazza
                            </p>
                        </div>

                    </div>

                </body>
                </html>
                """)


            #erstellt ein pdf aus der html datei
            pdfkit.from_file("/home/pi/Desktop/prototype_v3/print_data/data.html", "/home/pi/Desktop/prototype_v3/data.pdf")
            #sendet dem Drucker den Befehl zum Drucken
            call(['lp', '-d', 'Epson_Stylus_SX420W', '/home/pi/Desktop/prototype_v3/print_data/data.pdf'])

            print("printing Bill")

        elif value == "resetBackend":
            print("Backend wurde resettet")


        else:
            await websocket.send(value)


start_server = websockets.serve(backendSocket, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

