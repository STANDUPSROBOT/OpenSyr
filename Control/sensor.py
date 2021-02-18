# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 22:34:47 2021

@author: jerem
"""


DEBUG = True

if(not DEBUG):
    import RPi.GPIO as GPIO
    GPIO.cleanup()
    

class Sensor:

    def __init__(self):
        #TODO add the pins
        self.NO2 = 20
        self.NO1 = 21
        if(not DEBUG):
            self.setup()
        pass
        
    
    def setup(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.NO1, GPIO.IN, initial=GPIO.LOW)
        GPIO.setup(self.NO2, GPIO.IN, initial=GPIO.LOW)
        

    #TODO Return 1 if the sensor limit switch detect a rigth colision, 2 if a left, None if None
    def get_state(self):
        if(DEBUG):
            return 0
            
        if self.NO1>2:
            return 1
        elif self.NO2>2:
            return 2
        else:
            return 0