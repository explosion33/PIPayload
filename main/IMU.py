"""
Ethan Armstrong
warmst@uw.edu
implements IMU class and test method
"""
import board
import adafruit_bno055
import math
import time

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
        """
        IMU(i2c) | creates a new IMU object\n
        i2c | an adafruit board.I2C object, will create a new one if not provided
        """
        if not i2c:
            i2c = board.I2C()
        this.i2c = i2c
        this.sensor = adafruit_bno055.BNO055_I2C(i2c)
        this.lastTemp = 0xFFFF

        # inertial positioning vars
        this._velocity = [0,0,0]
        this._accel_pos = [0,0,0]

        this._c1 = None
        this._c2 = None
        this._c3 = None
        this._c4 = None
        this._c5 = None

        this._start = None
        this._last = 0

        this.hard_offset = (0,0,0)
        this._north_offset


    def _rotateZ(this, angle, accel):
        """
        rotateZ() | rotates vector about the z axis\n
        angle | (float) angle in radians to rotate by\n
        accel | ((float), (float), (float)) vector to rotate
        """
        x,y,z = accel
        r1 = (math.cos(angle) * x) + (-math.sin(angle) * y)
        r2 = (math.sin(angle) * x) + (math.cos(angle) * y)
        r3 = z

        return (r1,r2,r3)

    def _rotateY(this, angle, accel):
        """
        rotateY() | rotates vector about the y axis\n
        angle | (float) angle in radians to rotate by\n
        accel | ((float), (float), (float)) vector to rotate
        """
        x,y,z = accel
        r1 = (math.cos(angle) * x) + (math.sin(angle) * z)
        r2 = y
        r3 = (-math.sin(angle) * x) + (math.cos(angle) * z)

        return (r1,r2,r3)

    def _rotateX(this, angle, accel):
        """
        rotateX() | rotates vector about the x axis\n
        angle | (float) angle in radians to rotate by\n
        accel | ((float), (float), (float)) vector to rotate
        """
        x,y,z = accel
        r1 = x
        r2 = (math.cos(angle) * y) + (-math.sin(angle) * z)
        r3 = (math.sin(angle) * y) + (math.cos(angle) * z)

        return (r1,r2,r3)

    def _unRotateAccel(this, euler, accel):
        """
        unRotateAccel() | gets the original X,Y,Z components of a vector rotated in 3D\n
        euler | ((float), (float), (float)) angle the acceleration vector is rotates by in degrees
        accel | ((float), (float), (float)) rotated linear acceleration
        """
        euler = (euler[0]*math.pi/180,euler[1]*math.pi/180,euler[2]*math.pi/180)

        a = accel
        a = this._rotateZ(-euler[0], a)
        a = this._rotateY(-euler[1], a)
        a = this._rotateX(-euler[2], a)

        return a
    
    def inertialLoop(this):
        eulers = this.euler()
        accels = this.linear_accel()
        
        if eulers != (None, None, None) and accels != (None, None, None):
            # get elapsed time and delta time
            if this._start is None:
                this._start = time.time()

            t = time.time() - this._start
            dt = t - this._last
            this._last = t

            # Get acceleromter position data
            # rotate using orientation, truncate to 1 decimal place
            # rolling average with window size 5
            accels = this._unRotateAccel(eulers, accels)
            accels = (int(accels[0]*10)/10,int(accels[1]*10)/10,(int((accels[2] + 0.38)*10)/10))

            # hard coded rolling window is 35% faster than list representation
            # further analysis required to determine if this is nesesary
            # needs to run at 100Hz dt <= 0.01
            this._c5 = this._c4
            this._c4 = this._c3
            this._c3 = this._c2
            this._c2 = this._c1
            this._c1 = accels
            if this._c5 is not None:
                tot0 = this._c5[0]+this._c4[0]+this._c3[0]+this._c2[0]+this._c1[0]
                tot1 = this._c5[1]+this._c4[1]+this._c3[1]+this._c2[1]+this._c1[1]
                tot2 = this._c5[2]+this._c4[2]+this._c3[2]+this._c2[2]+this._c1[2]
                tot0 /= 5
                tot1 /= 5
                tot2 /= 5
                
                accels = (tot0,tot1,tot2)

                # additive integral for both velocity and pos
                this._velocity[0] += accels[0]*dt
                this._velocity[1] += accels[1]*dt
                this._velocity[2] += accels[2]*dt

                this._accel_pos[0] += this._velocity[0]*dt
                this._accel_pos[1] += this._velocity[1]*dt
                this._accel_pos[2] += this._velocity[2]*dt

    def getInertialPos(this):
        return (this._accel_pos[0], this._accel_pos[1], this._accel_pos[2])

    def updateInertialPos(this, pos):
        this._accel_pos[0] = pos[0]
        this._accel_pos[1] = pos[1]
        this._accel_pos[2] = pos[2]

    
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
        x,y,z = this.sensor.magnetic
        dx,dy,dz = this.hard_offset
        return (x+dx, y+dy, z+dz)

    def gyro(this):
        """gets gyroscape data in rad/sec"""
        return this.sensor.gyro

    def euler(this):
        """
        gets euler angle
        (z,y,x)
        """
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
    """
    while True:
        print("Temp: {}; ".format(sensors.temp()))
        print("Accel: {}; ".format(sensors.accel()))
        print("Mag: {}; ".format(sensors.mag()))
        print("Gyro: {}; ".format(sensors.gyro()))
        print("Euler: {}; ".format(sensors.euler()))
        print("Quaternion: {}; ".format(sensors.quaternion()))
        print("Linear Accel: {}; ".format(sensors.linear_accel()))
        print("Gravity: {}; ".format(sensors.gravity()))
    """

    while True:
        sensors.inertialLoop()
        print(sensors.getInertialPos())