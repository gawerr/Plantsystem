#!/usr/bin/env python3

import RPi.GPIO as GPIO
import datetime
import spidev 
import time
import sys

# Constants
pinPump = 0                               # GPIO pin of pump
needsWater = 4

# general GPIO settings
GPIO.setwarnings(False)                   # ignore warnings (unrelevant here)
GPIO.setmode(GPIO.BCM)                    # refer to GPIO pin numbers
GPIO.setup(pinPump, GPIO.OUT)             # Pi can send voltage to pump
GPIO.output(pinPump, GPIO.LOW)            # turn pump off

# create SPI connection
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000 # 1 MHz

# function to read out data from MCP3008 ADC 10BIT
def readData(channel):
      adc = spi.xfer2([1,(8+channel)<<4,0])
      data = ((adc[1]&3) << 8) + adc[2]
      return data


# read moisture data from channel 0
moisture = readData(0)

# write time and current moisture in statistic file
f = open("/home/gawerra/scripts/WateringStats.txt", "a") 
currentTime = datetime.datetime.now() 
f.write(str(currentTime) + ":\n")

print("Time: ", currentTime)

# 450 = 780 - 330, moisture in %
percentage = round(max(0, (moisture - 330) / 450 * 100), 2)
f.write("Current moisture: " + str(percentage) + "% (" + str(moisture) + ")\n")

print("Current moisture: " + str(percentage) + "% (" + str(moisture) + ")")

# if plants are to dry, start pumping and record the moisture in file
if moisture > needsWater: 
    t_end = time.time() + 4               # pump runs 4 seconds
    
    # actual pumping
    while (time.time() < t_end):                 
        GPIO.output(pinPump, GPIO.HIGH)               

    GPIO.output(pinPump, GPIO.LOW)        # turn pump off
    f.write("Plants got watered!\n")

f.write("\n")                             # line break for next log entry
f.close()                                 # close file
GPIO.cleanup()                            # proper clean up of used pins