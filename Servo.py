import RPi.GPIO as GPIO
from multiprocessing import Process, Queue
import time


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

        this.queue = Queue()

    def setAngle(this, angle, time=1) -> None:
        """
        setAngle(angle) : sets the angle of the sevo, using a background task to avoid blocking\n
        angle : int, the angle to set the servo\n
        time  : time to wait to turn the servo (1s to be safe, but can be measured) 
        """
        p = Process(target=this.setAngle, args=(this,angle,time))
        p.start()


    #helper function
    def setAngleTask(this, angle, t=1) -> None:
        """
        setAngleTask(angle, time) : communicates with servo to set its angle\n
        angle : int, the angle to set the servo\n
        time  : time to wait to turn the servo (1s to be safe, but can be measured) 
        """
        #thread safe communication, sets "isMoving" flag
        this.queue.put([True])

        GPIO.output(this.pin, True)

        #send duty cycle for given angle
        duty = angle/18 + 2
        this.pwm.ChangeDutyCycle(duty)

        #wait for servo to turn
        time.sleep(t)

        this.pwm.ChangeDutyCycle(0)

        GPIO.output(this.pin, False)

        this.queue.put([False])

    def isMoving(this) -> bool:
        """
        isMoving() : checks if the servo is actively moving\n
        returns : bool
        """
        return this.queue.get()[0]


if "__main__" in __name__:
    s = Servo(3,50)
    s.setAngle(40)