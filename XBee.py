from digi.xbee.devices import DigiPointDevice, RemoteDigiPointDevice, XBee64BitAddress
 

#transmitting XBee should be in coordinader mode
#should be set to API mode aswell

#reciever should be in router mode
#can be either API or AT depending on if using XTCU or python API


#make sure to scan for device, using portscan.sh script to get the right /dev/...
device = DigiPointDevice("/dev/serial0", 9600)
device.open()

remote_device = RemoteDigiPointDevice(device, XBee64BitAddress.from_hex_string("13A20041C7BFFC")) #MAC adress of other Xbee

while True:
    device.send_data(remote_device, "test data")