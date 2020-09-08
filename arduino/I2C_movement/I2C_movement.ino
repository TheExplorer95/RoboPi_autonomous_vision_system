#include <L298N.h>
#include <Wire.h>

//------Global variables------------------------------------------------------------------------------------------
#define SLAVE_ADDRESS 0x03

//volatile bool printFlag = false;
volatile bool motorFlag = false;
unsigned long timeDelta = 0;
unsigned long currentTime = millis();
volatile unsigned long callTime = -1;

const unsigned short int wheelVectors_len = 4;
float wheelVectors[wheelVectors_len];           // [0] frontLeft; [1] frontRight; [2] backLeft; [3] backRight
const float SLOPE_MAP = 255;                    // for mapping -> slope = (output_end - output_start) / (input_end - input_start)

L298N* motors[4];                               // [0] frontLeft; [1] frontRight; [2] backLeft; [3] backRight

union BytesToFloat {
    // 'converts' incoming bytes to a float array
    // valueReading: [0] wheelSpeed; [1] wheelAngle; [2] wheelRotation
    byte valueBuffer[12];
    float valueReading[3];    
} converter;


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

//------Functions---------------------------------------------------------------------------------------------------

void calcWheelVectors(float wheelSpeed, float angle, float rotation, float* destArr){
    float dirA = 0.8*(wheelSpeed * sin(angle + (PI/4)));
    float dirB = 0.8*(wheelSpeed * cos(angle + (PI/4)));
    float rotate = 0.2*rotation;
    
    destArr[0] = dirA + rotate;  // frontLeft
    destArr[1] = dirB - rotate;  // frontRight
    destArr[2] = dirB + rotate;  // backLeft
    destArr[3] = dirA - rotate;  // backRight
}

int mapValue(float value){
    int output = -255 + SLOPE_MAP * (value + 1);   // output = output_start + slope * (input - input_start)
    return output;
}

void setMotors(){
    for(short int i = 0; i<wheelVectors_len; i++){
        if(wheelVectors[i]<0){
            motors[i]->setSpeed(abs(wheelVectors[i]));
            motors[i]->backward();
        }else if(wheelVectors[i]>0){
            motors[i]->setSpeed(wheelVectors[i]);
            motors[i]->forward();
        }
    }
}

void stopMotors(){
    for(short int i = 0; i<wheelVectors_len; i++){
        motors[i]->stop();
    }
    motorFlag = false;
}

void tester(){
    while(true){
        for(short int s = 100; s<255; s+=100){
          delay(10000);
          for(short int i = 0; i<4; i++){
            motors[i]->setSpeed(s);
            motors[i]->backward();
          }
        }
    }  
}

void printInfo(){
    for(short int i = 0; i<4; i++){
        Serial.print("The ");
        Serial.print(i);
        Serial.print(" wheel is: ");
        Serial.println(wheelVectors[i]);
    }
    
    //printFlag = false;
}

void receiveData(int byteCount){  
    callTime = millis();

    // receiving incomming bytes
    for(short int i = 0; i<byteCount; i++){
        converter.valueBuffer[i] = Wire.read();
    }
    
    calcWheelVectors(converter.valueReading[0], converter.valueReading[1], converter.valueReading[2], wheelVectors);
    
    // mapping of values from [-1:1] to [-255:255]
    for (short int i = 0; i<wheelVectors_len; i++){
        wheelVectors[i] = mapValue(wheelVectors[i]);
    }
    
    // setting wheels (PWM at En)
    setMotors();
    
    //printFlag = true;
    motorFlag = true;
}

void blinkLED(int wait){
    digitalWrite(LED_BUILTIN, HIGH);
    delay(wait);
    digitalWrite(LED_BUILTIN, LOW);
    delay(wait);
}

//--------Core programm----------------------------------------------------------------------------------------------

void setup() {
    //Serial.begin(9600);          // start serial vonnection for print statements
    Wire.begin(SLAVE_ADDRESS);   // initialize i2c as slave
    Wire.onReceive(receiveData); // receive interrupt callback (triggered by I2C-Master)

    // initialize motors
    motors[0] = new L298N(frontLeft_En, frontLeft_In1, frontLeft_In2);
    motors[1] = new L298N(frontRight_En, frontRight_In1, frontRight_In2);
    motors[2] = new L298N(backLeft_En, backLeft_In1, backLeft_In2);
    motors[3] = new L298N(backRight_En, backRight_In1, backRight_In2);

    // finished initialization
    //Serial.println("Ready!");
    blinkLED(200);
    blinkLED(100);
    blinkLED(20);
}


void loop() {
    // stop motors if no signal received
    delay(100);
    currentTime = millis();
    timeDelta = currentTime - callTime;
    if((timeDelta>200)&&motorFlag) stopMotors();
    //tester();
    //if(printFlag) printInfo();
}
