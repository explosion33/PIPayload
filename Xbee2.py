#!/usr/bin/env python
import time
import os
import serial

from digi.xbee.devices import XBeeDevice, DigiMeshDevice, RemoteXBeeDevice, XBee64BitAddress
os.system("sudo systemctl stop serial-getty@serial0.service") # what does this do?



xBee = XBeeDevice("/dev/serial0", 9600)
xBee.open()
remote = RemoteXBeeDevice(xBee, XBee64BitAddress.from_hex_string("0013A20041C7BFD1")) #how does this work

while True:
    xBee.send_data(remote, "message")
    time.sleep(3)
