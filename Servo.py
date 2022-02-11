import RPi.GPIO as GPIO
from multiprocessing import Process, Queue
import time

def moveServo(pin, hz, angle, t=1):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    pwm = GPIO.PWM(pin, hz)
    pwm.start(0)

    GPIO.output(pin, True)

    #send duty cycle for given angle
    duty = angle/18 + 2
    pwm.ChangeDutyCycle(duty)

    #wait for servo to turn
    time.sleep(t)

    pwm.ChangeDutyCycle(0)

    GPIO.output(pin, False)


if "__main__" in __name__:
    pass