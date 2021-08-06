import serial
import time
import struct

class SX1276:

    READ = bytes("rr", 'utf-8')
    WRITE = bytes("wr", 'utf-8')
    TRANSMIT = bytes("tx", 'utf-8')
    RECEIVE = bytes("rx", 'utf-8')

    # READ = "rr"
    # WRITE = "wr"
    # TRANSMIT = "tx"
    # RECEIVE = "rx"

    def __init__(self, port_name):
        self.arduino = serial.Serial(port=port_name, baudrate=115200, timeout=1)
    
    # def set_bandwidth(self, bandwidth):
    #     reg = '0x1D'
    #     command = self.construct_command(SX1276.WRITE, reg, bandwidth)
    #     self.send_command(command)
    
    # # Transmit of Receive
    # def construct_command(self, transmit_or_receive, packet):
    #     return transmit_or_receive + packet
    
    # # Read or Write Register
    # def construct_command(self, write_or_read, register, value):
    #     return write_or_read + register + value

    def set_bandwidth(self, bandwidth):
        bandwidth_to_value = {7.8 : 0b0000,
                             10.4 : 0b0001,
                             15.6 : 0b0010,
                             20.8 : 0b0011,
                            31.25 : 0b0100,
                             41.7 : 0b0101,
                             62.5 : 0b0110,
                              125 : 0b0111,
                              250 : 0b1000,
                              500 : 0b1001 }
        value = bandwidth_to_value[bandwidth] * 0b1000 + 0b0010
        reg = 0x1D
        command = self.construct_command(SX1276.WRITE, reg, value)
        self.send_command(command)
    
    def set_spreading_factor(self, sf):
        sf_to_value = {64 : 6,
                      128 : 7,
                      256 : 8,
                      512 : 9,
                     1024 : 10,
                     2048 : 11,
                     4096 : 12}
        reg = 0x1E
        command = self.construct_command(SX1276.WRITE, reg, sf)
        self.send_command(command)
    
    # Transmit of Receive
    def construct_command(self, transmit_or_receive, packet):
        return struct.pack("siii", transmit_or_receive, packet)
    
    # Read or Write Register
    def construct_command(self, write_or_read, register, value):
        return struct.pack("siii", write_or_read, register, value)
    
    def send_command(self, command):
        self.arduino.write(bytes(command, 'utf-8'))
    
    def get_response(self):
        while True:
            response = self.arduino.readline().decode('utf-8')
            if response:
                print(response)
                break;

sx1276 = SX1276('/dev/tty.usbmodem14401')
time.sleep(1.7)

# sx1276.send_command("test 1")
# sx1276.get_response()

# sx1276.send_command("test 2")
# sx1276.get_response()

sx1276.set_bandwidth(7.8)
sx1276.get_response()

sx1276.set_spreading_factor(0b1000000)
sx1276.get_response()

# sx1276.set_bandwidth("0b10011001")
# sx1276.get_response()

