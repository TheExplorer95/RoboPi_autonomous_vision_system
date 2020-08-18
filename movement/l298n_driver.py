#Python script to read the Joystick values and send them to the Arduino

import RPI_MasterMovement as Send
import pygame
import math
from time import sleep

#------------Global variables-----------------

# initialize controler
try:
    pygame.init()
    window = pygame.display.set_mode((200, 200), 0, 32)
    pygame.joystick.init()
    j = pygame.joystick.Joystick(0)
    j.init()
    print(f'[INFO] Initialized: {j.get_name()}')
except:
    print('[ERROR] No Joystick connected')
    pygame.joystick.quit()
    exit()

# key mappings
PS3_axis_left_h = 0
PS3_axis_left_v = 1 
PS3_axis_right_h = 2 

def getJoystickReading():
    pygame.event.get()
    # get the joystick values
    joystick_left_h = j.get_axis(PS3_axis_left_h)
    joystick_left_v = j.get_axis(PS3_axis_left_v)
    joystick_right_h = j.get_axis(PS3_axis_right_h)
            
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

        # calculate desired rotation
        rotation = joystick_right_h

        return [speed, angle, rotation]

if __name__ == '__main__':
    try:
        while True:
            # send numbers to the Arduino
            Send.writeNumbers(getJoystickReading())

            sleep(.01)

    except KeyboardInterrupt:
        pygame.joystick.quit()
        quit()

