#from trilobot import *
import sys
import evdev
import numpy
import colorsys
import math
import time
from support_classes import bme680class, tof, GPSclass, tofToRGBMatrix5x5, matrix11x7display, LSM303Dclass
import board
import mysql.connector
import sys
import keyring

#	get some SQL credentials

sys.path.append('/home/pi/backendKeyring')
from pyPasswordsClass import backendKeyring

print("# Startup ##################")

keyring.set_keyring(backendKeyring())

USERsql = "flaskWebAppUser"
PWsql = keyring.get_password("SQL", "flaskWebAppUser")

print("Scolling message setup")
matrixScroll = matrix11x7display(1, 0.1, 2)
matrixScroll.scrollMessage("Starting up   ")

# print("Trilobot setup")
# tbot = Trilobot()

print("TOF to RGB setup")
RGBtof = tofToRGBMatrix5x5()

print("GPS setup")
GPSdata = GPSclass()

print("BME280 setup")
envSensor = bme680class()

print("TOF setup")
tof1 = tof(False , 400, 1499)

print("DOF setup")
dof = LSM303Dclass()

#	Loop round and get collect data

firstTime = True
while True:
    
    print("# Parameters ###############")
    print("Reading parameters") 

#     try:
        
# 	Creating connection object
    
    try:
        mydb = mysql.connector.connect(
        host = "localhost",
        user = USERsql,
        password = PWsql)
        
        mycursor = mydb.cursor()
        mycursor.execute("use trilobot")
        sql = "SELECT CONVERT(timeStamp,VARCHAR(20)) as ts, collectData, collectGPS, collectTOF, collectULT, collectENV, collectFrequency, collectGRD, collectDOF, stopEnvCollection, startupMessage, shutdownMessage, scrolMessagel FROM parameters ORDER BY id DESC LIMIT 1" 
        mycursor.execute(sql)
        parametersResult = mycursor.fetchone()
        print("sql parameters: ", parametersResult)
        
        startupMessage = parametersResult[10]
        shutdownMessage = parametersResult[11]
        scrollMessage = parametersResult[12]
        
        if firstTime:
            matrixScroll.scrollMessage(startupMessage)
        else:
            #matrixScroll.scrollMessage(scrollMessage)
            firstTime = False
            
        if parametersResult[9] == "checked":
            print("====================")
            print("Stop Signal Recieved")
            print("====================")
            matrixScroll.scrollMessage(shutdownMessage)
            sys.exit()
            
        #	carry on    
        
        collectData = parametersResult[1]
        collectGPS	= parametersResult[2]
        collectTOF	= parametersResult[3]
        collectULT	= parametersResult[4]
        collectENV	= parametersResult[5]  
        collectFrequency	= parametersResult[6]
        collectGRD	= parametersResult[7]
        collectDOF	= parametersResult[8]
        
        print("")
        print("Data Collection Options:")
        
        print("collectData",collectData)
        print("collectGPS",collectGPS)
        print("collectTOF",collectTOF)
        print("collectULT",collectULT)
        print("collectENV",collectENV)
        print("collectGRD",collectGRD)
        print("collectGRD",collectDOF)
        
        print("collectFrequency",collectFrequency)
        
    except:
        print("Something went wrong opening SQL parameters, setting defaults")

        startupMessage = ""
        shutdownMessage = ""

        collectData = "checked"
        collectGPS	= "checked"
        collectTOF	= "checked"
        collectULT	= "checked"
        collectENV	= "checked"
        collectGRD	= "checked"
        collectDOF	= "checked"
        
        collectFrequency = 30

    print("# BME280 ###################")
    
    if collectData == "checked" and collectENV == "checked" :
        print("Reading BME280")
        
        try:
            if envSensor.isSensorData():
                theTemperature= envSensor.getTemperature()
                thePressure = envSensor.getPressure()
                theHumidity = envSensor.getHumidity()

                output = '{0:.2f} C,{1:.2f} hPa,{2:.3f} %RH'.format(
                    theTemperature,
                    thePressure,
                    theHumidity)
                print(output)
                
                mycursor = mydb.cursor()
                mycursor.execute("use trilobot")
                
                sql = "INSERT INTO bme280 (temperature, pressure, humidity) VALUES (%s, %s, %s)"
                val = (theTemperature, thePressure, theHumidity)
                
                mycursor.execute(sql, val)
                mydb.commit()
                print(mycursor.rowcount, "record inserted.")
            
        except:
            print("Error at BME280")
                
    print("# TOF ######################")

    if collectData == "checked" and collectTOF ==  "checked":
        print("Reading TOF")
        
        try:
            if tof1.dataReady():
            
                data = tof1.getData()
                print(data)
                
                TOFminCell = tof1.minCell
                TOFmin = tof1.min
                TOFmax = tof1.max
                TOFavg = tof1.avg
                
                print(TOFminCell, TOFmin, TOFmax, TOFavg)
                
                mycursor = mydb.cursor()
                mycursor.execute("use trilobot")
            
                sql = "INSERT INTO frontTOF (minCell, min, max, avg, p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                val = (float(TOFminCell), float(TOFmin), float(TOFmax), float(TOFavg), float(data[0][0]), float(data[0][1]), float(data[0][2]), float(data[0][3]), float(data[1][0]), float(data[1][1]), float(data[1][2]), float(data[1][3]), float(data[2][0]), float(data[2][1]), float(data[2][2]), float(data[2][3]), float(data[3][0]), float(data[3][1]), float(data[3][2]), float(data[3][3]))       
                
                mycursor.execute(sql,val)
                mydb.commit()
                print(mycursor.rowcount, "record inserted.")
            
                distance = tof1.min /10
                print("front tof distance",distance)
                
                RGBtof.displayTOFdata(data)          
                
        except:
            print ("Error at TOF")           
 
    print("# GPS ###################")
    
    if collectData == "checked" and collectGPS == "checked":
        print("Reading GPS")
        
        try:
            if GPSdata.read():
                print(GPSdata.timestamp)
                print(GPSdata.latitude)
                print(GPSdata.longitude)
                print(GPSdata.altitude)
                print(GPSdata.num_sats)
                print(GPSdata.gps_qual)
                print(GPSdata.speed_over_ground)
         
                if GPSdata.latitude != None: 
                    mycursor = mydb.cursor()
                    mycursor.execute("use trilobot")
                
                    sql = "INSERT INTO GPSdata (latitude, longitude, altitude, num_sats, gps_qual) VALUES (%s, %s, %s, %s, %s)"
                    val = (GPSdata.latitude, GPSdata.longitude, GPSdata.altitude, GPSdata.num_sats, GPSdata.gps_qual)
                    
                    mycursor.execute(sql, val)
                    mydb.commit()
                    print(mycursor.rowcount, "record inserted.")
        except:
            print ("Error at GPS") 
    
