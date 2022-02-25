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

        sensorLog.log("'time': '" + str(currentTime) + "', ")
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
    return currentTime >= 10

def logSensors(sensorLog, sensors):
    sensorLog.log("{")
    sensorLog.log("'temp': '{}', ".format(sensors.temp()))
    sensorLog.log("'accel': '{}', ".format(sensors.accel()))
    sensorLog.log("'mag': '{}', ".format(sensors.mag()))
    sensorLog.log("'gyro': '{}', ".format(sensors.gyro()))
    sensorLog.log("'euler': '{}', ".format(sensors.euler()))
    sensorLog.log("'quaternion': '{}', ".format(sensors.quaternion()))
    sensorLog.log("'linear Accel': '{}', ".format(sensors.linear_accel()))
    sensorLog.log("'gravity': '{}', ".format(sensors.gravity()))
    sensorLog.log("}")
    sensorLog.logLine()


if "__main__" in __name__:
    main()
