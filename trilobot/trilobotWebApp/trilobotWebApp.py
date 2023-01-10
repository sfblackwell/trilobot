from flask import Flask, render_template, request
import json
import time
import os
import mysql.connector
from trilobot import *
import random

import sys
import keyring

sys.path.append('/home/pi/backendKeyring')
from pyPasswordsClass import backendKeyring

#	get db credentials

keyring.set_keyring(backendKeyring())

USERsql = "flaskWebAppUser"
PWsql = keyring.get_password("SQL", "flaskWebAppUser")

#
#	get some initial parameters
#
# Creating connection object

mydb = mysql.connector.connect(
host = "localhost",
user = USERsql,
password = PWsql)

mycursor = mydb.cursor()
mycursor.execute("use trilobot")

#	get parameters

sql = "SELECT motorStatic FROM parameters ORDER BY id DESC LIMIT 1"

mycursor.execute(sql)
parametersResult = mycursor.fetchone()

motorStatic = parametersResult[0]
print("motorStatic: ", motorStatic)

mycursor.close()
mydb.close()
    
# close my sql out

#	motor related items

STATIC = True
#STATIC = False

# 
if STATIC or motorStatic == "checked":
    motor_factor  = 0
else:
    motor_factor  = 1    
#     

MOTOR_STOP  = 0
MOTOR_INC   = 0.05
MOTOR_START = 0.3
MOTOR_MAX   = 1
    
ACT_RELEASED = "ACT_RELEASED"
ACT_PRESSED = "ACT_PRESSED"
ACT_HELD = "ACT_HELD"

#	few colors

BLANK  = (0, 0, 0)
RED    = (255, 0, 0)
GREEN  = (0, 255, 0)
CYAN   = (0, 255, 255)
BLUE   = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE  = (255, 255, 255)

#
#	start flask
#

print("# Initialise Flask ##########")
app = Flask(__name__)
print("# Flask Initialised #########")

#
#	this builds the parameters data set from the DB
#	and displays parameters page for user editing
#	template trilobotsetup.html renders the page for the user
#

@app.route('/trilobotsetup')
def trilobotsetup():
    
    print("The time is: ",str(time.ctime()),"/trilobotsetup")
    
    # Creating connection object
    
    mydb = mysql.connector.connect(
    host = "localhost",
    user = USERsql,
    password = PWsql)
    
    mycursor = mydb.cursor()
    mycursor.execute("use trilobot")
    
    #	get parameters
    
    sql = "SELECT CONVERT(timeStamp,VARCHAR(20)) as ts, collectData, collectGPS, collectTOF, collectULT, collectENV, collectFrequency, collectGRD, showData, showGPS, showTOF, showULT, showENV, showFrequency, showGRD, startupMessage, shutdownMessage, stopEnvCollection, gameController, motorStatic, motorButtonBig, scrollMessage FROM parameters ORDER BY id DESC LIMIT 1" 
    mycursor.execute(sql)
    parametersResult = mycursor.fetchone()
    #print("sql parameters: ", parametersResult) 
   
    templateData = {'parametersTS': parametersResult[0],'collectData': parametersResult[1], 'collectGPS': parametersResult[2], 'collectTOF': parametersResult[3],
                 'collectULT': parametersResult[4], 'collectENV': parametersResult[5], 'collectFrequency': parametersResult[6], 'collectGRD': parametersResult[7],    
                 'showData': parametersResult[8], 'showGPS': parametersResult[9], 'showTOF': parametersResult[10],
                 'showULT': parametersResult[11], 'showENV': parametersResult[12], 'showFrequency': parametersResult[13], 'showGRD': parametersResult[14],
                 'startMess': parametersResult[15], 'shutMess': parametersResult[16], 'stopEnvCollection': parametersResult[17], 'gameController': parametersResult[18],
                 'motorStatic': parametersResult[19], 'motorButtonBig': parametersResult[20], 'scrollMess': parametersResult[21]}
    
    print(templateData)
   
    mycursor.close()
    mydb.close()
        
    return render_template('trilobotsetup.html', **templateData)

#
#	this handles the update of parameters called by a javascript fetch
#	template trilobotupdatedata.html is a dummy render file
#

