"""
Ethan Armstrong
warmst@uw.edu
Implements GPS class
"""
import time
import board
import busio
import adafruit_gps
import serial

class GPS:
    """
    GPS interface to read and format gps data from an adafruit ultimate GPS breakout
    """
    def __init__(this):
        """
        GPS() | creates a new GPS object
        """
        this.uart = serial.Serial("/dev/serial0", baudrate=9600, timeout=10)
        this.gps = adafruit_gps.GPS(this.uart, debug=False) # Use UART/pyserial

        # Turn on the basic GGA and RMC info (what you typically want)
        this.gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

        # Set update rate to 1/10 second (0.1hz) which is what you typically want.
        this.gps.send_command(b"PMTK220,2000")

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

        this.flag = False

    def update(this):
        """
        update() | updates stored gps data if new data is available
        """
        hasNewData = this.gps.update()

        if hasNewData and this.flag: # this.gps.has_fix:
            this.updated = True

            this.data["time"]["month"]  = this.gps.timestamp_utc.tm_mon, # Grab parts of the time from the
            this.data["time"]["day"]    = this.gps.timestamp_utc.tm_mday, # struct_time object that holds
            this.data["time"]["year"]   = this.gps.timestamp_utc.tm_year, # the fix time. Note you might
            this.data["time"]["hour"]   = this.gps.timestamp_utc.tm_hour, # not get all data like year, day,
            this.data["time"]["minute"] = this.gps.timestamp_utc.tm_min, # month!
            this.data["time"]["second"] = this.gps.timestamp_utc.tm_sec,

            this.data["quality"]   = this.gps.fix_quality
            this.data["latitude"]  = this.gps.latitude
            this.data["longitude"] = this.gps.longitude
            

            #if this.gps.satellites:
            this.data["satellites"] = this.gps.satellites
            #if this.gps.altitude_m:
            this.data["altitude"] = this.gps.altitude_m
            #if this.gps.speed_knots:
            this.data["speed"] = this.gps.speed_knots

        this.flag = True


    def getData(this):
        """
        getData() | gets most recent gps data
        """
        this.updated = False
        return this.data

    def hasNewData(this):
        """
        hasNewData() | checks for new data\n
        returns : True if there is data that has not been retrieved with getData(), False otherwise
        """
        return this.updated

    def hasFix(this):
        return this.gps.has_fix


if "__main__" in __name__:
    start_pos = (None,None)
    gps = GPS()
    while True:
        gps.update()
        if gps.hasNewData():
            data = gps.getData()

            if start_pos == (None, None):
                start_pos = (data["latitude"], data["longitude"])

            driftX = start_pos[0] - data["latitude"]
            driftY = start_pos[1] - data["longitude"]
            print(driftX*111139, driftY*111139, data["altitude"], data["satellites"], data["time"]["second"])
        elif not gps.hasFix():
            print("no fix")

        time.sleep(0.5)