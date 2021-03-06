import smbus
import struct

# device adress
arduino = 0x03

# initialize serial commumication
bus = smbus.SMBus(1)

def writeNumbers(values):
    # sending an float to the arduino
    # consider changing d to f for float precision
    byteList = []
    try:
        for value in values:
            byteList += list(struct.pack('f', value))
        byteList.append(0)  # fails to send last byte over I2C, hence this needs to be added 
        bus.write_i2c_block_data(arduino, byteList[0], byteList[1:12])
    except:
        return 0

if __name__ == '__main__':
    while True:
        numbers = []
        for i in range(3):
            numbers.append(float(input(f'Give me number {i}: ')))
        writeNumbers(numbers)

