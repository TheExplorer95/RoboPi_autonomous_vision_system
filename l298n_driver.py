# Python script to control the L298N-Servo

import RPi.GPIO as GPIO
import time

# Global variables

# left front wheel
lf_en = 4
lf_in1 = 17
lf_in2 = 27

# rigth front wheel
rf_in3 = 22
rf_in4 = 5
rf_en = 6

# left back wheel
lb_en = 13
lb_in1 = 19
lb_in2 = 26

# rigth back wheel
rb_in3 = 18
rb_in4 = 23
rb_en = 24

def setupGPIO():
    # set GPIO to 'Broadcom SOC channel'
    GPIO.setmode(GPIO.BCM)

    # Setting all pins as output
    GPIO.setup(lf_in1, GPIO.OUT)
    GPIO.setup(lf_in2, GPIO.OUT)
    GPIO.setup(rf_in3, GPIO.OUT)
    GPIO.setup(rf_in4, GPIO.OUT)
    GPIO.setup(lb_in1, GPIO.OUT)
    GPIO.setup(lb_in2, GPIO.OUT)
    GPIO.setup(rb_in3, GPIO.OUT)
    GPIO.setup(rb_in4, GPIO.OUT)
    
    GPIO.setup(lf_en, GPIO.OUT)
    GPIO.setup(rf_en, GPIO.OUT)
    GPIO.setup(lb_en, GPIO.OUT)
    GPIO.setup(rb_en, GPIO.OUT)
    
    # GPIO preset
    GPIO.output(lf_in1, GPIO.LOW)
    GPIO.output(lf_in2, GPIO.LOW)
    GPIO.output(rf_in3, GPIO.LOW)
    GPIO.output(rf_in4, GPIO.LOW)
    GPIO.output(lb_in1, GPIO.LOW)
    GPIO.output(lb_in2, GPIO.LOW)
    GPIO.output(rb_in3, GPIO.LOW)
    GPIO.output(rb_in4, GPIO.LOW)
    
    GPIO.output(lf_en, GPIO.HIGH)
    GPIO.output(rf_en, GPIO.HIGH)
    GPIO.output(lb_en, GPIO.HIGH)
    GPIO.output(rb_en, GPIO.HIGH)

def forward():
    GPIO.output(lf_in1, GPIO.LOW)
    GPIO.output(lf_in2, GPIO.HIGH)
    GPIO.output(rf_in1, GPIO.LOW)
    GPIO.output(rf_in2, GPIO.HIGH)
    GPIO.output(lb_in1, GPIO.LOW)
    GPIO.output(lb_in2, GPIO.HIGH)
    GPIO.output(rb_in1, GPIO.LOW)
    GPIO.output(rb_in2, GPIO.HIGH)


def backward():
    GPIO.output(lf_in1, GPIO.HIGH)
    GPIO.output(lf_in2, GPIO.LOW)
    GPIO.output(rf_in1, GPIO.HIGH)
    GPIO.output(rf_in2, GPIO.LOW)
    GPIO.output(lb_in1, GPIO.HIGH)
    GPIO.output(lb_in2, GPIO.LOW)
    GPIO.output(rb_in1, GPIO.HIGH)
    GPIO.output(rb_in2, GPIO.LOW)

def endRoutine():
    GPIO.cleanup()
    print('GPIO\'s cleaned up')

def main():
    setupGPIO()
    forward()
    time.sleep(5)
    endRoutine()

if __name__ == '__main__':
    main()
