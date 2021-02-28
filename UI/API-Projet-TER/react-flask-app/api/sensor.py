# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 22:34:47 2021

@author: jerem
"""
import time

DEBUG = False

if(not DEBUG):
    import RPi.GPIO as GPIO
    
    

class Sensor:

    def __init__(self):
        #TODO add the pins
        self.NO1 = 5
        self.NO2 = 26
        if(not DEBUG):
            self.setup()
        pass
        
    
    def setup(self):
        
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.NO1, GPIO.IN)
        GPIO.setup(self.NO2, GPIO.IN)
        

    #TODO Return 1 if the sensor limit switch detect a rigth colision, 2 if a left, None if None
    def get_state(self):
        if  GPIO.input(self.NO1)==GPIO.LOW:
            return 1
        elif GPIO.input(self.NO2)==GPIO.LOW:
            return 2
        else:
            return 0

