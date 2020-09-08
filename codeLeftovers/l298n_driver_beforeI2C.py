#Python script to control the L298N-Servo

import pygame
import math
from sys import exit
from gpiozero import Motor
from time import sleep

#------------Global variables-----------------

# set GPIO PINs by 'Broadcom SOC channel'

# left back wheel
lb_bw_PIN = 4
lb_fw_PIN = 17

# left front wheel
lf_bw_PIN = 27
lf_fw_PIN = 22

# rigth front wheel
rf_bw_PIN = 19
rf_fw_PIN = 13

# rigth back wheel
rb_bw_PIN = 18
rb_fw_PIN = 26

# initialize the motors
bl = Motor(forward=lf_fw_PIN, 
              backward=lf_bw_PIN,
              enable=None,
              pwm=True)

fr = Motor(forward=rf_fw_PIN, 
              backward=rf_bw_PIN,
              enable=None,
              pwm=True)
  
fl = Motor(forward=lb_fw_PIN, 
              backward=lb_bw_PIN,
              enable=None,
              pwm=True)
  
br = Motor(forward=rb_fw_PIN, 
              backward=rb_bw_PIN,
              enable=None,
              pwm=True)

# initialize controler
try:
    pygame.init()
    window = pygame.display.set_mode((200, 200), 0, 32)
    pygame.joystick.init()
    j = pygame.joystick.Joystick(0)
    j.init()
    print(f'Initialized: {j.get_name()}')
except:
    print('No Joystick connected')
    pygame.joystick.quit()
    exit()

# key mappings
PS3_axis_left_h = 0
PS3_axis_left_v = 1 
PS3_axis_right_h = 2 

def main():
    try:
        while True:
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

                # calculate vectors
                v_fl = 0.8*(speed * math.sin(angle + (math.pi/4))) + 0.2*rotation
                v_fr = 0.8*(speed * math.cos(angle + (math.pi/4))) - 0.2*rotation
                v_bl = 0.8*(speed * math.cos(angle + (math.pi/4))) + 0.2*rotation
                v_br = 0.8*(speed * math.sin(angle + (math.pi/4))) - 0.2*rotation
                
                print(f'FL={v_fl} FR={v_fr} BL={v_bl} BR={v_br}')

                # update motor
                if v_fl < 0:
                    fl.backward(abs(v_fl))
                else:
                    fl.forward(v_fl)
                
                if v_fr < 0:
                    fr.backward(abs(v_fr))
                else:
                    fr.forward(v_fr)
                
                if v_bl < 0:
                    bl.backward(abs(v_bl))
                else:
                    bl.forward(v_bl)
                
                if v_br < 0:
                    br.backward(abs(v_br))
                else:
                    br.forward(v_br)
            else:
                fl.stop()
                fr.stop()
                bl.stop()
                br.stop()
                
            
            sleep(.1)

    except KeyboardInterrupt:
        pygame.joystick.quit()
        exit()

if __name__ == '__main__':
    main()
