#Python script to read the Joystick values and send them to the Arduino
import pygame
import math
from time import sleep
import smbus
import struct
from threading import Thread, Lock

class DriveControler():
    
    def __init__(self):
        self.init_arduino()
        self.init_joystick()
        self.drive_control()

    def init_arduino(self):
        self.arduino_addr = 0x03
        self.bus = smbus.SMBus(1)

    def init_joystick(self):
        # initialize pygame to get joystick instance
        pygame.init()
        self.window = pygame.display.set_mode((200, 200), 0, 32)
        pygame.joystick.init()
        if not pygame.joystick.get_init():
            raise Exception('[Error] - Joystick module not properly initialized')
        self.j = pygame.joystick.Joystick(0)
        self.j.init()
        print(f'[INFO] - Initialized: {self.j.get_name()}')

        # key mappings
        self.PS3_axis_left_h = 0
        self.PS3_axis_left_v = 1 
        self.PS3_axis_right_h = 3 

        self.instructions = tuple()

    def getJoystickReading(self):
        pygame.event.get()
        # get the joystick values
        joystick_left_h = self.j.get_axis(self.PS3_axis_left_h)
        joystick_left_v = self.j.get_axis(self.PS3_axis_left_v)
        joystick_right_h = self.j.get_axis(self.PS3_axis_right_h)
        
        # left verticval joystick values inverted
        if joystick_left_v != 0:
            joystick_left_v = -joystick_left_v
                
        # calculation for the wheel vectors 
        if (joystick_left_h != 0) or (joystick_left_v != 0) or (joystick_right_h != 0):
            # calculate desired speed (magnitude) [-1,1]
            speed = math.sqrt(joystick_left_h**2 + joystick_left_v**2)/1.39

            # calculate desired angle in rad [0, 2pi]
            vec_x = joystick_left_h 
            vec_y = joystick_left_v 
            len_vec = math.sqrt(vec_x*vec_x + vec_y*vec_y)
                    
            if len_vec != 0:
                angle = math.asin(vec_y/len_vec)*180/math.pi
            else:
                angle = 0

            if joystick_left_h <= 0 and angle >= 0:
                angle = angle
            elif joystick_left_h <= 0 and angle < 0:
                angle = 360 + angle
            elif joystick_left_h > 0 and angle >= 0:
                 angle = 180 - angle
            elif joystick_left_h > 0 and angle < 0:
                 angle = 180 - angle
                 
            angle = ((angle-90)%360) *math.pi/180

            # rotation == joystick_right_h
            self.instructions = (speed, angle, joystick_right_h)    
        else:
            self.instructions = (0.0, 0.0, 0.0)

    def writeNumbers(self):
        # sending floats to the arduino
        byteList = []
        for i in self.instructions:
            byteList += list(struct.pack('f', i))
        byteList.append(0) #fails to send last byte
        self.bus.write_i2c_block_data(self.arduino_addr, byteList[0], byteList[1:12])

    def drive_control(self):
        def drive_control_thread():
            try:
                while True:
                    self.getJoystickReading()
                    self.writeNumbers()
                    sleep(0.01)
            except Exception as e:
                pygame.joystick.quit()

        self.readWriteThread = Thread(target=drive_control_thread, args=())
        self.readWriteThread.daemon = True
        self.readWriteThread.start()

if __name__ == '__main__':
    driveControler = DriveControler()

    while True:
        pass
#   while True:
#       try:
#           driveControler.getJoystickReading()
#           driveControler.writeNumbers()
#           sleep(0.01)
#       finally:
#           pygame.joystick.quit()
#           print('[INFO] - Joystick disconnected')
    
