#!/usr/bin/env python
import os
import serial, time
import smbus
import math
import RPi.GPIO as GPIO
import struct
import sys
import datetime
#import grovepi
import struct
#from grovepi import *

#
__author__ = 'Doms Genoud'

#co2 sensor
#use an external usb to serial adapter
ser = serial.Serial('/dev/ttyUSB0',  9600, timeout = 1)    #Open the serial port at 9600 baud

#To open the raspberry serial port
#ser = serial.Serial('/dev/ttyAMA0',  9600, timeout = 1)    #Open the serial port at 9600 baud

#init serial
ser.flush()


############# carbon dioxid CO2 #####################
class CO2:
#inspired from c code of http://www.seeedstudio.com/wiki/Grove_-_CO2_Sensor
#Gas concentration= high level *256+low level
    inp =[]
    cmd_zero_sensor = "\xff\x87\x87\x00\x00\x00\x00\x00\xf2"
    cmd_span_sensor = "\xff\x87\x87\x00\x00\x00\x00\x00\xf2"
    cmd_get_sensor = "\xff\x01\x86\x00\x00\x00\x00\x00\x79"
    def read(self):
        try:
          while True:
                ser.write(CO2.cmd_get_sensor)
                CO2.inp = ser.read(9)
                high_level = struct.unpack('B',CO2.inp[2])[0]
                low_level = struct.unpack('B',CO2.inp[3])[0]
                temp_co2  =  struct.unpack('B',CO2.inp[4])[0] - 40

                #output in ppm
                conc = high_level*256+low_level
                return conc

        except IOError:
                return [-1,-1]

    def calibrateZero(self):
        try:
             ser.write(CO2.cmd_zero_sensor)
             print("CO2 sensor zero calibrated")

        except IOError:
                print("CO2 sensor calibration error")

    def calibrateSpan(self):
        try:
          while True:
                #ser.write(CO2.cmd_zero_sensor)
                print("CO2 sensor span calibrated")
                break

        except IOError:
                print("CO2 sensor calibration error")

########################################################################################################
#############   MAIN
########################################################################################################
# following the specs of the sensor :
# read the sensor, wait 3 minutes, set the zero, read the sensor
c = CO2()
#CO2 sensor calib

while True:
    try:
        co2 = c.calibrateZero()
        time.sleep(2)
        print("Read after calibration-->",c.read())
        time.sleep(1)
#        break
    except IndexError:
        print("Unable to read")
    except KeyboardInterrupt:
        print("Exiting")
        sys.exit(0)