@app.route('/trilobotparams', methods = ['POST','GET'])
def  trilobotparams():
    
    print("The time is: ",str(time.ctime()),"/trilobotparams")

    print("***********")
    if request.method == 'POST':
        paramType = request.form['paramType']
        print("paramType",paramType)
        if paramType == "messages":
            startupMess = request.form['startupMess']
            scrollMess = request.form['scrollMess']
            shutdownMess = request.form['shutdownMess']
            print(startupMess, scrollMess, shutdownMess)
            
            sql = "UPDATE parameters SET startupMessage = %s, shutdownMessage = %s, scrollMessage = %s"
            var = (startupMess, shutdownMess, scrollMess)
            
            print("---messages-----------------------------------")
            print(sql)
            print("--------------------------------------")
            print(var)
            print("--------------------------------------")
        elif paramType == "miscItems":
            gameController = request.form['gameController']
            stopEnvCollection = "checked" if request.form['stopEnvCollection'] == "true" else ""
            motorStatic = "checked" if request.form['motorStatic'] == "true" else ""
            motorButtonBig = "checked" if request.form['motorButtonBig'] == "true" else ""
            print(gameController, stopEnvCollection, motorStatic, motorButtonBig)
            
            sql = "UPDATE parameters SET gameController = %s, stopEnvCollection = %s, motorStatic = %s, motorButtonBig = %s"
            var = (gameController, stopEnvCollection, motorStatic, motorButtonBig)
            
            print("---misc-----------------------------------")
            print(sql)
            print("--------------------------------------")
            print(var)
            print("--------------------------------------")
            
            if motorStatic == "checked":
                motor_factor = 0
            else:
                motor_factor = 1
            
        elif paramType == "options": 
            collectData = "checked" if request.form['collectData'] == "true" else ""
            showData = "checked" if request.form['showData'] == "true" else ""
            collectGPS = "checked" if request.form['collectGPS'] == "true" else ""
            showGPS = "checked" if request.form['showGPS'] == "true" else ""
            collectTOF = "checked" if request.form['collectTOF'] == "true" else ""
            showTOF = "checked" if request.form['showTOF'] == "true" else ""
            collectULT = "checked" if request.form['collectULT'] == "true" else ""
            showULT = "checked" if request.form['showULT'] == "true" else ""
            collectENV = "checked" if request.form['collectENV'] == "true" else ""
            showENV = "checked" if request.form['showENV'] == "true" else ""
            collectGRD = "checked" if request.form['collectGRD'] == "true" else ""
            showGRD = "checked" if request.form['showGRD'] == "true" else ""
            
            collectFrequency = request.form['collectFrequency']
            showFrequency    = request.form['showFrequency']
                                   
            sql = "UPDATE parameters SET collectData = %s,showData = %s,collectGPS = %s,showGPS = %s,collectTOF = %s,showTOF = %s,collectULT = %s,showULT = %s,collectENV = %s,showENV = %s,collectGRD = %s,showGRD = %s,collectFrequency = %s,showFrequency = %s"
            var = (collectData,showData,collectGPS,showGPS,collectTOF,showTOF,collectULT,showULT,collectENV,showENV,collectGRD,showGRD,collectFrequency,showFrequency) 
            
            print("---options-----------------------------------")
            print(sql)
            print("--------------------------------------")
            print(var)
            print("--------------------------------------")
            
        # 	Creating connection object
            
        mydb = mysql.connector.connect(
        host = "localhost",
        user = USERsql,
        password = PWsql)
        
        # update sql
        
        mycursor = mydb.cursor()
        mycursor.execute("use trilobot")

        mycursor.execute(sql, var)
        mydb.commit()
        
        # close out sql
        
        mycursor.close()
        mydb.close()            

    
    print("***********")
    
    # all done
    
    return render_template('trilobotupdatedata.html')

