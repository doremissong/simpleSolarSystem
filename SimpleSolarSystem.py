# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 22:47:23 2022

@author: 김미송
"""
import matplotlib.pyplot as plt
import numpy as np

from sunpy.coordinates import get_body_heliographic_stonyhurst
from astropy.time import Time
from datetime import date, timedelta

class SimpleSolarSystem:
    def __init__(self):
        
        self.planet_list = ['Sun','Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter','Saturn','Uranus','Neptune']
        self.info_ss = np.loadtxt('information.csv', delimiter=',', usecols=range(13))
        self.planet_info = self.info_ss[1:]

        self.planet_paths = ['image/sun.png','image/mercury.png', 'image/venus.png', 'image/earth.png', 'image/mars.png',
                 'image/jupiter.png', 'image/saturn.png', 'image/uranus.png', 'image/neptune.png']

        self.zoom = 1/10
        
        self.theta_earth = 360/365.2 
        self.dtime = date.today()
        
               
    def setZoom(self, zoom=1/7):
        self.zoom=zoom
    def getZoom(self):
        return self.zoom
    def getThetaEarth(self):
        return self.theta_earth
    def getPlanetList(self, n=0):
        return self.planet_list[n:]
    def getPaths(self):
        return self.planet_paths
    
    def setTime(self, yyyy=0,mm=0,dd=0,n=0):
        if yyyy==0:
            self.dtime =date.today() + timedelta(days=n)
        else:
            self.dtime = date(yyyy, mm, dd)
            
        astro_time= Time(self.dtime.isoformat()) 
        dt = (self.dtime - date(self.dtime.year,3,22)).days
        angle_earth = dt * self.getThetaEarth() #
        
        planet_coord = [get_body_heliographic_stonyhurst(this_planet, time=astro_time) for this_planet in self.getPlanetList(1)]
        angle = [this_coord.lon for this_coord in planet_coord] 
        return (angle_earth, angle)
    
    def getTime(self):
        return self.dtime
    
    def getXnY(self, yyyy=0,mm=0,dd=0,n=0):
        (angle_earth, angle) = self.setTime(yyyy, mm, dd, n)
        Radius = np.arange(2,18,2)
        Xs = [r*cos(np.deg2rad(180+angle_earth),a) for r, a in zip(Radius, angle)]
        Ys = [r*sin(np.deg2rad(180+angle_earth),a) for r, a in zip(Radius, angle)]
        Xs.insert(0, 0)
        Ys.insert(0, 0)
        return (Xs, Ys)
    
    def getSunInfo(self):
        sun = self.planet_list[0]
        info = self.info_ss[0]
        
        info_str=(f"\nName : {sun}\n\n\
Mass : {info[0]} x 10^24 kg\n\n\
Diameter : {info[1]} x 10^6 km\n\n\
Density : {info[2]} kg/m^3\n\n\
Gravity : {info[3]} m/s^2\n\n\
Length of Day : {info[4]} h\n\n\
Orbital Period : {info[6]} days\n\n\
Axial tilt :  {info[8]}°\n\n\
Mean Temperature : {info[9]}°C\n\n\
Number of planets : {int(info[10])}")
        return info_str
    

    def getPlanetInfo(self, num):
        planet = self.planet_list[num+1]
        info = self.info_ss[num+1]
        
        info_str=(f"\nName : {planet}\n\n\
Mass : {info[0]} x 10^24 kg\n\n\
Diameter : {info[1]} x 10^6 km\n\n\
Density : {info[2]} kg/m^3\n\n\
Gravity : {info[3]} m/s^2\n\n\
Length of Day : {info[4]} h\n\n\
Distance from Sun : {info[5]} km\n\n\
Orbital Period : {info[6]} days\n\n\
Orbital Eccentricity : {info[7]}°\n\n\
Axial tilt :  {info[8]}°\n\n\
Mean Temperature : {info[9]}\n\n\
Number of Moons : {int(info[10])}\n")
        info_str += "Ring System : Yes\n\n" if info[11] else "Ring System : No\n\n"
        info_str += "Global Magnetic Field : Yes\n\n" if info[12] else "Global Magnetic Field : No\n\n"
        return info_str

    
def cos(alpha, beta):   
    return (np.cos(alpha)*np.cos(beta)-np.sin(alpha)*np.sin(beta))
def sin(alpha, beta):  
    return (np.sin(alpha)*np.cos(beta)+np.cos(alpha)*np.sin(beta))


if __name__ == '__main__':
    ss = SimpleSolarSystem()
    (xs, ys) = ss.getXnY(n=0)
    
    plt.figure(figsize=(5,5))
    a = np.linspace(0,2*np.pi, 1000)
    x_c = np.sin(a)
    y_c = np.cos(a)
    for r in np.arange(2,18,2):
        plt.plot(r*x_c, r*y_c, color="gray")
    
    for this_planet, x,y in zip(ss.getPlanetList(), xs, ys):
        plt.plot(x, y, 'o', label=this_planet)
    plt.legend()
    plt.show()
    
    print(ss.getTime())
    