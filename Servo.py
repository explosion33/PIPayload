import RPi.GPIO as GPIO

class Servo:
    def __init__(this, pin, hz):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.OUT)
        this.pwm = GPIO.PWM(pin, hz)
        this.pwm.start(0)
        this.pin = pin

    def setAngle(this, angle):
        duty = angle/18 + 2 #this needs to be tested, its different for every servo
        GPIO.output(this.pin, True)
        this.pwm.ChangeDutyCycle(duty)

        # some sort of delay here, most likely want to use processing module
        # sleep(1)

        GPIO.output(this.pin, False)
        this.pwm.ChangeDutyCycle(0)