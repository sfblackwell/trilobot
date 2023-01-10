STATIC = True
STATIC = False
 
import numpy
import colorsys
import math
import time
from support_classes import bme680class, tof, GPSclass
import board
from trilobot import *
import evdev
import mysql.connector

import sys
import keyring
sys.path.append('/home/pi/backendKeyring')
from pyPasswordsClass import backendKeyring

SWEEPS = 1  # How many sweeps of the servo to perform
STEPS = 3  # The number of discrete sweep steps
STEPS_INTERVAL = 1.5  # The time in seconds between each step of the sequence

#	motor speeds

MOTOR_STOP = 0
MOTOR_MEDIUM = 0.4
MOTOR_FAST = 1

#	few colors

BLANK  = (0, 0, 0)
RED    = (255, 0, 0)
GREEN  = (0, 255, 0)
CYAN   = (0, 255, 255)
BLUE   = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE  = (255, 255, 255)

#	game controller definitions

KEY_PRESSED = 1

ACT_RELEASED = 0
ACT_PRESSED = 1
ACT_HELD = 2

btnCode = list((
"BTN_UP",
"BTN_DOWN",
"BTN_LEFT",
"BTN_RIGHT",
"BTN_X",
"BTN_B",
"BTN_Y",
"BTN_A",
"BTN_TLEFT",
"BTN_TRIGHT",
"BTN_LINK",
"BTN_PWR"))

keyCode = list((46,
32,
18,
33,
35,
36,
23,
34,
37,
50,
49,
24))

def btnEvent(value):
    
    btnAction = ""
    if value == ACT_RELEASED:
       btnAction = "released"
    if value == ACT_PRESSED:
        btnAction = "pressed"
    if value == ACT_HELD:
       btnAction = "held"
        
    return btnAction


print("# Startup ##################")

if STATIC:
    print("static")
else:
    print("active")

#	get some SQL credentials

keyring.set_keyring(backendKeyring())

USERsql = "flaskWebAppUser"
PWsql = keyring.get_password("SQL", "flaskWebAppUser")

#get parameters from mysql

print("# Parameters ###############")
print("Reading parameters") 
try:
    
    # Creating connection object
    
    mydb = mysql.connector.connect(
    host = "localhost",
    user = USERsql,
    password = PWsql)
    
    mycursor = mydb.cursor()
    mycursor.execute("use trilobot")
    sql = "SELECT gameController FROM parameters ORDER BY id DESC LIMIT 1" 
    mycursor.execute(sql)
    parametersResult = mycursor.fetchone()
    gameController = parametersResult[0] 
   
    print("Game controller: ", gameController)
    
except:
    print("Something went wrong opening SQL parameters, setting defaults")
    gameController = '/dev/input/event2'
    print("Game controller: ", gameController)    
        
#	detect game contoller

print("# Game controller ##########")

try:
    device = evdev.InputDevice(gameController)
    
    print(device)
    print("capabilties")
    print(device.capabilities())
    print("capabilties verbose=True")
    print(device.capabilities(verbose=True))    
except:
    print("Exiting, something went wrong selecting game controller")
    print("# Game controller exit #####")
    sys.exit()
   
    
print("# Initialise ###############")

print("tbot setup")
tbot = Trilobot()
tbot.disable_servo()
print("Disable motors and servo")
tbot.set_motor_speed(MOTOR_LEFT, 0)
tbot.set_motor_speed(MOTOR_RIGHT, 0)

tbot.set_underlight(LIGHT_FRONT_RIGHT, RED)
tbot.set_underlight(LIGHT_FRONT_LEFT, GREEN)
tbot.set_underlight(LIGHT_MIDDLE_RIGHT, WHITE)
tbot.set_underlight(LIGHT_MIDDLE_LEFT, BLUE)
tbot.set_underlight(LIGHT_REAR_RIGHT, YELLOW)
tbot.set_underlight(LIGHT_REAR_LEFT, CYAN) 
time.sleep(5)
tbot.fill_underlighting(255,255,255)

print("# Looping ##################")

