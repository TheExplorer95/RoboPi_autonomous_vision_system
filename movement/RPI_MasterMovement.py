import smbus
import struct

# device adress
arduino = 0x03

# initialize serial commumication
bus = smbus.SMBus(1)

def writeNumber(value):
    # sending an float to the arduino
    # consider changing d to f for float precision
    ba = list(struct.pack('!f', value))
    print(ba)
    bus.write_i2c_block_data(arduino, ba[0], ba[1:3])

while True:
    number = float(input('Give me a number: '))
    writeNumber(number)

