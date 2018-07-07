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

        while 1:

            #liest den arduino aus
            actualInput = arduinoSerial.readline()
            #überprüft, ob der Arduino etwas gesendet hat
            if len(actualInput) > 0:
                

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

                #Ueberfuehrt das products array in ein JSON Objekt
                
                jsonData = []
                for product in products:
                    product.count = int(product.count)
                    jsonData.append(json.dumps(product.__dict__))
                
                jsonString = json.dumps(jsonData)  

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
    while True:
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
            await websocket.send(json.dumps(1324))


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
                    
                    jsonString = json.dumps(jsonData)
        
        elif value == "printBill":
            print("printing Bill")

        elif value == "resetBackend":
            print("Backend wurde resettet")

        else:
            await websocket.send(value)


start_server = websockets.serve(backendSocket, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

