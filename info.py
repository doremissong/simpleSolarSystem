# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 22:32:52 2022

@author: 김미송
"""

## 흠,, sss window에서 solarsystem  객체 선언하고
## info class에서도 선언해,,,
# 그냥 빼버려? 흠,,

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication
import sys  # We need sys so that we can pass argv to QApplication
import numpy as np
import webbrowser

from SolarSystem import SolarSystem


info_class = uic.loadUiType("info.ui")[0]

class InfoClass(QMainWindow, info_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('icon_buzz.png'))
        
        
        self.ss = SolarSystem()
        self.getSolarSystemInfo()
        
        self.btn_home.clicked.connect(self.btnHomeFunction)
        self.btn_more.clicked.connect(lambda: webbrowser.open('https://solarsystem.nasa.gov/solar-system/our-solar-system/overview/'))
        
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
# =============================================================================
#     def closeEvent(self, event):
#         message = QMessageBox.question(self, "Exit-이름", "Are you sure you want to quit?",
#                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
#         if message == QMessageBox.Yes:
#             event.accept()
#         else:
#             event.ignore()   
# =============================================================================
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    w = InfoClass()
    
    w.show()
    
    app.exec()