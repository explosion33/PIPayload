"""
Ethan Armstrong
warmst@uw.edu
Implements the Igniter class
"""
import RPi.GPIO as GPIO
import time
from multiprocessing import Process

class Igniter():
    """
    Igniter object, capable of sending a pulse down a specified GPIO pin on a raspberry pi
    """
    def __init__(this, pin):
        """
        Igniter(pin) | creates a new Igniter object on a given pin\n
        pin | the pin, in board mode to send a gate signal
        """
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin,False)

        this._pin = pin

    def ignite_sync(this, on_time=1):
        """
        ignite_sync(on_time) | ignites the connected charge while blocking for on_time seconds\n
        on_time | the time to keep the circuit closed for (seconds), default : 1
        """
        this._pulse(this._pin, on_time)
    
    def ignite(this,on_time=1):
        """
        ignite(on_time) | ignited the connected charge for on_time time in a background task\n
        on_time | the time to keep the circuit closed for (seconds), default : 1 
        """
        p = Process(target=this._pulse, args=[this._pin,on_time])
        p.start()
    
    @staticmethod
    def _pulse(pin, on_time=1):
        """
        _pulse(pin, on_time=1) | a class independent private method to handle a generic pulse event on the set pin\n
        pin | the pin to pulse on or off (board mode)\n
        on_time | the time to keep the circuit closed (seconds) default : 1
        """
        GPIO.output(pin, True)
        time.sleep(on_time)
        GPIO.output(pin, False)

if "__main__" in __name__:
    ig = Igniter(11)
    ig.ignite()