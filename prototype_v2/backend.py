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
    def __init__(self, name, count, water):
        self.name = name
        self.count = count
        self.water = water

#==============================================================================================================
#=== Initialisierung ===
#==============================================================================================================

#=== Variables ===
productNameList = []
products = []
totalWater = 0
actualProduct= "nothing"
jsonString = ""

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
        jsonData = []
        while 1:

            #liest den arduino aus
            actualInput = arduinoSerial.readline()
            #überprüft, ob der Arduino etwas gesendet hat
            if len(actualInput) > 0:
                

                actualInput = actualInput[:-2]
                actualInput = actualInput.decode("utf-8")
                actualInput = str(actualInput)

                sql = "SELECT * FROM `food` WHERE rfid=\'" + actualInput + "\'"
                cursor.execute(sql)

                data = cursor.fetchone()

                #verarbeitet den SQL Eintrag, und schreibt ihn in die beiden Arrays
                if data:
                    actualName = data[1]
                    if actualName not in productNameList:
                        productNameList.append(actualName)
                        products.append(Food(data[1], data[7], data[6]))
                    
                    actualProduct = actualName

                for product in products:
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


    global jsonString
    while True:
        value = await websocket.recv()

        if value == "getVariables":
            await websocket.send(jsonString)
        elif value == "getTotalWater":
            await websocket.send(json.dumps(1324))
        else:
            await websocket.send(value)


start_server = websockets.serve(backendSocket, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

