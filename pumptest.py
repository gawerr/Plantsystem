import RPi.GPIO as GPIO
import sys
import tty
import termios

pinPump = 21  # change if needed

GPIO.setmode(GPIO.BCM)
GPIO.setup(pinPump, GPIO.OUT)
GPIO.output(pinPump, GPIO.LOW)

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
            GPIO.output(pinPump, GPIO.HIGH)
            pump_state = True
            print("\nPump ON")

        elif key == 'f':
            GPIO.output(pinPump, GPIO.LOW)
            pump_state = False
            print("\nPump OFF")

        elif key == 't':
            pump_state = not pump_state
            GPIO.output(pinPump, pump_state)
            print(f"\nPump {'ON' if pump_state else 'OFF'}")

        elif key == 'q':
            break

except KeyboardInterrupt:
    pass

finally:
    GPIO.output(pinPump, GPIO.LOW)
    GPIO.cleanup()
    print("\nClean exit")