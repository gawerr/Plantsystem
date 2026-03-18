#!/usr/bin/env python3

import RPi.GPIO as GPIO
import datetime
import spidev 
import time
import sys

# Constants

# create SPI connection
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000 # 1 MHz

# function to read out data from MCP3008 ADC 10BIT
def readData(channel):
      adc = spi.xfer2([1,(8+channel)<<4,0])
      data = ((adc[1]&3) << 8) + adc[2]
      return data

# Scale raw ADC (0-1023) to 1-10; 10 is highest moisture
def moistureScale(raw_value, min_raw=0, max_raw=25, min_scaled=1, max_scaled=12):
      if raw_value < min_raw:
          raw_value = min_raw
      if raw_value > max_raw:
          raw_value = max_raw
      scaled = ((raw_value - min_raw) / (max_raw - min_raw)) * (max_scaled - min_scaled) + min_scaled
      return round(scaled, 1)

try:
    while True:
        # read moisture data from channel 0
        raw = readData(0)
        moisture = moistureScale(raw)
        print("Raw moisture:", raw, "Scaled moisture (1-10):", moisture)
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit(0)  # Exit the program cleanly
