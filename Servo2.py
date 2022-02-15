from tkinter.messagebox import NO
import RPi.GPIO as GPIO
from multiprocessing import Process, Queue
import time

class Servo:
    def __init__(this, pin, hz=50, startAngle=0):
        this.pin = pin

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.OUT)

        this.pwm = GPIO.PWM(pin, hz)
        this.pwm.start(startAngle)
    
    def changeAngle(this, angle, t=1):
        GPIO.output(this.pin, True)
        duty = angle/18 + 2
        this.pwm.ChangeDutyCycle(duty)

    
    def disableGpioAfter(t, pin):
        time.sleep(t)
        GPIO.output(pin, False)


if "__main__" in __name__:
    s = Servo(11)
    s.changeAngle(90)

