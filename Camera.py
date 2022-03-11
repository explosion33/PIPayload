import picamera
from multiprocessing import Process, Queue

class Camera:
    def __init__(this, resolution):
        this.camera = picamera.PiCamera()
        this.camera.resolution = resolution

    def startCamera(this, name):
        this.camera.start_recording(name)

    def startCameraTask(this, resolution, name) -> Process:
        """
        startCameraTask(resolution) : starts camera recording in a background process
        resolution : tuple (w,h) resolution to record in
        name       : String, name of video + exstension
        returns : Process
        """

        p = Process(target=this.camera.start_recording, args=(name,))
        p.start()
        this.process = p
    
    def stopCamera(this):
        this.camera.stop_recording()




# successful test of this code would be to observe 0-10 printed to console, then after the the
# program closes find an 11 second long file.
if "__main__" in __name__:
    import time
    c = Camera((640,480))
    c.startCamera('my_video.h264')

    i = 0
    while i<=10:
        print(i)
        i += 1
        time.sleep(1)
    c.stopCamera()