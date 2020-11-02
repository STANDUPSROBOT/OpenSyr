import RPi.GPIO as GPIO
import time
import math as m



class Motor_control():

    def __init__(self):
        self.step_pin = 23
        self.dir_pin = 24
        self.enable_pin = 22
        self.freq_hz = 60
        self.setup()

    def unlock(self):
        GPIO.output(self.enable_pin, True)

    def setup(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.enable_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.step_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.dir_pin, GPIO.OUT, initial=GPIO.LOW)

    def move(self,nbpas):
        GPIO.output(self.enable_pin, False)
        direction = nbpas < 0
        nbpas = abs(nbpas)
        if(direction):
            GPIO.output(self.dir_pin, True)
        else:
            GPIO.output(self.dir_pin, False)
        for i in range(nbpas):
            GPIO.output(self.step_pin, True)
            time.sleep(1/self.freq_hz)
            GPIO.output(self.step_pin, False)

    
    def convertir(self,periode, ml_periode, temps_total, diametre_ser):
        #calcul du volume expulsé par pas avec :
        #1 pas = 1.8°
        #pas_vis=2
        Vol_pas = 2*(1.8/360)*m.pi*(pow(diametre_ser,2)/4)
        #calcul du nombre de pas à faire lors d'une période si on donne les mL/periode 
        return  ml_periode/Vol_pas




#=============TESTS================
motor_control = Motor_control()
motor_control.move(nbpas = 1000)
for i in range(100):
    motor_control.move(nbpas = -1)
    time.sleep(0.1)
motor_control.unlock()