# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 18:01:07 2022

@author: 김미송
"""

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication, QDate
import sys  # We need sys so that we can pass argv to QApplication
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent, QCursor


from SolarSystem import SolarSystem
import webbrowser
# ----------------------------------------------------

main_class = uic.loadUiType("main2_horizontal.ui")[0]
sss_class = uic.loadUiType("sss_test.ui")[0]
info_class = uic.loadUiType("info.ui")[0]

# ----------------------------------------------------

class MainClass(QMainWindow, main_class):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('icon_buzz.png'))
        self.setWindowFlag(Qt.FramelessWindowHint)
        
        
        self.btn_SSS.clicked.connect(self.btnSSSFunction)
        self.btn_info.clicked.connect(self.btnInfoFunction)
        self.btn_exit.clicked.connect(self.btnExitFunction)

            
    def btnSSSFunction(self):
        print("move to the Simple Solar System window")
        self.w = SSSClass()
        if self.w.isVisible():
            self.w.hide()
            self.show()
        else:
            self.hide()
            self.w.show()       
    
    def btnInfoFunction(self):
        print("move to the Information window")
        self.w = InfoClass()
        if self.w.isVisible():
            self.w.hide()
            self.show()
        else:
            self.hide()
            self.w.show() 
        
    def btnExitFunction(self, event):
        print("EXIT ;)")
        self.close()
        
    def closeEvent(self, event):
        message = QMessageBox.question(self, "Exit-이름", "Are you sure you want to quit?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if message == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # MOUSE Click drag EVENT function
    def mousePressEvent(self, event):
        if event.button()==Qt.LeftButton:
            self.m_flag=True
            self.m_Position=event.globalPos()-self.pos() #Get the position of the mouse relative to the window
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  #Change mouse icon
    
    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:  
            self.move(QMouseEvent.globalPos()-self.m_Position)#Change window position
            QMouseEvent.accept()
    
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag=False
        self.setCursor(QCursor(Qt.ArrowCursor))

class SSSClass(QMainWindow, sss_class): 
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('icon_buzz.png'))
        self.setWindowFlag(Qt.FramelessWindowHint)
   
        self.fig = plt.Figure(facecolor='black')
        self.canvas = FigureCanvas(self.fig)
        self.ss = SolarSystem()
        
        self.btn_home.clicked.connect(self.btnHomeFunction)
       
        # self.btn_home.clicked.connect()
        self.btn_reset.clicked.connect(self.btnResetFunction)
        self.btn_plus.clicked.connect(lambda: self.btnPlusNMinusFunction(step=1))   #매개변수있으면 lambda
        self.btn_minus.clicked.connect(lambda: self.btnPlusNMinusFunction(step=-1))
        self.dateEdit.dateChanged.connect(lambda: self.dateEditFunction(True))
        self.dateEdit.setDate(QDate.currentDate())
        self.btn_exit.clicked.connect(self.btnExitFunction)
        
    def btnHomeFunction(self):
        self.w=MainClass()
        self.hide()
        self.w.show()  
    
    def btnResetFunction(self):
        self.dateEdit.setDate(QDate.currentDate())
        
    def btnPlusNMinusFunction(self, step=0):
        date = self.dateEdit.date().addDays(step)
        self.dateEdit.setDate(date)
        
    def dateEditFunction(self, check):
        date = self.dateEdit.date()
        if check:
            self.plotSolarSystem(yyyy=date.year(),mm=date.month(),dd=date.day())
# =============================================================================
# FUNCTION
    def plotSolarSystem(self, yyyy=0,mm=0,dd=0):
        
        self.graph_verticalLayout.removeWidget(self.canvas)
        #self.ax.clear()
        self.fig = plt.Figure(facecolor='black',figsize=(8,2))     #facecolor='black'
        self.fig.patch.set_alpha(0)
        
        self.canvas = FigureCanvas(self.fig)
        
        self.graph_verticalLayout.addWidget(self.canvas)
        self.graph_verticalLayout.setContentsMargins(0, 0, 0, 0)
    
        ax = self.fig.add_subplot(111)  # 1행 1열로 나눈건 중 첫번재
        ax.set_xlim(-17,17)
        ax.set_ylim(-17,17)
        ax.set_aspect('equal')
        ax.margins(0,0)
        #ax.axis('off')                         # 축 제거
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
        ax.patch.set_facecolor('#000000')
        
        theta = np.linspace(0,2*np.pi, 1000)
        x_c = np.sin(theta)
        y_c = np.cos(theta)
        for r in np.arange(2,18,2):
            ax.plot(r*x_c, r*y_c, color="gray")
# =============================================================================
        (xs,ys)=self.ss.getXnY(yyyy=yyyy, mm=mm, dd=dd)         
        for x, y, path in zip(xs, ys, self.ss.getPaths()):
            ab = AnnotationBbox(getImage(path,self.ss.getZoom()), (x, y), frameon=False)
            ax.add_artist(ab)
        self.canvas.draw()
        return ax
    
    def btnExitFunction(self, event):
        print("EXIT ;)")
        self.close()
    
    # MOUSE Click drag EVENT function
    def mousePressEvent(self, event):
        if event.button()==Qt.LeftButton:
            self.m_flag=True
            self.m_Position=event.globalPos()-self.pos() #Get the position of the mouse relative to the window
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  #Change mouse icon
    
    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:  
            self.move(QMouseEvent.globalPos()-self.m_Position)#Change window position
            QMouseEvent.accept()
    
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag=False
        self.setCursor(QCursor(Qt.ArrowCursor))
# =============================================================================
        
# close 이벤트
# =============================================================================

    def closeEvent(self, event):
        message = QMessageBox.question(self, "Exit-이름", "Are you sure you want to quit?",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if message == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()     
# =============================================================================
            
def getImage(path, zoom=1):
    return OffsetImage(plt.imread(path), zoom=zoom)
 
        
class InfoClass(QMainWindow, info_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('icon_buzz.png'))
        self.setWindowFlag(Qt.FramelessWindowHint)
        
        
        self.ss = SolarSystem()
        self.getSolarSystemInfo()
        
        self.btn_home.clicked.connect(self.btnHomeFunction)
        self.btn_more.clicked.connect(lambda: webbrowser.open('https://solarsystem.nasa.gov/solar-system/our-solar-system/overview/'))
        self.btn_exit.clicked.connect(self.btnExitFunction)   
        
        self.btn_sun.clicked.connect(self.btnSunFunction)
        self.btn_mercury.clicked.connect(lambda: self.btnPlanetFunction(0))
        self.btn_venus.clicked.connect(lambda: self.btnPlanetFunction(1))
        self.btn_earth.clicked.connect(lambda: self.btnPlanetFunction(2))
        self.btn_mars.clicked.connect(lambda: self.btnPlanetFunction(3))
        self.btn_jupiter.clicked.connect(lambda: self.btnPlanetFunction(4))
        self.btn_saturn.clicked.connect(lambda: self.btnPlanetFunction(5))
        self.btn_uranus.clicked.connect(lambda: self.btnPlanetFunction(6))
        self.btn_neptune.clicked.connect(lambda: self.btnPlanetFunction(7))
        
    def btnHomeFunction(self):
        self.w = MainClass()
        self.hide()
        self.w.show()    
    
    def btnExitFunction(self, event):
        print("EXIT ;)")
        self.close()
    
    def btnSunFunction(self):
        # f -string format

        info_str=("\n\nName : { }\n\
Mass : { } x 10^24 kg\n\
Diameter : { } x 10^6 km\n\
Density : { } kg/m^3\n\
Gravity : { } m/s^2\n\
Length of Day : { } h\n\
Distance from Sun : { } km\n\
Orbital Period : { } days\n\
Orbital Eccentricity : { }°\n\
Axial tilt :  { }°\n\
Mean Temperature : { }°C\n\
Number of Moons : { }\n\
Ring System : { }\n\
Global Magnetic Field : { }\n\
=========================")
        self.infoBrowser.setPlainText(info_str)
        
    def getSolarSystemInfo(self):
        self.planet_list = self.ss.getPlanetList()
        self.info_ss = self.ss.getPlanetInfo()
        planet_info = self.info_ss[1:]
        
    def btnPlanetFunction(self, num):
        planet = self.planet_list[num]
        info = self.info_ss[num]
    
        info_str=(f"\n\nName : {planet}\n\
Mass : {info[0]} x 10^24 kg\n\
Diameter : {info[1]} x 10^6 km\n\
Density : {info[2]} kg/m^3\n\
Gravity : {info[3]} m/s^2\n\
Length of Day : {info[4]} h\n\
Distance from Sun : {info[5]} km\n\
Orbital Period : {info[6]} days\n\
Orbital Eccentricity : {info[7]}°\n\
Axial tilt :  {info[8]}°\n\
Mean Temperature : {info[9]}°C\n\
Number of Moons : {int(info[10])}\n\
Ring System : {bool(info[10])}\n\
Global Magnetic Field : {bool(info[11])}\n\
=========================")
        self.infoBrowser.setPlainText(info_str)

    # MOUSE Click drag EVENT function
    def mousePressEvent(self, event):
        if event.button()==Qt.LeftButton:
            self.m_flag=True
            self.m_Position=event.globalPos()-self.pos() #Get the position of the mouse relative to the window
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  #Change mouse icon
    
    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:  
            self.move(QMouseEvent.globalPos()-self.m_Position)#Change window position
            QMouseEvent.accept()
    
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag=False
        self.setCursor(QCursor(Qt.ArrowCursor))
        
# CLOSE EVENT

    def closeEvent(self, event):
        message = QMessageBox.question(self, "Exit-이름", "Are you sure you want to quit?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if message == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()   
            
            
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    mainWindow = MainClass()
    
    mainWindow.show()
    
    app.exec()
    
    
# =============================================================================
# app = QApplication(sys.argv)
# 
# w = WindowClass()
# 
# w.show()
# 
# app.exec()
# =============================================================================
