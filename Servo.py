import RPi.GPIO as GPIO
from multiprocessing import Process, Queue
import time

def asyncSleep(t, callback):
    time.sleep(t)
    callback()

class Servo:
    def __init__(this, pin, hz):
        """
        Servo(pin, hz) : creates a new servo object\n
        pin : PWM pin for servo communication\n
        hz  : frequency in hertz to communicate with the servo
        """
        


    def setAngle(this,angle,t=1):
        """
        setAngleTask(angle, time) : communicates with servo to set its angle\n
        angle : int, the angle to set the servo\n
        time  : time to wait to turn the servo (1s to be safe, but can be measured) 
        """
        if not this.isMoving:
            this.setAngleHelper(angle,t)
        else:
            print("servo is currently moving")

    #helper function
    def setAngleHelper(this, angle, t=1) -> None:
        """
        setAngleTask(angle, time) : communicates with servo to set its angle\n
        angle : int, the angle to set the servo\n
        time  : time to wait to turn the servo (1s to be safe, but can be measured) 
        """
        this.isMoving = True
        

        this.isMoving = False

        

    def afterMove(this):
        pass


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
    s = Servo(11,50)

    p = Process(target=s.setAngle, args=(0,))
    p.start()