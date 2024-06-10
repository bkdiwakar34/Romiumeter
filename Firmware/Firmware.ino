#include "variable.h"
#include <Encoder.h>

#define ENC1A A1
#define ENC1B A2
#define ENC1MAXCOUNT    4*4096
#define ENC1COUNT2DEG   0.25f*0.00166

Encoder myEnc(ENC1A, ENC1B);
int prev_time = 0;

void setup() 
{
pinMode(A3,INPUT_PULLDOWN);   
Wire.begin();
mpu1.begin();
Serial1.begin(230400);
}

void loop() {
delt = micros() - prev_time;
prev_time = micros();
counter = myEnc.read();
mpu1.update();// updates the imu data
gyrox1= (mpu1.getrawGyroX());
gyroy1= (mpu1.getrawGyroY());
gyroz1= (mpu1.getrawGyroZ());
accelx1= (mpu1.getrawAccX());
accely1= (mpu1.getrawAccY());
accelz1= (mpu1.getrawAccZ());
sync = digitalRead(A3);
writeSensorStream(); // write all the data from teensy to bluetooth
}
  