#
#	this builds the data set from the DB called by a timed periodic javascript fetch
#	template trilobotdata.json renders the json for use
#
@app.route('/trilobotdata')
def trilobotdata():
    
    print("The time is: ",str(time.ctime()),"/trilobotdata")
    
    # Creating connection object
    
    mydb = mysql.connector.connect(
    host = "localhost",
    user = USERsql,
    password = PWsql)
    
    mycursor = mydb.cursor()
    mycursor.execute("use trilobot")
    
    #	get parameters
    
    sql = "SELECT CONVERT(timeStamp,VARCHAR(20)) as ts, collectData, collectGPS, collectTOF, collectULT, collectENV, collectFrequency, collectGRD, showData, showGPS, showTOF, showULT, showENV, showFrequency, showGRD, motorButtonBig FROM parameters ORDER BY id DESC LIMIT 1" 
    mycursor.execute(sql)
    parametersResult = mycursor.fetchone()
    #print("sql parameters: ", parametersResult)
       
    #	get bme680 data

    sql = "SELECT id as idCol, temperature, pressure, humidity, CONVERT(timeStamp,VARCHAR(20)) as ts FROM bme280 ORDER BY id DESC LIMIT 1" 
    mycursor.execute(sql)
    bme280result = mycursor.fetchone()
    #print("sql data: ", bme280result)
    
    #	get GPS data
    
    sql = "SELECT id as idCol, latitude, longitude, altitude, num_sats, gps_qual, CONVERT(timeStamp,VARCHAR(20)) as ts FROM GPSdata ORDER BY id DESC LIMIT 1" 
    mycursor.execute(sql)
    GPSresult = mycursor.fetchone()
    #print("sql data: ", GPSresult)
    
    #	get TOF data 
          
    sql = "SELECT id as idCol, minCell, min, max, avg, p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, CONVERT(timeStamp,VARCHAR(20)) as ts FROM frontTOF ORDER BY id DESC LIMIT 1" 
    mycursor.execute(sql)
    TOFresult = mycursor.fetchone()
    #print("sql data: ", TOFresult)

    #	get rear ultrasound data
    
    sql = "SELECT id as idCol, distance, CONVERT(timeStamp,VARCHAR(20)) as ts FROM RearUltrasound ORDER BY id DESC LIMIT 1" 
    mycursor.execute(sql)
    ULTresult = mycursor.fetchone()
    #print("sql data: ", ULTresult)  
    
    datalist = [{'parametersTS': parametersResult[0],'collectData': parametersResult[1], 'collectGPS': parametersResult[2], 'collectTOF': parametersResult[3],
                 'collectULT': parametersResult[4], 'collectENV': parametersResult[5], 'collectFrequency': parametersResult[6], 'collectGRD': parametersResult[7],    
                 'showData': parametersResult[8], 'showGPS': parametersResult[9], 'showTOF': parametersResult[10],
                 'showULT': parametersResult[11], 'showENV': parametersResult[12], 'showFrequency': parametersResult[13], 'showGRD': parametersResult[14], 'motorButtonBig': parametersResult[15], 
                 'bme280TS': bme280result[4], 'idCol': bme280result[0], 'temperature': bme280result[1], 'pressure': bme280result[2],'ENVts': bme280result[4],
                 'humidity': bme280result[3], 'gpsTS': GPSresult[6],'latitude': GPSresult[1], 'longitude': GPSresult[2] , 'altitude': GPSresult[3],
                 'num_sats': GPSresult[4], 'gps_qual':  GPSresult[5], 'tofTS': TOFresult[21], 'minCell': TOFresult[1], 'min': TOFresult[2], 'max': TOFresult[3], 'avg': TOFresult[4],
                 'p0': TOFresult[5], 'p1': TOFresult[6], 'p2': TOFresult[7], 'p3': TOFresult[8], 'p4': TOFresult[9], 'p5': TOFresult[10], 'p6': TOFresult[11], 'p7': TOFresult[12],
                 'p8': TOFresult[13], 'p9': TOFresult[14], 'p10': TOFresult[15], 'p11': TOFresult[16], 'p12': TOFresult[17], 'p13': TOFresult[18], 'p14': TOFresult[19], 'p15': TOFresult[20], 'TOFts': TOFresult[21],
                 'ULTdistance': ULTresult[1],'ULTts': ULTresult[2]}]
   
    mycursor.close()
    mydb.close()
    
    # close my sql out

    datajson = json.dumps(datalist, indent=4 )

    return render_template('trilobotdata.json', data = datajson)

