import time
from IMU import IMU
from Logger import Logger

def main(console):
    sensors = IMU()
    sensorLog = Logger("sensors.log")
    
    while True:
        sensorLog.log("Temp: {}; ".format(sensors.temp()))
        sensorLog.log("Accel: {}; ".format(sensors.accel()))
        sensorLog.log("Mag: {}; ".format(sensors.mag()))
        sensorLog.log("Gyro: {}; ".format(sensors.gyro()))
        sensorLog.log("Euler: {}; ".format(sensors.euler()))
        sensorLog.log("Quaternion: {}; ".format(sensors.quaternion()))
        sensorLog.log("Linear Accel: {}; ".format(sensors.linear_accel()))
        sensorLog.log("Gravity: {}; ".format(sensors.gravity()))
        sensorLog.logLine()

        if console:
            logToConsole(sensors)

        time.sleep(1)


def logToConsole(sensors) -> None:
    print("Temperature: {} degrees C".format(sensors.temp()))
    print("Accelerometer (m/s^2): {}".format(sensors.accel()))
    print("Magnetometer (microteslas): {}".format(sensors.mag()))
    print("Gyroscope (rad/sec): {}".format(sensors.gyro()))
    print("Euler angle: {}".format(sensors.euler()))
    print("Quaternion: {}".format(sensors.quaternion()))
    print("Linear acceleratison (m/s^2): {}".format(sensors.linear_accel()))
    print("Gravity (m/s^2): {}".format(sensors.gravity()))
    print()

if "__main__" in __name__:
    main(True)
