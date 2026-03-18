#!/usr/bin/env python3

import time
import sys
import RPi.GPIO as GPIO
import spidev 

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