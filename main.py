import time
from IMU import IMU
from Logger import Logger
from Camera import Camera
from Servo2 import Servo
from GPS import GPS


def main():
    sensors = IMU()
    sensorLog = Logger("sensors.log")

    s = Servo(17,50,0)
    s.changeAngle(0)

    c = Camera((640,480))
    c.startCamera('my_video.h264')
    
    gps = GPS()

    startTime = time.time()
    currentTime = 0

    deployed = False

    while True:
        currentTime = time.time() - startTime
        if readyToDeploy(currentTime) and not deployed:
            print("moving")
            s.changeAngle(180)
            deployed = True

        sensorLog.log(str(currentTime) + " s; ")
        logSensors(sensorLog, sensors)

        transmitData()

        print(currentTime)

        gps.update()
        if gps.hasNewData():
            pass#print(gps.getData())
        else:
            pass#print("no satelite fix")


def transmitData():
    pass

def readyToDeploy(currentTime):
    currentTime >= 10

def logSensors(sensorLog, sensors):
    sensorLog.log("Temp: {}; ".format(sensors.temp()))
    sensorLog.log("Accel: {}; ".format(sensors.accel()))
    sensorLog.log("Mag: {}; ".format(sensors.mag()))
    sensorLog.log("Gyro: {}; ".format(sensors.gyro()))
    sensorLog.log("Euler: {}; ".format(sensors.euler()))
    sensorLog.log("Quaternion: {}; ".format(sensors.quaternion()))
    sensorLog.log("Linear Accel: {}; ".format(sensors.linear_accel()))
    sensorLog.log("Gravity: {}; ".format(sensors.gravity()))
    sensorLog.logLine()


if "__main__" in __name__:
    main()
