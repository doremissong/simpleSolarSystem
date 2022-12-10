
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from PyQt5.QtCore import QDate
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from SimpleSolarSystem import SimpleSolarSystem
import webbrowser

main_class = uic.loadUiType("main.ui")[0]
sss_class = uic.loadUiType("sss.ui")[0]
info_class = uic.loadUiType("info.ui")[0]

class MainClass(QMainWindow, main_class):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('image/earth.png'))
        
        self.btn_SSS.clicked.connect(self.btnSSSFunction)
        self.btn_info.clicked.connect(self.btnInfoFunction)
        self.btn_exit.clicked.connect(self.btnExitFunction)

    def btnSSSFunction(self):
        self.w = SSSClass()
        if self.w.isVisible():
            self.w.hide()
            self.show()
        else:
            self.hide()
            self.w.show()       
    
    def btnInfoFunction(self):
        self.w = InfoClass()
        if self.w.isVisible():
            self.w.hide()
            self.show()
        else:
            self.hide()
            self.w.show() 
        
    def btnExitFunction(self, event):
        self.close()
        
    def closeEvent(self, event):
        message = QMessageBox.question(self, "Simple Solar System", "Are you sure you want to quit?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if message == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
            

class SSSClass(QMainWindow, sss_class): 
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('image/earth.png'))
   
        self.fig = plt.Figure(facecolor='black')
        self.canvas = FigureCanvas(self.fig)
        self.ss = SimpleSolarSystem()
        
        self.btn_home.clicked.connect(self.btnHomeFunction)
        self.btn_reset.clicked.connect(self.btnResetFunction)
        self.btn_plus.clicked.connect(lambda: self.btnPlusNMinusFunction(step=1))
        self.btn_minus.clicked.connect(lambda: self.btnPlusNMinusFunction(step=-1))
        self.dateEdit.dateChanged.connect(lambda: self.dateEditFunction(True))
        self.dateEdit.setDate(QDate.currentDate())
        
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
            
    def plotSolarSystem(self, yyyy=0,mm=0,dd=0):
        
        self.graph_verticalLayout.removeWidget(self.canvas)
        self.fig = plt.Figure(facecolor='black',figsize=(8,2))
        
        self.canvas = FigureCanvas(self.fig)
        
        self.graph_verticalLayout.addWidget(self.canvas)
        self.graph_verticalLayout.setContentsMargins(0, 0, 0, 0)
    
        ax = self.fig.add_subplot(111)
        ax.set_xlim(-17,17)
        ax.set_ylim(-17,17)
        ax.set_aspect('equal')
        ax.margins(0,0)
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
        ax.patch.set_facecolor('#000000')
        
        theta = np.linspace(0,2*np.pi, 1000)
        x_c = np.sin(theta)
        y_c = np.cos(theta)
        for r in np.arange(2,18,2):
            ax.plot(r*x_c, r*y_c, color="gray")
        (xs,ys)=self.ss.getXnY(yyyy=yyyy, mm=mm, dd=dd)         
        for x, y, path in zip(xs, ys, self.ss.getPaths()):
            ab = AnnotationBbox(getImage(path,self.ss.getZoom()), (x, y), frameon=False)
            ax.add_artist(ab)
        self.canvas.draw()
        return ax

    def closeEvent(self, event):
        message = QMessageBox.question(self, "Simple Solar System", "Are you sure you want to quit?",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if message == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()     
            
def getImage(path, zoom=1):
    return OffsetImage(plt.imread(path), zoom=zoom)
 
        
class InfoClass(QMainWindow, info_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('image/earth.png'))
        self.ss = SimpleSolarSystem()
        
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
        info_str=self.ss.getSunInfo()
        self.infoBrowser.setPlainText(info_str)
        
    def btnPlanetFunction(self, num):
        info_str = self.ss.getPlanetInfo(num)
        self.infoBrowser.setPlainText(info_str)

    def closeEvent(self, event):
        message = QMessageBox.question(self, "Simple Solar System", "Are you sure you want to quit?",
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