import time
import math


def rotateZ(angle, accel):
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

def rotateY(angle, accel):
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

def rotateX(angle, accel):
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

def unRotateAccel(euler, accel):
    """
    unRotateAccel() | gets the original X,Y,Z components of a vector rotated in 3D\n
    euler | ((float), (float), (float)) angle the acceleration vector is rotates by in degrees
    accel | ((float), (float), (float)) rotated linear acceleration
    """
    euler = (euler[0]*math.pi/180,euler[1]*math.pi/180,euler[2]*math.pi/180)

    a = accel
    a = rotateZ(-euler[0], a)
    a = rotateY(-euler[1], a)
    a = rotateX(-euler[2], a)

    return a
    

if "__main__" in __name__:
    from IMU import IMU
    from Barometer import Barometer
    
    
    baro = Barometer()
    sensors = IMU()

    start = time.time()
    last = 0

    velocity = [0,0,0]
    accel_pos = [0,0,0]

    c1,c2,c3,c4,c5=(None,None,None,None,None)
    num_accel_readings = 0

    while True:
        eulers = sensors.euler()
        accels = sensors.linear_accel()
        if eulers != (None, None, None) and accels != (None, None, None):
            # get elapsed time and delta time
            t = time.time() - start
            dt = t - last
            last = t

            # Get acceleromter position data
            # rotate using orientation, truncate to 1 decimal place
            # rolling average with window size 5
            accels = unRotateAccel(eulers, accels)
            accels = (int(accels[0]*10)/10,int(accels[1]*10)/10,(int((accels[2] + 0.38)*10)/10))

            num_accel_readings += 1

            # hard coded rolling window is 35% faster than list representation
            # further analysis required to determine if this is nesesary
            # needs to run at 100Hz dt <= 0.01
            c5 = c4
            c4 = c3
            c3 = c2
            c2 = c1
            c1 = accels
            if c5 is not None:
                tot0 = c5[0]+c4[0]+c3[0]+c2[0]+c1[0]
                tot1 = c5[1]+c4[1]+c3[1]+c2[1]+c1[1]
                tot2 = c5[2]+c4[2]+c3[2]+c2[2]+c1[2]
                tot0 /= 5
                tot1 /= 5
                tot2 /= 5
                
                accels = (tot0,tot1,tot2)

                # additive integral for both velocity and pos
                velocity[0] += accels[0]*dt
                velocity[1] += accels[1]*dt
                velocity[2] += accels[2]*dt

                accel_pos[0] += velocity[0]*dt
                accel_pos[1] += velocity[1]*dt
                accel_pos[2] += velocity[2]*dt




            baro_pos = baro.getAltitude()


            mix = 0.5 # 70% acceleromter
            position_y = (baro_pos*(1-mix)) + (accel_pos[1]*mix)
            position_y = round(position_y,2)

            
            #print(accels, dt)
            
            accel_pos[0] = round(accel_pos[0],2)
            accel_pos[1] = position_y
            accel_pos[2] = round(accel_pos[2],2)

            print(accel_pos[0], ("+" if position_y >= 0 else "") + str(position_y), accel_pos[2])
            
