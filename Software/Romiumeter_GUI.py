
import os
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
import time
from PyQt5.QtCore import QTimer
from Romiumeter_support_file  import SerialPort
from PyQt5.QtWidgets import *
from threading import Thread
from PyQt5.QtCore import QObject, pyqtSignal
from random import randint
import numpy as np
import pyqtgraph as pg

class SignalCommunicate(QObject):
    request_graph_update = pyqtSignal()
    invoke=pyqtSignal(int)

class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("welcome_screen.ui",self)
        self.Login.clicked.connect(self.gotologin)
        self.create.clicked.connect(self.gotocreate)
        
    def gotologin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def gotocreate(self):
        create = CreateAccScreen()
        widget.addWidget(create)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("login.ui",self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login.clicked.connect(self.loginfunction)
        self.back.clicked.connect(self.gotowelcome)
        
    def gotowelcome(self):
        welcome = WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    def loginfunction(self):
        user = self.emailfield.text()
        password = self.passwordfield.text()
        if len(user)==0 or len(password)==0:
            self.error.setText("Please input all fields.")
        else:
            path='data'
            global shoupath
            global necpath
            newpath2 = os.path.join(path, user)
            shoupath=os.path.join(newpath2,'shoulder')
            necpath=os.path.join(newpath2,'neck')
            if os.path.exists(newpath2):
                instruct = Instructions()
                widget.addWidget(instruct)
                widget.setCurrentIndex(widget.currentIndex() + 1)
                self.error.setText("")
            else:
                self.error.setText("Invalid username or password")

class CreateAccScreen(QDialog):
    def __init__(self):
        super(CreateAccScreen, self).__init__()
        loadUi("createacc.ui",self)
        self.hospitalnumber.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signup.clicked.connect(self.signupfunction)
        self.back1.clicked.connect(self.gotowelcome)
    def gotowelcome(self):
        welcome = WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    def signupfunction(self):
        hosp_num = self.hospitalnumber.text()
        confirm_hosp_num = self.confirmhospitalnumber.text()
        if len(hosp_num)==0 or len(confirm_hosp_num)==0:
            self.error.setText("Please fill in all inputs.")
        elif hosp_num != confirm_hosp_num:
            self.error.setText("hospital number does not match.")
        else:
            self.error.setText("Account is created successfully")
            path='data'
            newpath = os.path.join(path, hosp_num )
            shouldpath=os.path.join(newpath,'shoulder')
            neckpath=os.path.join(newpath,'neck')
            flexion = os.path.join(neckpath, 'flexion')
            extension = os.path.join(neckpath, 'extension' )
            Right_Lateral_flexion = os.path.join(neckpath, 'Right_Lateral_flexion' )
            Left_Lateral_flexion = os.path.join(neckpath, 'Left_Lateral_flexion' )
            Right_rotation = os.path.join(neckpath, 'Right_rotation' )
            Left_rotation = os.path.join(neckpath, 'Left_rotation' )
            flexion1=os.path.join(shouldpath,'flexion')
            extension1_=os.path.join(shouldpath,'extension')
            abduction=os.path.join(shouldpath,'abduction')
            adduction=os.path.join(shouldpath,'adduction')
            external_rotation=os.path.join(shouldpath,'e_rotation')
            internal_rotation=os.path.join(shouldpath,'i_rotation')
            if not os.path.exists(path):
                os.makedirs(path)
            if not os.path.exists(newpath):
                os.makedirs(newpath)
                os.makedirs(shouldpath)
                os.makedirs(neckpath)
                os.makedirs(flexion)
                os.makedirs(extension)
                os.makedirs(Right_Lateral_flexion)
                os.makedirs(Left_Lateral_flexion)
                os.makedirs(Right_rotation)
                os.makedirs(Left_rotation)
                os.makedirs(flexion1)
                os.makedirs(extension1_)
                os.makedirs(abduction)
                os.makedirs(adduction)
                os.makedirs(external_rotation)
                os.makedirs(internal_rotation)


class Instructions(QDialog):
    def __init__(self):
        super(Instructions, self).__init__()
        loadUi("instructions.ui",self)     
        self.shoulder.clicked.connect(self.gotoshoulder)
        self.neck.clicked.connect(self.gotoneck)
        self.home2.clicked.connect(self.gotowelcome)
        
    def gotowelcome(self):
        welcome = WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    def gotoshoulder(self):
        global Comp
        Comp = self.comprt.text()
        shoulder = Shoulder()
        widget.addWidget(shoulder)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    def gotoneck(self):
        global Comp
        Comp = self.comprt.text()
        print(Comp)
        neck = Neck()
        widget.addWidget(neck)
        widget.setCurrentIndex(widget.currentIndex() + 1)
class Neck(QDialog):
    def __init__(self):
        super(Neck, self).__init__()
        loadUi("neck.ui",self)
        self.back3_2.clicked.connect(self.gotoinstruct)
        self.obj = []
        for i in range(6):
            self.obj.append(pg.PlotWidget())
        layout1=QGridLayout()
        for j in range(6):
            layout1.addWidget(self.obj[j], j, 0) 
        self.pen = pg.mkPen(color=(255, 0, 0))
        self.plot.setLayout(layout1)
        self.x = list(range(800)) 
        self.y = [randint(0, 800) for _ in range(800)] 
        self.ref=[]
        for l in range(6):
            self.ref.append(self.obj[l].plot(self.x, self.y, pen=self.pen))  
        self.a = SerialPort(Comp,230400)
        self.a.s=1
        self.c=0
        self.sw=0
        self.d=[]
        self.counter=0
        self.counter1=0
        self.dummy=0
        self.counter2=0
        self.a.connect1()
        self.sec.setText("0")
        self.min.setText("0")
        self.hour.setText("0")
        self.startrecording.clicked.connect(self.count2)
        self.signalComm = SignalCommunicate()
        self.signalComm.request_graph_update.connect(self.update_plot_data)
        self.show_new_window()
        self.home.clicked.connect(self.gotowelcome)
    def gotowelcome(self):
        self.a.ser.close()
        self.a.s=0
        welcome = WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        
    def gotoinstruct(self):
        self.a.ser.close()
        self.a.s=0
        instruct1=Instructions()
        widget.addWidget(instruct1)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def change_file_name(self, path2):
        path3=os.path.join(path2, 'session00.csv')
        while os.path.exists(path3):
            base=list(os.path.basename(path3))
            if int(base[8])<9:
                base[8]=int(base[8])+1
                base[8]=str(base[8])
            elif int(base[8])==9:
                base[7]=int(base[7])+1
                base[7]=str(base[7])
                base[8]=int(base[8])-9
                base[8]=str(base[8])
            seperator = ' '
            base=seperator.join(base) 
            path3=os.path.join(path2,base.replace(" ", ""))
        return path3  
    def rec_dir(self):
        global path3
        if self.flexion.isChecked():           
            path2=os.path.join(necpath, 'flexion')
        elif self.extension.isChecked():
            path2=os.path.join(necpath, 'extension')
        elif self.rightlateralflexion.isChecked():
            path2=os.path.join(necpath, 'Right_Lateral_flexion')
        elif self.leftlateralflexion.isChecked():
            path2=os.path.join(necpath, 'Left_Lateral_flexion')
        elif self.rightrotation.isChecked():
            path2=os.path.join(necpath, 'Right_rotation')
        elif self.leftrotation.isChecked():
            path2=os.path.join(necpath, 'Left_rotation')
        path3 = self.change_file_name(path2)
                  
    def update_plot_data(self):
        if len(self.a.q)==1001:
            self.p=self.a.q[1:]
        else:
            self.p=self.a.q   
        self.p=np.array(self.p)
        self.t=np.transpose(self.p)
        for i in range(6):
            if len(list(self.t[i]))==1000:
                self.ref[i].setData(np.array(list(range(1000))),self.t[i])

    def count2(self):
        self.c+=1
        if self.c % 2 == 1:
            self.start_record()
            
        else:
            self.stop_record()

    def stop_record(self):
        self.timer1.stop()
        self.counter=0
        self.counter1=0
        self.counter2=0
        self.sec.setText(" %d" % self.counter)
        self.min.setText(" %d" % self.counter1)
        self.hour.setText(" %d" % self.counter2)
        self.a.kill_switch(0,path3)
        self.startrecording.setText('Start Recording')
        print("Recording stopped")

    def recurring_timer(self):
        self.counter += 1
        self.sec.setText(" %d" % self.counter)
        if self.counter>=60:
            self.counter1+=1
            self.min.setText(" %d" % self.counter1)
            self.counter=0
            self.sec.setText(" %d" % self.counter)
            if self.counter1>=60:
                self.counter2+=1
                self.hour.setText(" %d" % self.counter2)
                self.counter=0
                self.sec.setText(" %d" % self.counter)
                self.counter1=0
                self.min.setText(" %d" % self.counter1)

    def start_record(self):
        self.rec_dir()
        self.a.kill_switch(1,path3)
        self.timer1 = QTimer()
        self.timer1.setInterval(1000)
        self.timer1.timeout.connect(self.recurring_timer)
        self.timer1.start()
        self.startrecording.setText('Stop Recording')
        print("Recording started")
   
    def show_new_window(self):
        reader1 = Thread(target=self.connectnow,args=())
        reader1.start()
     
    def connectnow(self):
        while 1:
            time.sleep(0.5)
            self.signalComm.request_graph_update.emit() 
            
class Shoulder(QDialog):
    def __init__(self):
        super(Shoulder, self).__init__()
        loadUi("shoulder .ui",self)
        self.back2.clicked.connect(self.gotoinstruct)
        self.obj = []
        for i in range(6):
            self.obj.append(pg.PlotWidget())
        layout1=QGridLayout()
        for j in range(6):
            layout1.addWidget(self.obj[j], j, 0)  
        self.pen = pg.mkPen(color=(255, 0, 0))
        self.plot.setLayout(layout1)
        self.x = list(range(800)) 
        self.y = [randint(0, 800) for _ in range(800)] 
        self.ref=[]
        for l in range(6):
            self.ref.append(self.obj[l].plot(self.x, self.y, pen=self.pen))
        self.a = SerialPort(Comp,230400)
        self.a.s=1
        self.c=0
        self.sw=0
        self.d=[]
        self.counter=0
        self.counter1=0
        self.dummy=0
        self.counter2=0
        self.a.connect1()
        self.sec.setText("0")
        self.min.setText("0")
        self.hour.setText("0")
        self.startrecording.clicked.connect(self.count2)
        self.signalComm = SignalCommunicate()
        self.signalComm.request_graph_update.connect(self.update_plot_data)
        self.show_new_window()
        self.home.clicked.connect(self.gotowelcome)
    def gotowelcome(self):
        self.a.ser.close()
        self.a.s=0
        welcome = WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        
    def gotoinstruct(self):
        self.a.ser.close()
        self.a.s=0
        instruct1=Instructions()
        widget.addWidget(instruct1)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def change_file_name(self, path2):
        path3=os.path.join(path2, 'session00.csv')
        while os.path.exists(path3):
            base=list(os.path.basename(path3))
            if int(base[8])<9:
                base[8]=int(base[8])+1
                base[8]=str(base[8])
            elif int(base[8])==9:
                base[7]=int(base[7])+1
                base[7]=str(base[7])
                base[8]=int(base[8])-9
                base[8]=str(base[8])
            seperator = ' '
            base=seperator.join(base) 
            path3=os.path.join(path2,base.replace(" ", ""))
        return path3  
    
    def rec_dir(self):
        global path3
        if self.flexion.isChecked():           
            path2=os.path.join(necpath, 'flexion')
        elif self.extension.isChecked():
            path2=os.path.join(necpath, 'extension')
        elif self.abduction.isChecked():
            path2=os.path.join(necpath, 'abduction')
        elif self.adduction.isChecked():
            path2=os.path.join(necpath, 'adduction')
        elif self.e_rotation.isChecked():
            path2=os.path.join(necpath, 'e_rotation')
        elif self.i_rotation.isChecked():
            path2=os.path.join(necpath, 'i_rotation')
        path3 = self.change_file_name(path2)
        
              
    def update_plot_data(self):
        if len(self.a.q)==1001:
            self.p=self.a.q[1:]
        else:
            self.p=self.a.q   
        self.p=np.array(self.p)
        self.t=np.transpose(self.p)
        for i in range(6):
            if len(list(self.t[i]))==1000:
                self.ref[i].setData(np.array(list(range(1000))),self.t[i])

    def count2(self):
        self.c+=1
        if self.c % 2 == 1:
            self.start_record()
            
        else:
            self.stop_record()

    def stop_record(self):
        self.timer1.stop()
        self.counter=0
        self.counter1=0
        self.counter2=0
        self.sec.setText(" %d" % self.counter)
        self.min.setText(" %d" % self.counter1)
        self.hour.setText(" %d" % self.counter2)
        self.a.kill_switch(0,path3)
        self.startrecording.setText('Start Recording')
        print("Recording stopped")

    def recurring_timer(self):
        self.counter += 1
        self.sec.setText(" %d" % self.counter)
        if self.counter>=60:
            self.counter1+=1
            self.min.setText(" %d" % self.counter1)
            self.counter=0
            self.sec.setText(" %d" % self.counter)
            if self.counter1>=60:
                self.counter2+=1
                self.hour.setText(" %d" % self.counter2)
                self.counter=0
                self.sec.setText(" %d" % self.counter)
                self.counter1=0
                self.min.setText(" %d" % self.counter1)

    def start_record(self):
        self.rec_dir()
        self.a.kill_switch(1,path3)
        self.timer1 = QTimer()
        self.timer1.setInterval(1000)
        self.timer1.timeout.connect(self.recurring_timer)
        self.timer1.start()
        self.startrecording.setText('Stop Recording')
        print("Recording started")
   
    def show_new_window(self):
        reader1 = Thread(target=self.connectnow,args=())
        reader1.start()
     
    def connectnow(self):
        while 1:
            time.sleep(0.5)
            self.signalComm.request_graph_update.emit() 
            
# main
app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(800)
widget.setFixedWidth(1150)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")