from IMU import IMU
import time

sensors = IMU()
time.sleep(2)


mag_x, mag_y, mag_z = sensors.mag()

min_x = max_x = mag_x
min_y = max_y = mag_y
min_z = max_z = mag_z

while True:
    mag_x, mag_y, mag_z = sensors.mag()

    min_x = min(min_x, mag_x)
    min_y = min(min_y, mag_y)
    min_z = min(min_z, mag_z)

    max_x = max(max_x, mag_x)
    max_y = max(max_y, mag_y)
    max_z = max(max_z, mag_z)

    offset_x = (max_x + min_x) / 2
    offset_y = (max_y + min_y) / 2
    offset_z = (max_z + min_z) / 2

    print(
            "Hard Offset:  X: {0:8.2f}, Y:{1:8.2f}, Z:{2:8.2f} uT".format(
                offset_x, offset_y, offset_z
            )
        )