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


# test
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent, QCursor

sss_class = uic.loadUiType("sss_test.ui")[0]


class SSSClass(QMainWindow, sss_class): 
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('icon_buzz.png'))
   
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
    #     self..show_popup_ok('alert','This solar system is not like real one.')
        
    # def show_popup_ok(self, title: str, content: str):

    #     msg = QMessageBox()

    #     msg.setWindowTitle(title)

    #     msg.setText(content)

    #     msg.setStandardButtons(QMessageBox.Ok)

    #     result = msg.exec_()

    #     if result == QMessageBox.Ok:

    #         self.send_valve_popup_signal.emit(True)
        
    def btnHomeFunction(self):
        #w=MainClass()
        self.hide()
        #self.w.show()  
    
    def btnResetFunction(self):
        self.dateEdit.setDate(QDate.currentDate())
        #self.n = 0
        #self.plotSolarSystem()    #n=0
        #그리는 함수 호출
        
    def btnPlusNMinusFunction(self, step=0):
        date = self.dateEdit.date().addDays(step)
        self.dateEdit.setDate(date)
        #self.n += step
        #self.plotSolarSystem(n=self.n)
        
    def dateEditFunction(self, check):
        #date = QDate.currentDate()
        date = self.dateEdit.date()
        if check:
            self.plotSolarSystem(yyyy=date.year(),mm=date.month(),dd=date.day())
        #print(date.year(), date.month(), date.day())
# =============================================================================
# FUNCTION
    def plotSolarSystem(self, yyyy=0,mm=0,dd=0):
        print(1) #< -- 한번 그려지는지 체킈
        self.graph_verticalLayout.removeWidget(self.canvas)
        #self.ax.clear()
        self.fig = plt.Figure(facecolor='black')     #facecolor='black'
        self.fig.patch.set_alpha(0.1)
        
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