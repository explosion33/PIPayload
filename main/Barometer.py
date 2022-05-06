"""
Ethan Armstrong
warmst@uw.edu
Implements the Barmoter class as well as test functionality
"""
import Adafruit_BMP.BMP085 as BMP085

class Barometer:
    """
    Baromter object acts as an interface for a connected adafruit bno055 (9dof) IMU breakout board
    """
    def __init__(this) -> None:
        """
        Baromter() | creates a new Baromter object
        """
        this.bmp = BMP085.BMP085()

        #check for saved altitude calibration in TPTA.conf, if not use SPT
        if not this.readCalibration():
            print("warning barometer has not been calibrated\ncalls to getAltitude() may not be accurate")
            #average sea level pressure
            this.baseHeight = 0
            this.basePressure = 1013.25

    def readCalibration(this):
        """
        readCalibration() | reads a calibration file "TPTA.conf" for stored calibration values
        """

        with open("TPTA.conf", "r") as f:
            base = f.readlines()
            if (len(base) < 2):
                return False
            this.baseHeight   = float(base[0].strip().replace("\n", ""))
            this.basePressure = float(base[1].strip().replace("\n", ""))

            print(this.baseHeight, this.basePressure)
            
        return True

    def calibrate(this, currentHeight):
        """
        calibrate(currentHeight) | calibrates the sensor for a given location\n
        currentHeight | (float) current known altitude
        """
        with open("TPTA.conf", "w") as f:
            f.write(str(currentHeight))
            f.write("\n")
            f.write(str(this.getPressure()))

    def getTemperature(this):
        """
        getTemperature() | gets temperature\n
        returns : (float) C
        """
        return this.bmp.read_temperature()

    def getPressure(this):
        """
        getPressure() | gets current pressure\n
        returns : (float) Pa
        """
        return this.bmp.read_pressure()

    def getAltitude(this):
        """
        getAltitude() | gets current altitude\n
        returns : (float) meters
        """
        #use the hypsometric formula to calculate altitude from temp and pressure
        P = this.getPressure()
        T = this.getTemperature() + 273.15 #C to Kelvin
        RATIO = 1.0/5.257
        RATIO2 = 0.0065

        return this.baseHeight + ((((this.basePressure/P)**RATIO)-1)*T)/RATIO2
    

if "__main__" in __name__:
    import time
    baro = Barometer()

    last = time.time()

    c1,c2,c3,c4,c5=None

    while True:
        #print(str(baro.getAltitude()) +" m", str(baro.getPressure()) + " Pa", str(baro.getTemperature()) + " C")

        # rolling window of length 5, without having to use list or for loop
        c5 = c4
        c4 = c3
        c3 = c2
        c3 = c1
        c1 = baro.getAltitude()
        if c5 is not None:
            dt = last - time.time()
            tot = c5+c4+c3+c2+c1
            tot /= 5
            print(dt, tot)
        

