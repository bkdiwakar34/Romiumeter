import serial
import struct
from threading import Thread
import csv
import numpy as np

class SerialPort(object):
    def __init__(self, serialport, serialrate=460800):
        self.c=0
        self.ad='0'
        self.count = 0
        self.plSz = 0
        self.payload = bytearray()
        self.sw=0
        self.w=[]
        self.l=np.zeros((6,1000))
        self.l1=np.zeros((1000,6))
        self.y=[]
        self.q=[]
        self.s=0
        self.serialport = serialport
        self.ser = serial.Serial(serialport, serialrate) 
        
    def show_data(self):
        chksum=0
        _chksum=1
        payload=[]
        y1=[]
        x=[]
        while self.s==1:  
            trl=self.ser.read(1000)
            x.append(trl)
            y1=y1+list(x[:][0])
            x=[]
            for i in range(1000):
                if y1[0]==255 and y1[1]==255:    
                    if len(y1)>21:
                        chksum = 255 + 255
                        plSz = y1[2]
                        chksum += plSz
                        y2=bytes(y1[3:21])
                        payload = y2
                        chksum += sum(y1[3:21])
                        chksum = bytes([chksum % 256])
                        _chksum = bytes([y1[21]%256])
                        if chksum==_chksum:  
                            self.y=list(struct.unpack('9h',payload))
                            self.c=self.y[:6]  
                            self.q.append(self.c)
                            if len(self.q)>1000:
                                self.q=self.q[1:]
                            if self.sw :
                                self.writer.writerow(self.y)
                            y1=y1[22:]
                            if len(y1)<22:
                                break
                        else:
                            y1=y1[22:]
                            if len(y1)<22:
                                break
                    else:
                        break       
                else:
                    y1=y1[i+1:]
                    if len(y1)<4:
                        break

    def kill_switch(self, sw,path3):
        if sw:
            header=['gyrox1','gyroy1','gyroz1','accelx1','accely1','accelz1','enc','delt','sync']
            self.f=open(path3, 'w',newline='')
            self.writer = csv.writer(self.f)
            self.writer.writerow(header)
            self.sw = 1
        if not sw:
            self.sw = 0
            self.f.close()
              
    def connect1(self):
        if self.ser.isOpen():
            self.show=Thread(target=self.show_data,args=())
            self.show.start() 



