#!/usr/bin/env python3

import RPi.GPIO as GPIO
import datetime
import spidev 
import time
import sys

# Constants
pinPump = 0                               # GPIO pin of pump
needsWater = 630                          # sensor value for dry air

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

try:
    while True:
        # read moisture data from channel 0
        moisture = readData(0)
        print("Moisture:", moisture)
        time.sleep(5)

except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit(0)  # Exit the program cleanly
