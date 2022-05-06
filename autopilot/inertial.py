"""
TODO
Implement some Calibration
    based on tests the first ~10 data points are invalid
    if we skip these, then take ~100 data points and average there offset from zero
    we can get a calibration assuming a stable enviroment

Implement Rotation Matrix
    sensors.euler()
    use the current orientation to calculate the position from a stationary reference frame

    from Wolfram
    D (first euler angle)
    |  cos sin 0 |
    | -sin cos 0 |
    |  0    0  1 |

    C (second euler angle)
    | 1   0   0  |
    | 0  cos sin |
    | 0 -sin cos |

    B (third euler angle)
    |  cos sin 0 |
    | -sin cos 0 |
    |   0   0  1 |

    I believe we can plug the corresponding angle (D,C,B) into each matrix,
    then multiply the inverse of the matrix by our acceleration vector to get the actual vector

    the inverse is given by
    adjoint(A) / determinate(A)


Implement simpler additive integral
    store a speed variable, starts at 0
    store a pos variable, starts at 0
    every frame grab transformed acceleration
    increment speed by accel*dt
    increment pos by speed*dt

Ensure Delta Time (dt) is less than 0.01 for all calculations always
    the adafruit 9dof records information at 100hZ, if our inertial positioning loop takes longer than this time
    we will have lost some data
    
    this class can be made to run in a seperate process and use shared memory to keep track of acurate position,
    even when the main controller is doing something else
"""

import time
import math
from filter_tools import integrate, movingAverage, getNoisyAcceleration, getAcceleration



def rotateZ(angle, accel):
    x,y,z = accel
    # D
    """
    |  cos sin 0 |
    | -sin cos 0 |
    |  0    0  1 |
    """
    r1 = (math.cos(angle) * x) + (-math.sin(angle) * y)
    r2 = (math.sin(angle) * x) + (math.cos(angle) * y)
    r3 = z

    return (r1,r2,r3)

def rotateY(angle, accel):
    x,y,z = accel
    # C
    """
    | 1   0   0  |
    | 0  cos sin |
    | 0 -sin cos |
    """
    r1 = (math.cos(angle) * x) + (math.sin(angle) * z)
    r2 = y
    r3 = (-math.sin(angle) * x) + (math.cos(angle) * z)

    return (r1,r2,r3)

def rotateX(angle, accel):
    x,y,z = accel
    # B
    """
    |  cos sin 0 |
    | -sin cos 0 |
    |  0    0  1 |
    """
    r1 = x
    r2 = (math.cos(angle) * y) + (-math.sin(angle) * z)
    r3 = (math.sin(angle) * y) + (math.cos(angle) * z)

    return (r1,r2,r3)

def unRotateAccel(euler, accel):
    euler = (euler[0]*math.pi/180,euler[1]*math.pi/180,euler[2]*math.pi/180)

    a = accel
    a = rotateZ(-euler[0], a)
    a = rotateY(-euler[1], a)
    a = rotateX(-euler[2], a)

    return a

def trunc(n,d):
    m = 10**d
    return int(n*m)/m
    

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
            t = time.time() - start
            dt = t - last
            last = t

            # Get acceleromter position data
            # rotate using orientation, truncate to 1 decimal place
            # rolling average with window size 5
            accels = unRotateAccel(eulers, accels)
            accels = (int(accels[0]*10)/10,int(accels[1]*10)/10,(int((accels[2] + 0.38)*10)/10))

            num_accel_readings += 1

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

            
                velocity[0] += accels[0]*dt
                velocity[1] += accels[1]*dt
                velocity[2] += accels[2]*dt

                accel_pos[0] += velocity[0]*dt
                accel_pos[1] += velocity[1]*dt
                accel_pos[2] += velocity[2]*dt


            baro_pos = baro.getAltitude()


            mix = 0.7 # 80% acceleromter
            position = (baro_pos*(1-mix)) + (accel_pos[1]*mix)

            
                


            #print(accels, dt)
            print(int(position), accel_pos[1], baro_pos)
            
            accel_pos[1] = position
            
            


        