#
#	effectivly a container for the driving pages
#	rendered by trilobot.html
#

@app.route('/')
def trilobot():  
    
    print("The time is: ",str(time.ctime()),"/trilobotbot") 
    
    return render_template('trilobot.html')


#
#	this handles the collect/show button responces called by a javascript fetch
#	it uses the dummy render template trilobotupdatedata.html
#

@app.route('/trilobotupdatedata', methods = ['POST','GET'])
def  trilobotupdatedata():

    print("The time is: ",str(time.ctime()),"/trilobotupdatedata")
    
    print("***********")
    if request.method == 'POST':
        gridName = request.form['dataCollect']
        newGridValue = request.form['dataCollectStatus']
        print(gridName, newGridValue)
    print("***********")

    
    # Creating connection object
    
    mydb = mysql.connector.connect(
    host = "localhost",
    user = USERsql,
    password = PWsql)
    
    mycursor = mydb.cursor()
    mycursor.execute("use trilobot")
    
    #	set parameters
    
    sql = "UPDATE parameters SET " + gridName + " = '" + newGridValue + "' "

    print(sql)
    print("***********")
    
    mycursor.execute(sql)
    mydb.commit()
    mycursor.close()
    mydb.close()
    
    return render_template('trilobotupdatedata.html')


#
#	this is the restart/shutdown response called by a javascript fetch
#	it uses the dummy render template trilobotupdatedata.html
#

@app.route('/trilobotrestart', methods = ['POST','GET'])
def  trilobotrestart():

    print("The time is: ",str(time.ctime()),"/trilobotrestart")

    print("***********")
    if request.method == 'POST':
        restartType = request.form['type']
        print(restartType)
    print("***********")

    if restartType == "piShutdownConfirm":
        print("shuting down now")
        print("***********")
        cmd = "sudo shutdown -h now"
        os.system(cmd)
        time.sleep(30)       
    elif restartType == "piRebootConfirm":
        print("Restarting now")
        print("***********")
        cmd = "sudo reboot now"
        os.system(cmd)
        time.sleep(30)

    return render_template('trilobotupdatedata.html')

#
#	this is the driving/motor control html page called by a javascript fetch
#	uses the json render template trilobotdata.json
#

@app.route('/trilobotmotor', methods = ['POST','GET'])
def  trilobotmotor():

    print("The time is: ",str(time.ctime()),"/trilobotmotor")

    # set up trilobot class if needed

    if 'tbot' in globals():
        print("tbot object exits")
    else:    
        print("# Initialise Motors & LEDs ##")
        global tbot
        print("tbot setup")

        tbot = Trilobot()  

        if STATIC:
            print("Motors static", motor_factor)

        else:
            print("Motors active", motor_factor)
            
        print("Stop Speed", MOTOR_STOP)
        print("Inc. Speed", MOTOR_INC)
        print("Start Speed", MOTOR_START)
        print("Max. Speed", MOTOR_MAX)

        print("Disable motors and servo for startup")
        tbot.disable_servo()
        tbot.disable_motors()

        tbot.set_underlight(LIGHT_FRONT_RIGHT, RED)
        tbot.set_underlight(LIGHT_FRONT_LEFT, GREEN)
        tbot.set_underlight(LIGHT_MIDDLE_RIGHT, WHITE)
        tbot.set_underlight(LIGHT_MIDDLE_LEFT, BLUE)
        tbot.set_underlight(LIGHT_REAR_RIGHT, YELLOW)
        tbot.set_underlight(LIGHT_REAR_LEFT, CYAN)
        tbot.fill_underlighting(255,255,255)
        
    if 'motorSpeed' in globals():
        print("motorSpeed exits")
    else:
        global motorSpeed
        motorSpeed = MOTOR_START
        print("motorSpeed created")

    if 'lastBtn' in globals():
        print("lastBtn exits")
    else:
        global lastBtn
        lastBtn = ""
        print("lastBtn created")
        
    if 'lastReaction' in globals():
        print("lastReaction exits")
    else:
        global lastReaction
        lastBtn = ""
        print("lastReaction created")
         
    print("Waiting")
    print("# Motors Ready ###############")
    
