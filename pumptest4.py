import RPi.GPIO as GPIO
import time

# Use BCM GPIO numbering
GPIO.setmode(GPIO.BCM)
relay_pin = 21
GPIO.setup(relay_pin, GPIO.OUT)

# Turn relay on (Low-level trigger)
GPIO.output(relay_pin, GPIO.HIGH)
time.sleep(2)

# Turn relay off
GPIO.output(relay_pin, GPIO.LOW)

time.sleep(2)
GPIO.output(relay_pin, GPIO.HIGH)
time.sleep(2)
GPIO.output(relay_pin, GPIO.LOW)
GPIO.cleanup()
