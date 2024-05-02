#include "variable.h"
int prev_time = 0;

void setup() 
{
 Serial1.begin(230400);
 //Initiate the Wire library and join the I2C bus.
  Wire.begin();
  mpu1.setAddress(0x68);
  mpu1.begin(1,0);
}

void loop() {
delt = micros() - prev_time;
prev_time = micros();
mpu1.update();// updates the imu data
gyrox1= (mpu1.getrawGyroX());
gyroy1= (mpu1.getrawGyroY());
gyroz1= (mpu1.getrawGyroZ());
writeSensorStream(); // write all the data from teensy to bluetooth
}
  
