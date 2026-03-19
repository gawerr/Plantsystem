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

# write time and current moisture in statistic file
f = open("/home/gawerra/scripts/moisture.csv", "a") 
currentTime = datetime.datetime.now() 

try:
    # average raw readings from channel 0 for 30 seconds
    duration = 30
    start_time = time.monotonic()
    raw_values = []

    while time.monotonic() - start_time < duration:
        raw = readData(0)
        raw_values.append(raw)
        time.sleep(0.1)  # sample every 100 ms

    if raw_values:
        raw_avg = sum(raw_values) / len(raw_values)
        moisture = moistureScale(raw_avg)
        print("Raw moisture average:", round(raw_avg, 2), "Scaled moisture (1-12):", moisture)
        f.write(f"Time: {currentTime}, Current moisture: {moisture}, Raw moisture: {raw_avg}")
    else:
        print("No samples collected")

except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit(0)  # Exit the program cleanly

f.write("\n")                             # line break for next log entry
f.close()                                 # close file
GPIO.cleanup()                            # proper clean up of used pins