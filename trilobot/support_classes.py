# Support  classes

import numpy
import bme680
import vl53l5cx_ctypes as vl53l5cx
from vl53l5cx_ctypes import STATUS_RANGE_VALID, STATUS_RANGE_VALID_LARGE_PULSE
import colorsys
import math
import time
from pa1010d import PA1010D
from rgbmatrix5x5 import RGBMatrix5x5
from matrix11x7 import Matrix11x7
from matrix11x7.fonts import font5x5
from lsm303d import LSM303D

# gps class

class GPSclass:
    def __init__(self):

        self.gps = PA1010D()

    def read(self):
        
        self.result = self.gps.update()
        if self.result:
            
            self.timestamp = self.gps.data['timestamp']
            self.latitude =  self.gps.data['latitude']
            self.longitude = self.gps.data['longitude']
            self.altitude =  self.gps.data['altitude']
            self.num_sats =  self.gps.data['num_sats']
            self.gps_qual =  self.gps.data['gps_qual']
            self.speed_over_ground = self.gps.data['speed_over_ground']
                
        return self.result

# bme680 class

class bme680class:
    def __init__(self):

        try:
            self.sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
        except (RuntimeError, IOError):
            self.sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

# These oversampling settings can be tweaked to
# change the balance between accuracy and noise in
# the data.

        self.sensor.set_humidity_oversample(bme680.OS_2X)
        self.sensor.set_pressure_oversample(bme680.OS_4X)
        self.sensor.set_temperature_oversample(bme680.OS_8X)
        self.sensor.set_filter(bme680.FILTER_SIZE_3)
    
    def isSensorData(self):
        
        return self.sensor.get_sensor_data()
    
    def getTemperature(self):
    
        return self.sensor.data.temperature
    
    def getPressure(self):
    
        return self.sensor.data.pressure   
    
    def getHumidity(self):
    
        return self.sensor.data.humidity
    
# pan & tilt class

class ptHat:
    def __init__(self, posP, posT, incP, incT):
        self.posP = posP
        self.posT = posT
        self.incP = incP
        self.incT = incT
    
        pantilthat.pan(posP)
        pantilthat.tilt(posT)
        
        # initialize lights
        
        pantilthat.light_mode(pantilthat.WS2812)
        pantilthat.light_type(pantilthat.GRBW)
        r, g , b, w = 0, 0, 0, 50
        
        pantilthat.brightness(2)
        
        pantilthat.set_all(r, g, b, w)
        pantilthat.show()
        time.sleep(1)
        pantilthat.clear()
        pantilthat.show()
    
    def nextPos(self):
    
        self.posP = self.posP + self.incP
        if self.posP > MINPAN and self.posP < MAXPAN:
            pantilthat.pan(self.posP)
        else:
            self.incP = self.incP * -1
        
            self.posT = self.posT + self.incT 
            if self.posT > MINTILT and self.posT < MAXTILT:
                pantilthat.tilt(self.posT)
            else:
                self.incT = self.incT  * -1 

        print("pan",self.posP, "inc", self.incP,"tilt", self.posT, "inc", self.incT)
        
    def gotoPos(self, gotoPan, gotoTilt):
         
        self.posP = gotoPan
        self.posT = gotoTilt
        pantilthat.pan(self.posP)
        pantilthat.tilt(self.posT)
        
    def setInc(self, newPanInc, newTiltInc):
        
        self.incP = newPanInc
        self.incT = newTiltInc
        
    def setLed(self, led, colour):
        
        pantilthat.set_pixel(led, colour[0],colour[1],colour[2], colour[3])
        pantilthat.show()  
        
        
# end of pan & tilt class

# tof sensor class

# tof sensor position in array

    #         =15
    #         ^
    #	1 1 1 1
    #	1 1 1 1
    #	1 1 1 1
    #	1 1 1 1
    #	^
    #	=0

class tof:
    
    def __init__(self, highRes, minDist, maxDist ):

        print("Uploading firmware, please wait...")
        self.vl53 = vl53l5cx.VL53L5CX()
        print("Done!")

        self.resHigh = highRes
        
        self.a8or4 = 8 * 8
        if highRes == False:
           self.a8or4 = 4 * 4
        
        print("res", self.a8or4)
        
        self.vl53.set_resolution(self.a8or4)
        self.vl53.enable_motion_indicator(self.a8or4)
        self.vl53.set_motion_distance(minDist, maxDist)
        self.vl53.set_ranging_frequency_hz(10)
        
        self.vl53.start_ranging()
        
        self.min = -9999
        self.max = -9999
        self.avg = -9999
        self.minCell = -9999
        self.front = -9999

    def dataReady(self):
        
        return self.vl53.data_ready()
        
    def getData(self):
        
        data = self.vl53.get_data()
