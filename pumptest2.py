import RPi.GPIO as GPIO
import time

LED_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# Create PWM instance at 100 Hz
pwm = GPIO.PWM(LED_PIN, 100)
pwm.start(0)  # Start with 0% duty cycle

try:
    while True:
        # Fade in
        for duty_cycle in range(0, 101, 1):
            pwm.ChangeDutyCycle(duty_cycle)
            time.sleep(2.0)

        # Fade out
        for duty_cycle in range(100, -1, -1):
            pwm.ChangeDutyCycle(duty_cycle)
            time.sleep(2.0)

except KeyboardInterrupt:
    pass

finally:
    pwm.stop()
    GPIO.cleanup()