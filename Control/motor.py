# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 00:45:02 2021

@author: jerem
"""

import time
import math as m

DEBUG = False

if(not DEBUG):
    import RPi.GPIO as GPIO
    GPIO.cleanup()



class Motor():

    def __init__(self):
        self.step_pin = 23
        self.dir_pin = 24
        self.enable_pin = 22
        self.freq_hz = 100
        self.thread = 0.8
        self.angle_per_step = 1.8
        self.driver_sub_division = 1

        self.stopFlag = False
        self.curent_step = 0
        if(not DEBUG):
            self.setup()
        

    def reset(self):
        self.stopFlag = False
        self.curent_step = 0


    def unlock(self):
        GPIO.output(self.enable_pin, True)

    def setup(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.enable_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.step_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.dir_pin, GPIO.OUT, initial=GPIO.LOW)

    def move_step(self,nb_step,mode):
        if(DEBUG):
            print("Starting injection of "+ str(nb_step)+" steps with period  = ",1/self.freq_hz," please wait")
            for i in range(nb_step):
                time.sleep(1/self.freq_hz)
                self.curent_step += i
        else:
            GPIO.output(self.enable_pin, False)
            direction = nb_step < 0
            nb_step = abs(nb_step)
            if(direction):
                GPIO.output(self.dir_pin, True)
            else:
                GPIO.output(self.dir_pin, False)

            for i in range(nb_step):
                if(self.stopFlag):
                    break
                GPIO.output(self.step_pin, True)
                if mode == 1:
                    time.sleep(1/self.freq_hz)
                    GPIO.output(self.step_pin, False)
                elif mode== 2:
                    time.sleep(1/1000)
                    GPIO.output(self.step_pin, False)
                if direction: 
                    self.curent_step -= i
                if else: 
                    self.curent_step += i


    def move_dist(self,dist_cm,time_sec = 1):
        steps = dist_cm / ((self.angle_per_step/360.0)*self.thread) 
        print(dist_cm)
        t = time_sec/steps
        for i in range(int(steps)):
            if(self.stopFlag):
                break
            self.move_step(1)
            time.sleep(t)


    def move_ml(self,ml,diametre_ser):
        Vol_pas = self.thread*(self.angle_per_step/360.0)*m.pi*(diametre_ser/2)**2
        nb_pas = ml/Vol_pas
        self.move_step(int(nb_pas))







# #=============TESTS================
# motor_control = Motor_control()
# #motor_control.move_ml(5,1.579)
# motor_control.move_time_freq(0.05,0.5,100,1.579)

# motor_control.unlock()
# GPIO.cleanup()