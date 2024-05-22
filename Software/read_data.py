import serial
import struct
from threading import Thread
import csv
import numpy as np
import math
import json

class MyJSONEncoder(json.JSONEncoder):         
    def default(self, o):
        try:
            return o.tolist() 
        except AttributeError:
            pass
        return json.JSONEncoder.default(self, o)
    
class SerialPort(object):
    def __init__(self, serialport, serialrate=460800):
        self.sw=0
        self.s=0
        self.g_ofst=1
        self.offset = []
        self.angle_acc =np.zeros(500)
        # Initialise serial port
        self.serialport = serialport
        self.ser = serial.Serial(serialport, serialrate) 
        self.q_int = [1, 0, 0, 0]
        self.calibrate = 0
        self.reset = 0
        self._var_gyro_offst = 2.0
    def show_data(self):      
        while self.s==1:  
            y1 = self.ser.read(100)
            for i in range(100):
                if y1[0]==255 and y1[1]==255:
                    if len(y1)>11:
                        chksum = 255 + 255
                        plSz = y1[2]
                        chksum += plSz
                        y2=bytes(y1[3:11])
                        payload = y2
                        chksum += sum(y1[3:11])
                        chksum = bytes([chksum % 256])
                        _chksum = bytes([y1[11]%256])
                        if chksum==_chksum: 
                            self.y=list(struct.unpack('4h',payload))
                            data = self.y
                            if self.calibrate == 1:
                                self.offset.append(np.array(self.y[:3])/65.5)
                                if len(self.offset) == 500:
                                    gyro_offset = np.mean(self.offset, axis=0)
                                    offset = {'gyro_off':gyro_offset}
                                    with open(r'D:\banglore_workshop\angle_demo\software\export.json', 'w') as f:
                                        json.dump(offset, f, separators=(',', ':'), sort_keys=True, indent=4, cls=MyJSONEncoder)
                                    self.offset = []
                                    self.calibrate = 0
                            if self.reset == 1:
                                self.offset.append(np.array(self.y[:3])/65.5)
                                if len(self.offset) == 500:
                                    gyro_offset = np.mean(self.offset, axis=0)
                                    self._var_gyro_offst = np.max(np.var(self.offset[:500],axis = 0))

                            with open(r'D:\banglore_workshop\angle_demo\software\export.json', "r") as f:
                                off = json.load(f, object_pairs_hook=lambda x: dict((k, np.array(v)) for k, v in x))
                            if self._var_gyro_offst < 1.0:
                                final_gyro_off = gyro_offset
                            else:
                                final_gyro_off = off['gyro_off']
                            ang = self.rom(data,final_gyro_off)
                            data.extend([ang])
                            self.angle_acc = np.append(self.angle_acc, ang)
                            if len(self.angle_acc)>4000:
                                self.angle_acc = self.angle_acc[1:]
                            if self.sw:
                                self.writer.writerow(data)
                            y1=y1[12:]
                            if len(y1)<12:
                                break
                        else:
                            y1=y1[12:]
                            if len(y1)<12:
                                break
                    else:
                        break       
                else:
                    y1=y1[i+1:]
                    if len(y1)<4:
                        break

    def kill_switch(self, sw,path3):
        if sw:
            header=['gx','gy','gz','del_t','ang']
            self.f=open(path3, 'w',newline='')
            self.writer = csv.writer(self.f)
            self.writer.writerow(header)
            self.sw = 1
        if not sw:
            self.sw = 0
            self.f.close()

    def quaternion_multiply(self, quaternion1, quaternion0):
        w0, x0, y0, z0 = quaternion0
        w1, x1, y1, z1 = quaternion1
        return np.array([-x1 * x0 - y1 * y0 - z1 * z0 + w1 * w0,
                        x1 * w0 + y1 * z0 - z1 * y0 + w1 * x0,
                        -x1 * z0 + y1 * w0 + z1 * x0 + w1 * y0,
                        x1 * y0 - y1 * x0 + z1 * w0 + w1 * z0], dtype=np.float64)

    def rom(self,data,off):
        gyro = data[:3]
        del_t = data[3]/1000000
        gyro = (np.array(gyro).astype(float)/65.5)-off 
        gyro = np.deg2rad(gyro)
        if np.linalg.norm(gyro) !=0 :
                aor = gyro/ np.linalg.norm(gyro)
        else:
                aor = gyro
        delta_theta = np.linalg.norm(gyro)*del_t
        temp_var = math.sin(delta_theta/2)
        q_gyro = [math.cos(delta_theta/2), aor[0]*temp_var, aor[1]*temp_var, aor[2]*temp_var]
        self.q_int = self.quaternion_multiply(q_gyro,self.q_int)
        q_int_norm = self.q_int/np.linalg.norm(self.q_int)
        gyro_ang = np.rad2deg(2*np.arccos(q_int_norm[0]))
        return gyro_ang
   
    def connect1(self):
        if self.ser.isOpen():
            self.show=Thread(target=self.show_data,args=())
            self.show.start() 



