import RPi.GPIO as GPIO
import time
import sys
import tty
import termios

# Use BCM GPIO numbering
GPIO.setmode(GPIO.BCM)
relay_pin = 18
GPIO.setup(relay_pin, GPIO.OUT)

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

print("Single-Key Pump Control")
print("o=ON | f=OFF | t=TOGGLE | q=QUIT")

pump_state = False

try:
    while True:
        key = getch().lower()

        if key == 'o':
            GPIO.output(relay_pin, GPIO.LOW)
            pump_state = True
            print("\nPump ON")

        elif key == 'f':
            GPIO.output(relay_pin, GPIO.HIGH)
            pump_state = False
            print("\nPump OFF")

        elif key == 't':
            pump_state = not pump_state
            GPIO.output(relay_pin, pump_state)
            print(f"\nPump {'ON' if pump_state else 'OFF'}")

        elif key == 'q':
            break

except KeyboardInterrupt:
    pass

finally:
    GPIO.output(relay_pin, GPIO.LOW)
    GPIO.cleanup()
    print("\nClean exit")