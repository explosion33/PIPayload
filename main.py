import time
from IMU import IMU
from Logger import Logger
from Camera import Camera
from Servo import Servo2


def main():
    sensors = IMU()
    sensorLog = Logger("sensors.log")

    s = Servo2(11,50,0)
    s.setAngle(0)

    c = Camera((640,480))
    c.startCamera('my_video.h264')
    
    while True:
        if readyToDeploy():
            s.setAngle(180)

        sensorLog.log(time.time())
        logSensors(sensorLog, sensors)

        transmitData()

        time.sleep(1)


def transmitData():
    pass

def readyToDeploy():
    time.time(10)

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
    main(True)
