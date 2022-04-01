import board
import adafruit_bno055

class IMU:
    """
        a wrapper class to get bno055 sensor data\n
        has methods for:\n
        temp()\n
        accel()\n
        mag()\n
        gyro()\n
        euler()\n
        quaternion()\n
        linear_accel()\n
        gravity()\n
    """
    def __init__(this, i2c = None):
        if not i2c:
            i2c = board.I2C()
        this.i2c = i2c
        this.sensor = adafruit_bno055.BNO055_I2C(i2c)
        this.lastTemp = 0xFFFF
    
    def temp(this):
        """
        gets the current temperature in degrees Celcius
        """
        #special conversion for rpi? not sure
        result = this.sensor.temperature
        if abs(result - this.lastTemp) == 128:
            result = this.sensor.temperature
            if abs(result - this.last_val) == 128:
                return 0b00111111 & result
        last_val = result
        return result
    
    def accel(this):
        """gets acceleration in m/s^2"""
        return this.sensor.acceleration
    def mag(this):
        """gets magnometer data in microteslas"""
        return this.sensor.magnetic
    def gyro(this):
        """gets gyroscape data in rad/sec"""
        return this.sensor.gyro
    def euler(this):
        """gets euler angle"""
        return this.sensor.euler
    def quaternion(this):
        """gets quaternion"""
        return this.sensor.quaternion
    def linear_accel(this):
        """gets linear acceleration in m/s^2"""
        return this.sensor.linear_acceleration
    def gravity(this):
        """gets gravity in m/s^2"""
        return this.sensor.gravity

if "__main__" in __name__:
    sensors = IMU()
    while True:
        print("Temp: {}; ".format(sensors.temp()))
        print("Accel: {}; ".format(sensors.accel()))
        print("Mag: {}; ".format(sensors.mag()))
        print("Gyro: {}; ".format(sensors.gyro()))
        print("Euler: {}; ".format(sensors.euler()))
        print("Quaternion: {}; ".format(sensors.quaternion()))
        print("Linear Accel: {}; ".format(sensors.linear_accel()))
        print("Gravity: {}; ".format(sensors.gravity()))