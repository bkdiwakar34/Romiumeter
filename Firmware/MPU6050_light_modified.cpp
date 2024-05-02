
#include "MPU6050_light_modified.h"
#include "Arduino.h"

/* Wrap an angle in the range [-limit,+limit] (special thanks to Edgar Bonet!) */
static float wrap(float angle,float limit){
  while (angle >  limit) angle -= 2*limit;
  while (angle < -limit) angle += 2*limit;
  return angle;
}

/* INIT and BASIC FUNCTIONS */

MPU6050::MPU6050(TwoWire &w){
  wire = &w;
}

byte MPU6050::begin(int gyro_config_num, int acc_config_num){
  // changed calling register sequence [https://github.com/rfetick/MPU6050_light/issues/1] -> thanks to augustosc
  byte status = writeData(MPU6050_PWR_MGMT_1_REGISTER, 0x01); // check only the first connection with status
  writeData(MPU6050_SMPLRT_DIV_REGISTER, 0x00);
  writeData(MPU6050_CONFIG_REGISTER, 0x00);
  setGyroConfig(gyro_config_num);
  setAccConfig(acc_config_num);
  
  this->update();
  //angleX = this->getAccAngleX();
  //angleY = this->getAccAngleY();
  preInterval = millis(); // may cause lack of angular accuracy if begin() is much before the first update()
  return status;
}

byte MPU6050::writeData(byte reg, byte data){
  wire->beginTransmission(address);
  wire->write(reg);
  wire->write(data);
  byte status = wire->endTransmission();
  return status; // 0 if success
}

// This method is not used internaly, maybe by user...
byte MPU6050::readData(byte reg) {
  wire->beginTransmission(address);
  wire->write(reg);
  wire->endTransmission(true);
  wire->requestFrom(address,(uint8_t) 1);
  byte data =  wire->read();
  return data;
}

/* SETTER */

byte MPU6050::setGyroConfig(int config_num){
  byte status;
  switch(config_num){
    case 0: // range = +- 250 deg/s
    gyro_lsb_to_degsec = 131.0;
    status = writeData(MPU6050_GYRO_CONFIG_REGISTER, 0x00);
    break;
  case 1: // range = +- 500 deg/s
    gyro_lsb_to_degsec = 65.5;
    status = writeData(MPU6050_GYRO_CONFIG_REGISTER, 0x08);
    break;
  case 2: // range = +- 1000 deg/s
    gyro_lsb_to_degsec = 32.8;
    status = writeData(MPU6050_GYRO_CONFIG_REGISTER, 0x10);
    break;
  case 3: // range = +- 2000 deg/s
    gyro_lsb_to_degsec = 16.4;
    status = writeData(MPU6050_GYRO_CONFIG_REGISTER, 0x18);
    break;
  default: // error
    status = 1;
    break;
  }
  return status;
}

byte MPU6050::setAccConfig(int config_num){
  byte status;
  switch(config_num){
    case 0: // range = +- 2 g
    acc_lsb_to_g = 16384.0;
    status = writeData(MPU6050_ACCEL_CONFIG_REGISTER, 0x00);
    break;
  case 1: // range = +- 4 g
    acc_lsb_to_g = 8192.0;
    status = writeData(MPU6050_ACCEL_CONFIG_REGISTER, 0x08);
    break;
  case 2: // range = +- 8 g
    acc_lsb_to_g = 4096.0;
    status = writeData(MPU6050_ACCEL_CONFIG_REGISTER, 0x10);
    break;
  case 3: // range = +- 16 g
    acc_lsb_to_g = 2048.0;
    status = writeData(MPU6050_ACCEL_CONFIG_REGISTER, 0x18);
    break;
  default: // error
    status = 1;
    break;
  }
  return status;
}

/* UPDATE */

void MPU6050::fetchData(){
 wire->beginTransmission(address);
 wire->setClock(100000);
 wire->write(MPU6050_ACCEL_OUT_REGISTER);
 wire->endTransmission(false);
 wire->requestFrom(address,(uint8_t) 14);

  int16_t rawData[7]; // [ax,ay,az,temp,gx,gy,gz]

  for(int i=0;i<7;i++){
  rawData[i]  = wire->read() << 8;
    rawData[i] |= wire->read();
  }

  rawaccX = rawData[0];
  rawaccY = rawData[1];
  rawaccZ = rawData[2];
  rawtemp = rawData[3];
  rawgyroX = rawData[4];
  rawgyroY = rawData[5];
  rawgyroZ = rawData[6];

}

void MPU6050::update(){
  // retrieve raw data
  this->fetchData();
}