#     print("# ULTRA ####################")       
# 
#     if collectData == "checked" and collectULT == "checked":
#         print("Reading ultrasound")
#             
#         try:
#             distance = tbot.read_distance()
#             distanceMM = int(distance*10)
#             print("rear ultrasound distance", distance, distanceMM)
#              
#             if distance >= 0:
#                 mycursor = mydb.cursor()
#                 mycursor.execute("use trilobot")
# 
#                 sql = "INSERT INTO RearUltrasound (distance) VALUES ("+str(distanceMM) +")"
#                 
#                 mycursor.execute(sql)
#                 mydb.commit()
#                 print(mycursor.rowcount, "record inserted.")
#             else:
#                 print("Invalid distance ignored")
#                 
#         except:
#             print ("Error at rear ultrasound") 

    print("# DOF ####################")       

    if collectData == "checked" and collectDOF == "checked":
        print("Reading DOF raw data")
        
        try:
            accelerXYZ = dof.getRealAccel()
            print("acceler", accelerXYZ)

            magnetoXYZ = dof.getMag()
            print("magneto", magnetoXYZ)
            
            mycursor = mydb.cursor()
            mycursor.execute("use trilobot")

            sql = "INSERT INTO 6Dof (accelerX,accelerY,accelerZ,magnetoX,magnetoY,magnetoZ) VALUES (%s,%s,%s,%s,%s,%s)"
            val = (accelerXYZ[0], accelerXYZ[1], accelerXYZ[2], magnetoXYZ[0], magnetoXYZ[1], magnetoXYZ[2])
            
            mycursor.execute(sql, val)
            mydb.commit()
            print(mycursor.rowcount, "record inserted.")
                
        except:
            print ("Error at DOF") 
 


    print("# Looping ##################")
    print("Waiting",collectFrequency)
    time.sleep(collectFrequency)

    


