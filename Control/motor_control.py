import RPi.GPIO as GPIO
import time



class Motor_control():

    def __init__(self):
        self.step_pin = 23
        self.dir_pin = 24
        self.enable_pin = 22
        self.freq_hz = 240
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




#=============TESTS================
motor_control = Motor_control()
motor_control.move(nbpas = 100)
for i in range(100):
    motor_control.move(nbpas = -1)
    time.sleep(0.1)
motor_control.unlock()