from tkinter.messagebox import NO
import RPi.GPIO as GPIO
from multiprocessing import Process, Queue
import time

active_servos = {}

def moveServo(pin, hz, angle, t=1):
    """
    moveServo(pin, hz, angle, t=1) : moves a servo on a pin, using pwm on a given frequency to a given angle\n
    pin   : the pin the servo is attatched to\n
    hz    : the pwm frequency the servo operates at\n
    angle : the angle to turn the servo to\n
    t     : the time to wait for the servo to turn\n
    """
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

    GPIO.cleanup(pin)


def updateList():
    """
    updateList() : updates the list of active pins 
    """
    for pin, process in active_servos:
        if process != None:
            if not process.is_alive():
                active_servos[pin] = None

def isMoving(pin):
    """
    isMoving(pin) : checks if the servo on a given pin is active\n
    pin     : the pin number the servo is attatched to\n
    returns : true if moving, false if not\n
    \n
    calls updateList()
    """
    updateList()

    if pin not in active_servos.keys():
        active_servos[pin] = None
        return False

    return active_servos[pin] == None

def moveServoAsync(pin, hz, angle, t=1):
    """
    moveServoAsync(pin, hz, angle, t=1) : moves a servo without blocking a main event loop\n
    returns : true if the servo was moved, false if the servo was already moving
    """
    if not isMoving(pin):
        p = Process(target=moveServo, args=(pin,hz,angle,t,))
        active_servos[pin] = p
        p.start()
        return True
    return False


if "__main__" in __name__:
    moveServoAsync(11,50,0,1)
    
    while isMoving(11):
        pass

    moveServoAsync(11,50,90,1)

    while isMoving(11):
        pass

    moveServoAsync(11,50,0,1)
