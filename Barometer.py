import Adafruit_BMP.BMP085 as BMP085

class Barometer:
    def __init__(this) -> None:
        this.bmp = BMP085.BMP085()

        if not this.readCalibration():
            print("warning barometer has not been calibrated\ncalls to getAltitude() may not be accurate")
            #average sea level pressure
            this.baseHeight = 0
            this.basePressure = 1013.25

    def readCalibration(this):
        with open("TPTA.conf", "r") as f:
            base = f.readlines()
            if (len(base) < 2):
                return False
            this.baseHeight   = float(base[0].strip().replace("\n", ""))
            this.basePressure = float(base[1].strip().replace("\n", ""))
            
            print(this.baseHeight, this.basePressure)
        return True

    def calibrate(this, currentHeight):
        with open("TPTA.conf", "w") as f:
            f.write(str(currentHeight))
            f.write("\n")
            f.write(str(this.getPressure()))

    def getTemperature(this):
        return this.bmp.read_temperature()
    def getPressure(this):
        return this.bmp.read_pressure()
    def getAltitude(this):
        #uses the hypsometric formula
        P = this.getPressure()
        T = this.getTemperature() + 273.15 #C to Kelvin
        RATIO = 1.0/5.257
        RATIO2 = 0.0065

        return this.baseHeight + ((((this.basePressure/P)**RATIO)-1)*T)/RATIO2
    

if "__main__" in __name__:
    import time
    baro = Barometer()

    while True:
        print(str(baro.getAltitude()) +" m", str(baro.getPressure()) + " Pa", str(baro.getTemperature()) + " C")
        time.sleep(1)
