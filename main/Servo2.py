"""
Ethan Armstrong
warmst@uw.edu
Implements the Servo class, and test method
"""
import RPi.GPIO as GPIO
from multiprocessing import Process, Queue
import time

class Servo:
    """
    Servo object controlls a given servo continuously
    i.e. outputs a continous pwm signal to the given servo
    """
    def __init__(this, pin, hz=50, startAngle=0):
        """
        Servo(pin,hz,startAngle) | creates a new Servo object\n
        pin | the pwm controll pin the servo is attached to (board mode)\n
        hz | the hertz the servo operates at  default : 50\n
        startAngle | the angle to start the servo at  default : 0
        """
        this.pin = pin

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.OUT)

        this.pwm = GPIO.PWM(pin, hz)
        this.pwm.start(startAngle)
    
    def changeAngle(this, angle):
        """
        changeAngle(angle) | changes the angle of the servo\n
        angle | new angle in degrees
        """
        GPIO.output(this.pin, True)
        duty = angle/18 + 2
        this.pwm.ChangeDutyCycle(duty)



if "__main__" in __name__:
    s = Servo(17)
    s.changeAngle(90)

