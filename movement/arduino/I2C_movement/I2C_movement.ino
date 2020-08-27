#include <L298N.h>
#include <Wire.h>

//------Global variables----------------
#define SLAVE_ADDRESS 0x03
volatile bool flag = false;

union BytesToFloat {
    // 'converts' incoming bytes to a float array
    // valueReading: [0] wheelSpeed; [1] wheelAngle; [2] wheelRotation
    byte valueBuffer[12];
    float valueReading[3];    
} converter;

const unsigned short int wheelVectors_len = 4;
float* wheelVectors[4];   // [0] frontLeft; [1] frontRight; [2] backLeft; [3] backRight
L298N* motors[4];         // [0] frontLeft; [1] frontRight; [2] backLeft; [3] backRight

// L298N PINs
const short int frontLeft_En = 5;
const short int frontLeft_In1 = 7;
const short int frontLeft_In2 = 8;

const short int frontRight_En = 6;
const short int frontRight_In1 = 10;
const short int frontRight_In2 = 11;

const short int backLeft_En = 3;
const short int backLeft_In1 = 2;
const short int backLeft_In2 = 4;

const short int backRight_En = 9;
const short int backRight_In1 = 12;
const short int backRight_In2 = 13;

//--------------------------------------

void calcWheelVectors(float wheelSpeed, float angle, float rotation, float* destArr){
    destArr[0] = 0.8*(wheelSpeed * sin(angle + (3.14159/4))) + 0.2*rotation;  // frontLeft
    destArr[1] = 0.8*(wheelSpeed * cos(angle + (3.14159/4))) - 0.2*rotation;  // frontRight
    destArr[2] = 0.8*(wheelSpeed * cos(angle + (3.14159/4))) + 0.2*rotation;  // backLeft
    destArr[3] = 0.8*(wheelSpeed * sin(angle + (3.14159/4))) - 0.2*rotation;  // backRight
}

void setup() {
    Serial.begin(9600);          // start serial vonnection for print statements
    Wire.begin(SLAVE_ADDRESS);   // initialize i2c as slave
    Wire.onReceive(receiveData); // receive interrupt callback (triggered by I2C-Master)

    // set PINs
    pinMode(backLeft_En, OUTPUT);
    pinMode(backLeft_In1, OUTPUT);    
    pinMode(backLeft_In2, OUTPUT);   
    pinMode(backRight_En, OUTPUT);
    pinMode(backRight_In1, OUTPUT);
    pinMode(backRight_In2, OUTPUT);
    pinMode(frontRight_En, OUTPUT);
    pinMode(frontRight_In1, OUTPUT);
    pinMode(frontRight_In2, OUTPUT);
    pinMode(frontLeft_En, OUTPUT);
    pinMode(frontLeft_In1, OUTPUT);
    pinMode(frontLeft_In2, OUTPUT);

    // initialize motors
    motors[0] = new L298N(frontLeft_En, frontLeft_In1, frontLeft_In2);
    motors[1] = new L298N(frontRight_En, frontRight_In1, frontRight_In2);
    motors[2] = new L298N(backLeft_En, backLeft_In1, backLeft_In2);
    motors[3] = new L298N(backRight_En, backRight_In1, backRight_In2);

    // initlialize wheelVectors
    for(short int i = 0; i<wheelVectors_len; i++){
        wheelVectors[i] = new float;
    }
    
    Serial.println("Ready!");  
}

void loop() {
    if(flag) printInfo();
    delay(100);
}

void printInfo(){
    for(uint8_t index = 0; index<3; index++){
        Serial.print("The number is: ");
        Serial.println(converter.valueReading[index]);
    }
    for(uint8_t index = 0; index<12; index++){
        Serial.print("Number ");
        Serial.print(index);
        Serial.print(" is: ");
        Serial.println(converter.valueBuffer[index]);
    }
    flag = false;
}

void receiveData(int byteCount){
    for(short int index = 0; index<byteCount; index++){
        converter.valueBuffer[index] = Wire.read();
    }
    
    calcWheelVectors(converter.valueReading[0], converter.valueReading[1], converter.valueReading[2], *wheelVectors);

    // mapping of values from [-1:1] to [-255:255]
    for (short int i = 0; i<wheelVectors_len; i++){
        *wheelVectors[i] = map(*wheelVectors[i], -1, 1, -255, 255);
    }
    
    // setting wheels (PWM at En)
    for(short int i = 0; i<wheelVectors_len; i++){
        if(*wheelVectors[i]<0){
            motors[i]->setSpeed(abs(*wheelVectors[i]));
            motors[i]->backward();
        }else if(*wheelVectors[i]>0){
            motors[i]->setSpeed(*wheelVectors[i]);
            motors[i]->forward();
        }else{
            motors[i]->stop();
        }
    }
}
