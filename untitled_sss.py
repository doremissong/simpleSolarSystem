# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 10:39:03 2022

@author: 김미송
"""
#SSSwindow()

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication, QDate
import sys  # We need sys so that we can pass argv to QApplication
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

from SolarSystem import SolarSystem

sss_class = uic.loadUiType("sss_test.ui")[0]


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
        self.dateEdit.dateChanged.connect(self.dateEditFunction)
        self.dateEdit.setDate(QDate.currentDate())
# =============================================================================
# FUNCTION
    def plotSolarSystem(self, yyyy=0,mm=0,dd=0,n=0):
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
        (xs,ys)=self.ss.getXnY(n=n, yyyy=yyyy, mm=mm, dd=dd)         
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
        
    def dateEditFunction(self):
        #date = QDate.currentDate()
        date = self.dateEdit.date()
        self.plotSolarSystem(yyyy=date.year(),mm=date.month(),dd=date.day())
        print(date.year(), date.month(), date.day())
        
#        self.plotSolarSystem(yyyy=)
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
            
def getImage(path, zoom=1):
    return OffsetImage(plt.imread(path), zoom=zoom)
         
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    w = SSSClass()
    
    w.show()
    
    app.exec()