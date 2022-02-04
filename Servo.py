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
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.OUT)
        this.pwm = GPIO.PWM(pin, hz)
        this.pwm.start(0)
        this.pin = pin

        this.isMoving = False


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
        GPIO.output(this.pin, True)

        #send duty cycle for given angle
        duty = angle/18 + 2
        this.pwm.ChangeDutyCycle(duty)

        #wait for servo to turn
        p = Process(target=asyncSleep, args=(time, this.afterMove))
        p.start()

        

    def afterMove(this):
        this.pwm.ChangeDutyCycle(0)

        GPIO.output(this.pin, False)

        this.isMoving = False



if "__main__" in __name__:
    s = Servo(3,50)
    s.setAngle(40)