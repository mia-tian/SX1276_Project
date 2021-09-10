import serial
import time

class SX1276:

    READ = "rr"
    WRITE = "wr"
    TRANSMIT = "tx"
    RECEIVE = "rx"
    MSG_END = "\r"

    def __init__(self, port_name):
        self.arduino = serial.Serial(port=port_name, baudrate=115200, timeout=1)

    
    def set_bandwidth(self, bandwidth, coding_rate):
        '''
        sets bandwidth (kHz) of to 7.8, 10.4, 15.6, 20.8, 31.25, 41.7, 62.5, 125, 250, or 500
        sets coding rate to 4/5, 4/6, 4/7, or 4/8
        sets explicit header mode
        example function call: set_bandwidth(7.8, '4/5')
        '''
        print('Setting Bandwidth to', bandwidth, 'kHz, and coding rate to', coding_rate)

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

        coding_rate_to_value = {'4/5' : 0b001,
                                '4/6' : 0b010,
                                '4/7' : 0b011,
                                '4/8' : 0b100 }
        
        try:
            value = str((bandwidth_to_value[bandwidth] << 4) + (coding_rate_to_value[coding_rate] << 1) + 0b0)
            reg = str(0x1D)
            command = self.construct_command_write(SX1276.WRITE, reg, value)
            self.send_command(command)
        except KeyError:
            print('Unsucessful: invalid bandwidth or coding rate\n')

    
    def set_spreading_factor(self, sf):
        '''
        sets spreading factor (chips/symbol) to 64, 128, 256, 512, 1024, 2048, 4096
        sets normal mode- a single packet is sent
        CRC enable 
        default SymbTimeout
        example function call: set_spreading_factor(64)
        '''
        print('Setting Spreading Factor to', sf, "chips/symbol")

        sf_to_value = {64 : 6,
                    128 : 7,
                    256 : 8,
                    512 : 9,
                    1024 : 10,
                    2048 : 11,
                    4096 : 12}
        
        try:
            value = str((sf_to_value[sf] << 4) + 0b0100)
            reg = str(0x1E)
            command = self.construct_command_write(SX1276.WRITE, reg, value)
            self.send_command(command)
        except KeyError:
            print('Unsucessful: invalid spreading factor\n')

    def set_transmit_power(self, Pout):
        '''
        sets PA output pin to RFO pin
        sets MaxPower and OutputPower 
        example function call: set_transmit_power(10.2)
        '''
        print('Setting Transmitted Power to', Pout, 'dBm')

        # brute force method to find MaxPower and OutputPower
        min_dist = float('inf')
        for MaxPower in range(9):
            Pmax = 10.8 + (.6 * MaxPower)
            for OutputPower in range(17):
                calc_Pout = Pmax - (15 - OutputPower)
                if abs(calc_Pout - Pout) < min_dist:
                    min_dist = abs(calc_Pout - Pout)
                    MaxPower_best = MaxPower
                    OutputPower_best = OutputPower
                    Pout_best = calc_Pout

        print('Closest Pout:', Pout_best, ', MaxPower:', MaxPower_best, ', OutputPower:', OutputPower_best)
        value = str(int((0x00 << 7) + (MaxPower_best << 4) + OutputPower_best))
        reg = str(0x09)
        command = self.construct_command_write(SX1276.WRITE, reg, value)
        self.send_command(command)
    
    def read_register(self, reg):
        command = self.construct_command_read(SX1276.READ, str(reg))
        self.send_command(command)
    
    # Transmit of Receive
    def construct_command(self, transmit_or_receive, packet):
        return transmit_or_receive + packet
    
    # Read or Write Register
    def construct_command_write(self, write_or_read, register, value):
        return write_or_read + " " + register + " " + value + " " + SX1276.MSG_END
    
    def construct_command_read(self, write_or_read, register):
        return write_or_read + " " + register + " " + SX1276.MSG_END

    def send_command(self, command):
        print('command: ' + command)
        self.arduino.flush()
        self.arduino.write(bytes(command, 'utf-8'))
        self.get_response()

    def get_response(self):
        time.sleep(.1)
        response = self.arduino.read_until(b"\r").decode('utf-8')
        self.arduino.reset_output_buffer()
        # response = self.arduino.readline().decode('utf-8')
        print(response)
        print()


sx1276 = SX1276('/dev/tty.usbmodem14401')
time.sleep(1.7)

sx1276.set_bandwidth(500, '4/6')

sx1276.set_spreading_factor(4096)

sx1276.set_transmit_power(10)

sx1276.read_register(0x1E)


# class SX1276:

#     READ = bytes("rr", 'utf-8')
#     WRITE = bytes("w", 'utf-8')
#     TRANSMIT = bytes("tx", 'utf-8')
#     RECEIVE = bytes("rx", 'utf-8')

#     def __init__(self, port_name):
#         self.arduino = serial.Serial(port=port_name, baudrate=115200, timeout=1)

#     def set_bandwidth(self, bandwidth):
#         bandwidth_to_value = {7.8 : 0b0000,
#                             10.4 : 0b0001,
#                             15.6 : 0b0010,
#                             20.8 : 0b0011,
#                             31.25 : 0b0100,
#                             41.7 : 0b0101,
#                             62.5 : 0b0110,
#                             125 : 0b0111,
#                             250 : 0b1000,
#                             500 : 0b1001 }
#         # error coding rate: 4/5
#         # explicit header mode
#         value = bandwidth_to_value[bandwidth] * 0b10000 + 0b0010
#         reg = 0x1D
#         print('Setting Bandwidth to', bandwidth_to_value[bandwidth])
#         command = self.construct_command(SX1276.WRITE, reg, value)
#         self.send_command(command)
    
#     def set_spreading_factor(self, sf):
#         sf_to_value = {64 : 6,
#                     128 : 7,
#                     256 : 8,
#                     512 : 9,
#                     1024 : 10,
#                     2048 : 11,
#                     4096 : 12}
#         # normal mode
#         # crc disable
#         # RX timeout MSB
#         value = sf_to_value[sf] * 0b10000 + 0b0000
#         print('Setting Spreading Factor to', sf)
#         reg = 0x1E
#         command = self.construct_command(SX1276.WRITE, reg, value)
#         self.send_command(command)
    
#     # Transmit of Receive
#     def construct_command(self, transmit_or_receive, packet):
#         return struct.pack("ci", transmit_or_receive, packet)
    
#     # Read or Write Register
#     def construct_command(self, write_or_read, register, value):
#         print('command:', write_or_read, register, value)
#         return struct.pack("cii", write_or_read, register, value)
    
#     def send_command(self, command):
#         print('command:', command)
#         # self.arduino.flush()
#         self.arduino.write(command)
    
#     def get_response(self):
#         # response = self.arduino.readline().decode('utf-8')
#         response = self.arduino.readline()
#         print(response)
#         print()





