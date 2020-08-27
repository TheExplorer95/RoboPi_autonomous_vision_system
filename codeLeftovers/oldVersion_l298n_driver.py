# Python script to control the L298N-Servo

import RPi.GPIO as GPIO
import time

# set GPIO to 'Broadcom SOC channel'
GPIO.setmode(GPIO.BCM)

temp1 = 1

# left front wheel
lf_in3 = 17
lf_in4 = 27
lf_en = 4


# Setting outputs
GPIO.setup(lf_in3, GPIO.OUT)
GPIO.setup(lf_in4, GPIO.OUT)
GPIO.setup(lf_en, GPIO.OUT)

# GPIO preset
GPIO.output(lf_in3, GPIO.LOW)
GPIO.output(lf_in4, GPIO.LOW)
GPIO.output(lf_en, GPIO.HIGH)

def forward():
    GPIO.output(lf_in3, GPIO.LOW)
    GPIO.output(lf_in4, GPIO.HIGH)

def backward():
    GPIO.output(lf_in3, GPIO.HIGH)
    GPIO.output(lf_in4, GPIO.LOW)

def endRoutine():
    GPIO.cleanup()
    print('GPIO\'s cleaned up')

def main():
    forward()
    time.sleep(5)
    backward()
    time.sleep(5)
    endRoutine()

if __name__ == '__main__':
    main()
