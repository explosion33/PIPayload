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
            print(msg)
            q.put(msg) # data needs to first be parsed, so if the msg is a json, we need to format to [msg['x'], msg['y']]

#tester method to get generated data should function the same as getNewXbeeData
def getNewRandomData(q):
    import time
    from random import randint

    t = 0
    while True:
        r = randint(0,1)+0.5
        time.sleep(r)
        t += r

        data = [t, randint(-20,20)]
        q.put(data)

    
@app.route("/", methods=["GET", ])
def main():
    return render_template("main.html")

#main page
@app.route('/getData<num>', methods=['GET'])
def data1(num):
    q = processes[0][0]

    while not q.empty():
        d = q.get()
        collectedData.append(d)

    #num is current size of users data, so we only give them the data they dont have
    print(len(collectedData))
    return jsonify(collectedData[int(num)::])



if __name__ == '__main__':
    q = Queue()
    p = Process(target=getNewRandomData, args=[q,])
    processes.append((q,p))
    p.start()

    app.run(host="0.0.0.0", port=80)