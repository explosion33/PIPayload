import imp
import RPi.GPIO as GPIO
from multiprocessing import Process
import time


class Servo:
    def __init__(this, pin, hz):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.OUT)
        this.pwm = GPIO.PWM(pin, hz)
        this.pwm.start(0)
        this.pin = pin

    def setAngleTask(this, angle):
        p = Process(target=this.setAngle, args=(angle,))
        p.start()

    def setAngle(this, angle):
        
        duty = angle/18 + 2 #this needs to be tested, its different for every servo
        GPIO.output(this.pin, True)
        this.pwm.ChangeDutyCycle(duty)

        time.sleep(1)

        GPIO.output(this.pin, False)
        this.pwm.ChangeDutyCycle(0)


if "__main__" in __name__:
    s = Servo(3,50)
    s.setAngle(40)