import time
from SX1276_Interface import SX1276

'''
Example of test file that uses SX1276_Interface. Must
input name of your own serial port.

Output:

Setting Bandwidth to 500 kHz, and coding rate to 4/6
command: wr 29 148 
|loop| wr 29 148 |wr|29|148|
Writing Register 1D to value: 10010100

Setting Spreading Factor to 4096 chips/symbol
command: wr 30 196 
|loop| wr 30 196 |wr|30|196|
Writing Register 1E to value: 11000100

Setting Transmitted Power to 10 dBm
Closest Pout: 10.0 , MaxPower: 2 , OutputPower: 13
command: wr 9 45 
|loop| wr 9 45 |wr|9|45|
Writing Register 9 to value: 101101

command: wr 29 2 
|loop| wr 29 2 |wr|29|2|
Writing Register 1D to value: 10

command: rr 30 
|loop| rr 30 |rr|30|
Register 1E has value: 11000100

command: tx super duper important message coming through 
|loop| tx super duper important message coming through |tx|super duper important message coming through|
Transmitting: super duper important message coming through

command: rx 
|loop| rx |rx|
Receiving ... 
'''

sx1276 = SX1276('/dev/tty.usbmodem14101')
time.sleep(1.7)

sx1276.set_bandwidth(500, '4/6')

sx1276.set_spreading_factor(4096)

sx1276.set_transmit_power(10)

sx1276.write_register(0x1D, 0b00000010)

sx1276.read_register(0x1E)

sx1276.transmit('super duper important message coming through')

sx1276.receive()