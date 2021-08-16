import serial
import time
import struct

class SX1276:

    READ = "rr"
    WRITE = "wr"
    TRANSMIT = "tx"
    RECEIVE = "rx"

    # READ = bytes("rr", 'utf-8')
    # WRITE = bytes("w", 'utf-8')
    # TRANSMIT = bytes("tx", 'utf-8')
    # RECEIVE = bytes("rx", 'utf-8')

    def __init__(self, port_name):
        self.arduino = serial.Serial(port=port_name, baudrate=115200, timeout=1)
    
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
        # error coding rate: 4/5
        # explicit header mode
        value = str(bandwidth_to_value[bandwidth] * 0b10000 + 0b0010)
        print('Setting Bandwidth to', bandwidth)
        reg = str(0x1D)
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
        # normal mode
        # crc disable
        # RX timeout MSB
        value = str(sf_to_value[sf] * 0b10000 + 0b0000)
        print('Setting Spreading Factor to', sf)
        reg = str(0x1E)
        command = self.construct_command(SX1276.WRITE, reg, value)
        self.send_command(command)
    
    # Transmit of Receive
    def construct_command(self, transmit_or_receive, packet):
        return transmit_or_receive + packet
    
    # Read or Write Register
    def construct_command(self, write_or_read, register, value):
        return write_or_read + " " + register + " " + value + " "

    def send_command(self, command):
        print('command: ' + command)
        self.arduino.write(bytes(command, 'utf-8'))

    def get_response(self):
        response = self.arduino.readline().decode('utf-8')
        print(response)
        print('\n')


    # def set_bandwidth(self, bandwidth):
    #     bandwidth_to_value = {7.8 : 0b0000,
    #                         10.4 : 0b0001,
    #                         15.6 : 0b0010,
    #                         20.8 : 0b0011,
    #                         31.25 : 0b0100,
    #                         41.7 : 0b0101,
    #                         62.5 : 0b0110,
    #                         125 : 0b0111,
    #                         250 : 0b1000,
    #                         500 : 0b1001 }
    #     # error coding rate: 4/5
    #     # explicit header mode
    #     value = bandwidth_to_value[bandwidth] * 0b10000 + 0b0010
    #     reg = 0x1D
    #     print('Setting Bandwidth to', bandwidth_to_value[bandwidth])
    #     command = self.construct_command(SX1276.WRITE, reg, value)
    #     self.send_command(command)
    
    # def set_spreading_factor(self, sf):
    #     sf_to_value = {64 : 6,
    #                 128 : 7,
    #                 256 : 8,
    #                 512 : 9,
    #                 1024 : 10,
    #                 2048 : 11,
    #                 4096 : 12}
    #     # normal mode
    #     # crc disable
    #     # RX timeout MSB
    #     value = sf_to_value[sf] * 0b10000 + 0b0000
    #     reg = 0x1E
    #     command = self.construct_command(SX1276.WRITE, reg, value)
    #     self.send_command(command)
    
    # # Transmit of Receive
    # def construct_command(self, transmit_or_receive, packet):
    #     return struct.pack("ci", transmit_or_receive, packet)
    
    # # Read or Write Register
    # def construct_command(self, write_or_read, register, value):
    #     print('command:', write_or_read, register, value)
    #     return struct.pack("cii", write_or_read, register, value)
    
    # def send_command(self, command):
    #     print('command:', command)
    #     self.arduino.write(command)
    
    # def get_response(self):
    #     # response = self.arduino.readline().decode('utf-8')
    #     response = self.arduino.readline()
    #     print(response)
    #     print()

sx1276 = SX1276('/dev/tty.usbmodem14301')
time.sleep(1.7)

sx1276.set_bandwidth(500)
sx1276.get_response()

sx1276.set_spreading_factor(4096)
sx1276.get_response()



