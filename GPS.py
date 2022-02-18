import time
import board
import busio
import adafruit_gps
import serial

class GPS:
    def __init__(this):
        this.uart = serial.Serial("/dev/serial0", baudrate=9600, timeout=10)
        this.gps = adafruit_gps.GPS(this.uart, debug=False) # Use UART/pyserial

        # Turn on the basic GGA and RMC info (what you typically want)
        this.gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

        # Set update rate to once a second (1hz) which is what you typically want.
        this.gps.send_command(b"PMTK220,1000")

        this.updated = False

        this.data = {
            "time": {
                "month"  : None,
                "day"    : None,
                "year"   : None,
                "hour"   : None,
                "minute" : None,
                "second" : None,
            },

            "latitude"   : None,
            "longitude"  : None,
            "quality"    : None,
            "satellites" : None,
            "altitude"   : None,
            "speed"      : None,
        }

    def update(this):
        hasNewData = this.gps.update()
        print(hasNewData, this.gps.has_fix)
        if this.gps.has_fix:
            this.updated = True

            this.data["time"]["month"]  = this.gps.timestamp_utc.tm_mon, # Grab parts of the time from the
            this.data["time"]["day"]    = this.gps.timestamp_utc.tm_mday, # struct_time object that holds
            this.data["time"]["year"]   = this.gps.timestamp_utc.tm_year, # the fix time. Note you might
            this.data["time"]["hour"]   = this.gps.timestamp_utc.tm_hour, # not get all data like year, day,
            this.data["time"]["minute"] = this.gps.timestamp_utc.tm_min, # month!
            this.data["time"]["second"] = this.gps.timestamp_utc.tm_sec,

            this.data["quality"]   = this.gps.fix_quality
            this.data["latitude"]  = this.gps.latitude
            this.data["logintude"] = this.gps.longitude
            

            if this.gps.satellites:
                this.data["satellites"] = this.gps.satellites
            if this.gps.altitude_m:
                this.data["altitude"] = this.gps.altitude_m
            if this.gps.speed_knots:
                this.data["speed"] = this.gps.speed_knots


    def getData(this):
        this.updated = False
        return this.data

    def hasNewData(this):
        return this.updated


if "__main__" in __name__:
    gps = GPS()
    while True:
        gps.update()
        if gps.hasNewData():
            print(gps.getData())
        else:
            print("no satelite fix")
        time.sleep(1)