#	carry on with steering etc

    btn = ""
    reaction = ""  
    print("***********")
    if request.method == 'POST':
        
        btn = request.form['btnAction']
        reaction = request.form['btnReaction']
        motorSpeed = int(request.form['motorSpeed'])/100 * motor_factor
        print("motorSpeed",motorSpeed)

        #	control motors            
        
        if btn == "BTN_UP":
            if reaction == ACT_PRESSED:
                tbot.forward(speed=motorSpeed)
                lColor = YELLOW
                rColor = YELLOW
            elif reaction == ACT_HELD:
                tbot.forward(speed=motorSpeed)
                lColor = GREEN
                rColor = GREEN
            elif reaction == ACT_RELEASED:
                tbot.stop()
                lColor = WHITE
                rColor = WHITE
                
            tbot.set_underlight(LIGHT_FRONT_LEFT, lColor)
            tbot.set_underlight(LIGHT_FRONT_RIGHT, rColor)
             
        elif btn == "BTN_DOWN":
            if reaction == ACT_PRESSED:
                tbot.backward(speed=motorSpeed)
                lColor = YELLOW
                rColor = YELLOW 
            elif reaction == ACT_HELD:
                tbot.backward(speed=motorSpeed)
                lColor = GREEN
                rColor = GREEN
            elif reaction == ACT_RELEASED:
                tbot.stop()
                lColor = WHITE
                rColor = WHITE
                
            tbot.set_underlight(LIGHT_REAR_LEFT, lColor)
            tbot.set_underlight(LIGHT_REAR_RIGHT, rColor)
           
        elif btn == "BTN_LEFT":
            if reaction == ACT_PRESSED:
                tbot.turn_left(speed=motorSpeed)
                lColor = YELLOW
                rColor = YELLOW
            elif reaction == ACT_HELD:
                tbot.turn_left(speed=motorSpeed)
                lColor = GREEN
                rColor = GREEN
            elif reaction == ACT_RELEASED:
                tbot.stop()
                lColor = WHITE
                rColor = WHITE
                
            tbot.set_underlight(LIGHT_FRONT_LEFT, lColor)
            tbot.set_underlight(LIGHT_FRONT_RIGHT, rColor)
                
        elif btn == "BTN_RIGHT":
            if reaction == ACT_PRESSED:
                tbot.turn_right(speed=motorSpeed)
                lColor = YELLOW
                rColor = YELLOW
            elif reaction == ACT_HELD:
                tbot.turn_right(speed=motorSpeed)
                lColor = GREEN
                rColor = GREEN
            elif reaction == ACT_RELEASED:
                tbot.stop()
                lColor = WHITE
                rColor = WHITE
                
            tbot.set_underlight(LIGHT_REAR_LEFT, lColor)
            tbot.set_underlight(LIGHT_FRONT_RIGHT, rColor)
            
        elif btn == "BTN_TLEFT":
            if reaction == ACT_PRESSED:
                tbot.curve_forward_left(speed=motorSpeed)
                lColor = BLUE
                rColor = BLUE
            elif reaction == ACT_HELD:
                tbot.curve_forward_left(speed=motorSpeed)
                lColor = RED
                rColor = RED
            elif reaction == ACT_RELEASED:
                tbot.stop()
                lColor = WHITE
                rColor = WHITE
                
            tbot.set_underlight(LIGHT_FRONT_LEFT, lColor)
            tbot.set_underlight(LIGHT_REAR_RIGHT, rColor)
            
        elif btn == "BTN_TRIGHT":
            if reaction == ACT_PRESSED:
                tbot.curve_forward_right(speed=motorSpeed)
                lColor = BLUE
                rColor = BLUE
            elif reaction == ACT_HELD:
                tbot.curve_forward_right(speed=motorSpeed)
                lColor = RED
                rColor = RED
            elif reaction == ACT_RELEASED:
                tbot.stop()
                lColor = WHITE
                rColor = WHITE
                
            tbot.set_underlight(LIGHT_REAR_LEFT, lColor)
            tbot.set_underlight(LIGHT_FRONT_RIGHT, rColor)

        elif btn == "BTN_RLEFT":
            if reaction == ACT_PRESSED:
                tbot.curve_backward_left(speed=motorSpeed)
                lColor = BLUE
                rColor = BLUE
            elif reaction == ACT_HELD:
                tbot.curve_backward_left(speed=motorSpeed)
                lColor = RED
                rColor = RED
            elif reaction == ACT_RELEASED:
                tbot.stop()
                lColor = WHITE
                rColor = WHITE
                
            tbot.set_underlight(LIGHT_FRONT_LEFT, lColor)
            tbot.set_underlight(LIGHT_REAR_RIGHT, rColor)
            
        elif btn == "BTN_RRIGHT":
            if reaction == ACT_PRESSED:
                tbot.curve_backward_right(speed=motorSpeed)
                lColor = BLUE
                rColor = BLUE
            elif reaction == ACT_HELD:
                tbot.curve_backward_right(speed=motorSpeed)
                lColor = RED
                rColor = RED
            elif reaction == ACT_RELEASED:
                tbot.stop()
                lColor = WHITE
                rColor = WHITE
                
            tbot.set_underlight(LIGHT_REAR_LEFT, lColor)
            tbot.set_underlight(LIGHT_FRONT_RIGHT, rColor)

        elif btn == "BTN_STOP":
            tbot.stop()

            lColor = WHITE
            rColor = WHITE
                
            tbot.set_underlight(LIGHT_REAR_LEFT, lColor)
            tbot.set_underlight(LIGHT_FRONT_RIGHT, rColor) # update lask btn and motor speed
        
        if btn != "BTN_STOP" and btn != "BTN_X" and btn != "BTN_Y" and btn != "BTN_A" and btn != "BTN_B": 
            if btn == lastBtn and reaction == ACT_PRESSED and lastReaction == ACT_PRESSED:
                motorSpeed = motorSpeed + MOTOR_INC
                if motorSpeed > MOTOR_MAX:
                        motorSpeed = MOTOR_MAX    
            
            print("***********")
            print("Action:", btn, "Reaction:", reaction, "lastBtn:", lastBtn, "motorSpeed:", motorSpeed)
            print("***********")
            lastBtn = btn
            lastReaction = reaction