while True:
    
    for event in device.read_loop():
        # print(event,event.code,event.type,event.value)
        if event.type == KEY_PRESSED:
            print("# Key pressed ##############")
            
            action = ""
            keyPos = keyCode.index(event.code)
            btn = btnCode[keyPos]
            action = btn + "  " + btnEvent(event.value)
                    
            print(action)
            
            #	control motors            
            
            if btn == "BTN_UP":
                if event.value == ACT_PRESSED:
                    tbot.set_motor_speeds(MOTOR_MEDIUM, MOTOR_MEDIUM)
                    lColor = YELLOW
                    rColor = YELLOW
                if event.value == ACT_HELD:
                    tbot.set_motor_speeds(MOTOR_FAST, MOTOR_FAST)
                    lColor = GREEN
                    rColor = GREEN
                if event.value == ACT_RELEASED:
                    tbot.set_motor_speeds(MOTOR_STOP, MOTOR_STOP)
                    lColor = WHITE
                    rColor = WHITE
                    
                tbot.set_underlight(LIGHT_FRONT_LEFT, lColor)
                tbot.set_underlight(LIGHT_FRONT_RIGHT, rColor)
                    
            elif btn == "BTN_DOWN":
                if event.value == ACT_PRESSED:
                    tbot.set_motor_speeds(-MOTOR_MEDIUM, -MOTOR_MEDIUM)
                    lColor = YELLOW
                    rColor = YELLOW 
                if event.value == ACT_HELD:
                    tbot.set_motor_speeds(-MOTOR_FAST, -MOTOR_FAST)
                    lColor = GREEN
                    rColor = GREEN
                if event.value == ACT_RELEASED:
                    tbot.set_motor_speeds(-MOTOR_STOP, -MOTOR_STOP)
                    lColor = WHITE
                    rColor = WHITE
                    
                tbot.set_underlight(LIGHT_REAR_LEFT, lColor)
                tbot.set_underlight(LIGHT_REAR_RIGHT, rColor)
                
            elif btn == "BTN_LEFT":
                if event.value == ACT_PRESSED:
                    tbot.set_motor_speeds(MOTOR_MEDIUM, -MOTOR_MEDIUM)
                    lColor = YELLOW
                    rColor = YELLOW
                if event.value == ACT_HELD:
                    tbot.set_motor_speeds(MOTOR_FAST, -MOTOR_FAST)
                    lColor = GREEN
                    rColor = GREEN
                if event.value == ACT_RELEASED:
                    tbot.set_motor_speeds(MOTOR_STOP, -MOTOR_STOP)
                    lColor = WHITE
                    rColor = WHITE
                    
                tbot.set_underlight(LIGHT_FRONT_LEFT, lColor)
                tbot.set_underlight(LIGHT_REAR_RIGHT, rColor)
                    
            elif btn == "BTN_RIGHT":
                if event.value == ACT_PRESSED:
                    tbot.set_motor_speeds(-MOTOR_MEDIUM, MOTOR_MEDIUM)
                    lColor = YELLOW
                    rColor = YELLOW
                if event.value == ACT_HELD:
                    tbot.set_motor_speeds(-MOTOR_FAST, MOTOR_FAST)
                    lColor = GREEN
                    rColor = GREEN
                if event.value == ACT_RELEASED:
                    tbot.set_motor_speeds(-MOTOR_STOP, MOTOR_STOP)
                    lColor = WHITE
                    rColor = WHITE
                    
                tbot.set_underlight(LIGHT_REAR_LEFT, lColor)
                tbot.set_underlight(LIGHT_FRONT_RIGHT, rColor)
                
            elif btn == "BTN_TLEFT":
                if event.value == ACT_PRESSED:
                    tbot.curve_forward_left(MOTOR_MEDIUM)
                    lColor = BLUE
                    rColor = BLUE
                if event.value == ACT_HELD:
                    tbot.curve_forward_left(MOTOR_FAST)
                    lColor = RED
                    rColor = RED
                if event.value == ACT_RELEASED:
                    tbot.set_motor_speeds(-MOTOR_STOP, MOTOR_STOP)
                    lColor = WHITE
                    rColor = WHITE
                    
                tbot.set_underlight(LIGHT_FRONT_LEFT, lColor)
                tbot.set_underlight(LIGHT_REAR_RIGHT, rColor)
                
            elif btn == "BTN_TRIGHT":
                if event.value == ACT_PRESSED:
                    tbot.curve_forward_right(MOTOR_MEDIUM)
                    lColor = BLUE
                    rColor = BLUE
                if event.value == ACT_HELD:
                    tbot.curve_forward_right(MOTOR_FAST)
                    lColor = RED
                    rColor = RED
                if event.value == ACT_RELEASED:
                    tbot.set_motor_speeds(MOTOR_STOP, -MOTOR_STOP)
                    lColor = WHITE
                    rColor = WHITE
                    
                tbot.set_underlight(LIGHT_REAR_LEFT, lColor)
                tbot.set_underlight(LIGHT_FRONT_RIGHT, rColor)

            #	control servo
            
            elif btn == "BTN_X":
                if event.value == ACT_PRESSED or event.value == ACT_HELD:
                    tbot.servo_to_center()
                    lColor = GREEN
                    rColor = GREEN
            elif btn == "BTN_Y":
                if event.value == ACT_PRESSED or event.value == ACT_HELD:
                    tbot.servo_to_min()
                    lColor = YELLOW
                    rColor = YELLOW
            elif btn == "BTN_A":
                if event.value == ACT_PRESSED or event.value == ACT_HELD:
                    tbot.servo_to_max()
                    lColor = BLUE
                    rColor = BLUE
            elif btn == "BTN_B":
                if event.value == ACT_PRESSED or event.value == ACT_HELD:
                    tbot.disable_servo()
                    lColor = WHITE
                    rColor = WHITE
                    
            tbot.set_underlight(LIGHT_MIDDLE_LEFT, lColor)
            tbot.set_underlight(LIGHT_MIDDLE_RIGHT, rColor)
     
    time.sleep(.1)
 
 