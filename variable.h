
#include "Arduino.h"
#include "CustomDS.h"
#include "Wire.h"
#include "MPU6050_light_modified.h"

MPU6050 mpu1(Wire);

//Sensor data

int gyrox1;
int gyroy1;
int gyroz1;
int delt;

// Out data buffer
::OutDataBuffer4Float outPayload;
