from digi.xbee.devices import DigiPointDevice, RemoteDigiPointDevice, XBee64BitAddress
 
class reciever:
    def __init__(this, PORT, BAUD, MAC_REMOTE):
        this.device = DigiPointDevice(PORT, BAUD)
        this.device.open()

        this.remote_device = RemoteDigiPointDevice(device, XBee64BitAddress.from_hex_string(MAC_REMOTE))
    
    def parseMessage(this, msg):
        return msg
    
    def check_for_message(this):
        msg = this.device.read_expl_data_from(this.remote_device)
        if msg:
            return this.parseMessage(msg)
        return None


if "__main__" in __name__:
    PORT = "COM2"
    BAUD = 9600
    MAC  = "13A20041C7BFFC"

    r = reciever(PORT, BAUD, MAC)
    
    while True:
        msg = r.check_for_message()
        if msg:
            print(msg)
