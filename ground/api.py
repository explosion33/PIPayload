from flask import Flask, render_template, flash, redirect, request, url_for, jsonify
from multiprocessing import Process, Queue
from xBee_recieve import reciever


app = Flask(__name__)

processes = []
collectedData = []

def getNewXbeeData(q):
    PORT = "COM2"
    BAUD = 9600
    MAC  = "13A20041C7BFFC"

    r = reciever(PORT, BAUD, MAC)

    while True:
        msg = r.check_for_message()
        if msg:
            q.put(msg) # data needs to first be parsed, so if the msg is a json, we need to format to [msg['x'], msg['y']]

#tester method to get generated data should function the same as getNewXbeeData
def getNewRandomData(q):
    """
    temp()\n
    accel()\n
    mag()\n
    gyro()\n
    euler()\n
    quaternion()\n
    linear_accel()\n
    gravity()\n
    """
    import time
    from random import randint

    t = 0
    lastAccel = [0,0,0]
    while True:
        r = randint(5,10)/10.0
        print(r)
        time.sleep(r)
        t += r

        data = {
            "time"  : t,
            "accel" : [lastAccel[0] + randint(-20,20),lastAccel[1] + randint(-20,20),lastAccel[2] + randint(-20,20)],
            "gyro"  : [randint(-20,20),randint(-20,20),randint(-20,20)],
            "temp"  : randint(30,100), 
            }
        q.put(data)

        lastAccel = data["accel"]

    
@app.route("/", methods=["GET", ])
def main():
    return render_template("main.html")

#main page
@app.route('/api/<data>/<num>', methods=['GET'])
def api(data, num):
    q = processes[0][0]

    while not q.empty():
        d = q.get()
        collectedData.append(d)

    #num is current size of users data, so we only give them the data they dont have
    out = []
    if "accel" in data:
        n = 0
        if "Y" in data:
            n = 1
        elif "Z" in data:
            n = 2

        for d in collectedData[int(num)::]:
            out.append([d["time"], d["accel"][n]])

    elif "gyro" in data:
        n = 0
        if "Y" in data:
            n = 1
        elif "Z" in data:
            n = 2

        for d in collectedData[int(num)::]:
            out.append([d["time"], d["gyro"][n]])

    elif data == "temp":
        for d in collectedData[int(num)::]:
            out.append([d["time"], d["temp"]])

    return jsonify(out)



if __name__ == '__main__':
    q = Queue()
    p = Process(target=getNewRandomData, args=[q,])
    processes.append((q,p))
    p.start()

    app.run(host="0.0.0.0", port=80)
    for p in processes:
        p[1].terminate()