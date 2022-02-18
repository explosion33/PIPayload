#!/usr/bin/env python
import time
import serial

ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1             
 )
counter=0       

#reads until /n
def read(ser):
    data = ser.readline().strip()
    print(data)

def write(ser, message):
    ser.write(str.encode(str(message)))

while True:
    #read(ser)
    write(ser, "test data")
