# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 18:01:07 2022

@author: 김미송
"""

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication
import sys  # We need sys so that we can pass argv to QApplication
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

from SolarSystem import SolarSystem


# ----------------------------------------------------

main_class = uic.loadUiType("main2_horizontal.ui")[0]
sss_class = uic.loadUiType("sss_test.ui")[0]
info_class = uic.loadUiType("info.ui")[0]

# ----------------------------------------------------

class WindowClass(QMainWindow, main_class):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('icon_buzz.png'))
        
        self.w = None
        
        #self.btn_RSS.clicked.connect(self.btnRSSFunction)
        self.btn_SSS.clicked.connect(self.btnSSSFunction)
        self.btn_info.clicked.connect(self.btnInfoFunction)
        self.btn_exit.clicked.connect(self.btnExitFunction)

    def closeEvent(self, event):
        message = QMessageBox.question(self, "Exit-이름", "Are you sure you want to quit?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if message == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
            
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

# ----------------------------------------------------
# (dateEdit 수정 전)
class SSSClass(QMainWindow, sss_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('icon_buzz.png'))
        
        #self.dateEdit
        
        self.fig = plt.Figure(facecolor='black')
        self.canvas = FigureCanvas(self.fig)
# =============================================================================
#여기부터
        self.ss = SolarSystem()
        self.n = 0
        self.plotSolarSystem(self.n)  #n=0
       
        # self.btn_home.clicked.connect()
        self.btn_reset.clicked.connect(self.btnResetFunction)
        self.btn_plus.clicked.connect(lambda: self.btnPlusNMinusFunction(step=1))   #매개변수있으면 lambda
        self.btn_minus.clicked.connect(lambda: self.btnPlusNMinusFunction(step=-1))
        #self.dateEdit.dateChanged.connect()
    
# =============================================================================
# FUNCTION
    def plotSolarSystem(self, n=0):
        #if redraw is True:
        self.graph_verticalLayout.removeWidget(self.canvas)
        #self.ax.clear()
        self.fig = plt.Figure(facecolor='black')
        self.canvas = FigureCanvas(self.fig)
        self.graph_verticalLayout.addWidget(self.canvas)

    # 기본틀
        ax = self.fig.add_subplot(111)  # 1행 1열로 나눈건 중 첫번재
        ax.set_xlim(-16,16)
        ax.set_ylim(-16,16)
        ax.set_aspect('equal')
        ax.axis('off')                         # 축 제거
        ax.padding=0
        ax.patch.set_facecolor('#3F3F3F')       # ax 배경 제거 
        theta = np.linspace(0,2*np.pi, 1000)
        x_c = np.sin(theta)
        y_c = np.cos(theta)
        for r in np.arange(1,17,2):
            ax.plot(r*x_c, r*y_c, color="gray")
# =============================================================================
        (xs,ys)=self.ss.getXnY(n=n)         
        for x, y, path in zip(xs, ys, self.ss.getPath()):
            ab = AnnotationBbox(getImage(path,self.ss.getZoom()), (x, y), frameon=False)
            ax.add_artist(ab)
        self.canvas.draw()
        return ax
# =============================================================================
        
    def btnResetFunction(self):
        #self.ax.clear()
        self.n = 0
        self.plotSolarSystem(n=self.n)    #n=0
        #그리는 함수 호출
        
    def btnPlusNMinusFunction(self, step=0):
        self.n += step
        self.plotSolarSystem(n=self.n)
        
# =============================================================================
# close 이벤트
#     def closeEvent(self, event):
#         message = QMessageBox.question(self, "Exit-이름", "Are you sure you want to quit?",
#                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
#         if message == QMessageBox.Yes:
#             event.accept()
#         else:
#             event.ignore()     
# =============================================================================
            
        
class InfoClass(QMainWindow, info_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('icon_buzz.png'))
        

    
        
    def closeEvent(self, event):
        message = QMessageBox.question(self, "Exit-이름", "Are you sure you want to quit?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if message == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()   
            

def getImage(path, zoom=1):
    return OffsetImage(plt.imread(path), zoom=zoom)

            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    w = WindowClass()
    
    w.show()
    
    app.exec()