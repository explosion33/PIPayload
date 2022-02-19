from digi.xbee.devices import DigiMeshDevice, RemoteDigiMeshDevice, XBee64BitAddress
 

device = DigiMeshDevice("/dev/serial0", 9600)
device.open()

remote_device = RemoteDigiMeshDevice(device, XBee64BitAddress.from_hex_string("13A20041C7BFFC"))

while True:
    device.send_data(remote_device, "test data")