#	control servo
    
        lColor = RED
        rColor = RED
        if btn == "BTN_X":
            if reaction == ACT_PRESSED or reaction == ACT_HELD:
                tbot.servo_to_center()
                lColor = GREEN
                rColor = GREEN
            elif reaction == ACT_RELEASED:
                tbot.disable_servo()
                lColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                rColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        elif btn == "BTN_Y":
            if reaction == ACT_PRESSED or reaction == ACT_HELD:
                tbot.servo_to_max()
                lColor = YELLOW
                rColor = YELLOW
            elif reaction == ACT_RELEASED:
                tbot.disable_servo()
                lColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                rColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        elif btn == "BTN_A":
            if reaction == ACT_PRESSED or reaction == ACT_HELD:
                tbot.servo_to_min()
                lColor = BLUE
                rColor = BLUE
            elif reaction == ACT_RELEASED:
                tbot.disable_servo()
                lColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                rColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        elif btn == "BTN_B":
            if reaction == ACT_PRESSED or reaction == ACT_HELD:
                tbot.disable_servo()
                lColor = WHITE
                rColor = WHITE
            elif reaction == ACT_RELEASED:
                tbot.disable_servo()
                lColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                rColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                
            tbot.set_underlight(LIGHT_FRONT_LEFT, lColor)
            tbot.set_underlight(LIGHT_FRONT_RIGHT, rColor)
    
#    return render_template('trilobotupdatedata.html')

    motorSpeedSlider = int(motorSpeed*100)
    datalist = [{'motorSpeed': motorSpeedSlider, 'motorSpeed1': motorSpeedSlider}]
 
    datajson = json.dumps(datalist, indent=4 )
    print(datajson)
    return render_template('trilobotdata.json', data = datajson)


# 	lets get going

if __name__ == '__main__':
        
    print("# Initialise Flask 2 #########")
    app.run(debug=True, host='0.0.0.0')
    print("# Flask Initialised 2 ########")    
    



