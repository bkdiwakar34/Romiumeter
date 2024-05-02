#ifndef MPU6050_LIGHT_MODIFIED_H
#define MPU6050_LIGHT_MODIFIED_H

#include "Arduino.h"
#include "Wire.h"

#define MPU6050_ADDR                  0x68
#define MPU6050_SMPLRT_DIV_REGISTER   0x19
#define MPU6050_CONFIG_REGISTER       0x1a
#define MPU6050_GYRO_CONFIG_REGISTER  0x1b
#define MPU6050_ACCEL_CONFIG_REGISTER 0x1c
#define MPU6050_PWR_MGMT_1_REGISTER   0x6b

#define MPU6050_GYRO_OUT_REGISTER     0x43
#define MPU6050_ACCEL_OUT_REGISTER    0x3B

#define RAD_2_DEG             57.29578 // [deg/rad]
#define CALIB_OFFSET_NB_MES   500
#define TEMP_LSB_2_DEGREE     340.0    // [bit/celsius]
#define TEMP_LSB_OFFSET       12412.0

#define DEFAULT_GYRO_COEFF    0.98

class MPU6050{
  public:
    // INIT and BASIC FUNCTIONS
  MPU6050(TwoWire &w);
    byte begin(int gyro_config_num=1, int acc_config_num=0);
  
  byte writeData(byte reg, byte data);
    byte readData(byte reg);
  
  
  void setAddress(uint8_t addr){ address = addr; };
  uint8_t getAddress(){ return address; };
  
  // MPU CONFIG SETTER
  byte setGyroConfig(int config_num);
  byte setAccConfig(int config_num);
  
  // DATA GETTER
    int getrawAccX(){ return rawaccX; };
    int getrawAccY(){ return rawaccY; };
    int getrawAccZ(){ return rawaccZ; };

    int getrawGyroX(){ return rawgyroX; };
    int getrawGyroY(){ return rawgyroY; };
    int getrawGyroZ(){ return rawgyroZ; };
  
  

  // INLOOP UPDATE
  void fetchData(); // user should better call 'update' that includes 'fetchData'
    void update();
  
  // UPSIDE DOWN MOUNTING
  bool upsideDownMounting = false;


  private:
    TwoWire *wire;
  uint8_t address = MPU6050_ADDR; // 0x68 or 0x69
  float gyro_lsb_to_degsec, acc_lsb_to_g;
    float gyroXoffset, gyroYoffset, gyroZoffset;
  float accXoffset, accYoffset, accZoffset;
    int rawtemp, rawaccX, rawaccY, rawaccZ, rawgyroX, rawgyroY, rawgyroZ;
    float temp, accX, accY, accZ, gyroX, gyroY, gyroZ;
    float angleAccX, angleAccY;
    float angleX, angleY, angleZ;
    unsigned long preInterval;
    float filterGyroCoef; // complementary filter coefficient to balance gyro vs accelero data to get angle
};

#endif
