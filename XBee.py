#!/usr/bin/env python
import time
import os
import serial

from digi.xbee.devices import XBeeDevice, DigiMeshDevice, RemoteXBeeDevice, XBee64BitAddress
os.system("sudo systemctl stop serial-getty@serial0.service") # what does this do?



receiver = XBeeDevice("/dev/serial0", 9600)
receiver.open()
remote_device = RemoteXBeeDevice(receiver, XBee64BitAddress.from_hex_string("0013A20041C7BFD1")) #how does this work

#xbee.send_data(remote_device, "message")

while True:
    data_variable = receiver.read_data_from(remote_device)
    
    if(data_variable is None):
        print('No Data Found')
    else:
        print(data_variable.data.decode("utf-8"))
        print(data_variable.timestamp)
        print("============================")
        print()
    time.sleep(3)

receiver.close()