#        print(self.resHigh)
        
        if self.resHigh == True:
            cells=64
            #d2 = numpy.flipud(numpy.array(data.distance_mm).reshape((8,8)))
            d1 = numpy.array(data.distance_mm).reshape((64))
            d2 = numpy.array(d1).reshape((8,8))
        else:
            cells=16
            #d2 = numpy.flipud(numpy.array(data.distance_mm).reshape((8,8)))
            
            d0 = numpy.array(data.distance_mm).reshape((64))
            d1 = numpy.delete(d0,slice(16,64),axis=0)
            d2 = numpy.array(d1).reshape((4,4))
        
        # calc few things
        
        self.min = d2.min()
        self.max = d2.max()
        self.avg = d2.sum() / d2.size
        self.front = d1[5]

        for z in range(cells):
            if int(d1[z]) == int(d2.min()):
                self.minCell = z
                break
         
        #print(self.minCell, self.min, self.max, self.avg, self.front )
              
        return d2

# end of tof sensor class

# RGBMatrix5x5 display class for TOF data

# RGBMatrix5x5 display led position in array

    #  =0
    #   ^
    #	1 1 1 1
    #	1 1 1 1
    #	1 1 1 1
    #	1 1 1 1
    #	      ^
    #	      =15

class tofToRGBMatrix5x5:
    
    def __init__(self):
        
        self.matrix = RGBMatrix5x5()

        # color distance etc arrays

        self.distances = []
        self.distances.append((250, 255, 0, 0, "Red", 2093))
        self.distances.append((500, 255, 255 , 0, "Amber", 1047))
        self.distances.append((1000, 0, 0, 255, "Blue", 523))
        self.distances.append((1500,0, 255, 0, "Green", 262))
        self.distances.append((10000,0, 0, 0, "Blank", -1))

       # setup default display       

        for x in range(5):
            self.matrix.set_pixel(x, 2, 255, 255, 255)
        for y in range(5):
            self.matrix.set_pixel(2, y, 255, 255, 255)
        self.matrix.show()
      
    def displayTOFdata(self, TOFdata):
    
        #	flip the data for display 

        fTOFdata = numpy.flip(TOFdata,0)

        r = 0
        for row in fTOFdata:
            mRow = r if r<2 else r+1
            c = 0
            for cell in row:
                mCell = c if c<2 else c+1
                
                for z in range(len(self.distances)):               
                    if cell < self.distances[z][0]:
                        break
                
#                print(cell, r, c, mRow, mCell,self. distances[z][1], self.distances[z][2], self.distances[z][3])
                self.matrix.set_pixel(mRow, mCell, self.distances[z][1], self.distances[z][2], self.distances[z][3])
                self.matrix.show()
                
                c = c+1
            r = r + 1      

# End of RGBMatrix5x5 display class for TOF data

#	matrix11x7 message scroller

class matrix11x7display:
    
    def __init__(self, startDelay, stepDelay, endDelay):
        
        self.matrix11x7 = Matrix11x7()
        
        self.matrix11x7.set_brightness(0.5)
        self.matrix11x7.clear()
        self.matrix11x7.show()
        
        self.delayStart = startDelay
        self.delayStep  = stepDelay
        self.delayEnd   = endDelay

    def scrollMessage(self, message):
    
        self.lastMessage = message
    
        self.matrix11x7.clear()                         # Clear the display and reset scrolling to (0, 0)
        length = self.matrix11x7.write_string(message)  # Write out your message
        self.matrix11x7.show()                          # Show the result
        time.sleep(self.delayStart)                		# Initial delay before scrolling

        length -= self.matrix11x7.width

        # Now for the scrolling loop...
        while length > 0:
            self.matrix11x7.scroll(1)                   # Scroll the buffer one place to the left
            self.matrix11x7.show()                      # Show the result
            length -= 1
            time.sleep(self.delayStep)             # Delay for each scrolling step

        time.sleep(self.delayEnd)                  # Delay at the end of scrolling

#	6dof class

class LSM303Dclass:
    def __init__(self):

        self.lsm = LSM303D(0x1d)
        
    # Get accelerometer values in g

    def getRealAccel(self):
        
        xyz = self.lsm.accelerometer()
        
        return xyz

    # Get compass raw values

    def getMag(self):

        xyz = self.lsm.magnetometer()
        
        return xyz

    # Get heading from the compass