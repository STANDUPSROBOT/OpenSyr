from motor import Motor
from sensor import Sensor
import math
import time

class experiemnt():
    def __init__(self):
        
        #===Experiment parameters===
        self.serynge_diam = None
        self.total_ml = None
        #
        self.length_of_exp = None
        self.periode = None
        #
        self.min_ml_precision  = None
        #

        #===
        self.elapsed_steps = None
        self.nb_step_max = None
        self.state_flag = 0 # 1 if experiment stoped 2 if changing seringe 

        
        #Loading the motor class
        self.sensor = Sensor()
        self.motor = Motor()
        self.motor.unlock()

        self.flag_is_init_position = False # flag to check if we are on the init position


        self.reset()


    def set_parameters(self,serynge_diam,total_ml,length_of_exp):
        """
        Method called by the UI to set the experiment parameters
        """
        self.serynge_diam = serynge_diam
        self.total_ml = total_ml
        self.length_of_exp = length_of_exp
        #deducing some parameters
        lin_precision = (self.motor.thread/360)*(self.motor.angle_per_step/self.motor.driver_sub_division)
        self.min_ml_precision = (math.pi*(self.serynge_diam/2)**2) * lin_precision
        
        #Using the minimal ml to compute the mminimal period of injections
        ml_per_sec = self.total_ml/self.length_of_exp
        self.periode = 1/(ml_per_sec/self.min_ml_precision)
      

    def reset(self):
        """
        Method to reset the experiment
        """
        self.elapsed_steps = 0
        self.state_flag = 0
        self.motor.reset()


    def run(self):
        #TODO start un thread qui appelle le bon nombre de fois step
        # if the experiment  has not been initialised (nb_step_max is None) we cant run it
        # the experiment should stop if the state flag is 1 or 2
        pass


    def step(self):
        #TODO call motor step
        # and set self.flag_is_init_position to false 
        pass


    def init_position(self):
        #TODO Drive the motor to the init position (nb_step_max/2 i guess)
        pass


    def find_nb_step_max(self):
        #TODO Use the sensor and the motor to determine the minimum
        pass

    def replace_seringe(self):
        #TODO freeze the experiment to let the user change the seringe
        self.state_flag = 2
        pass

    def continue_experiment(self):
        #TODO continue the experiment after seringe replacement and position initialisation
        # check the flag flag_is_init_position
        #just update the number of ml we still have to inject using the elapsed_steps and then call the run method
        #DO NOT CALL RESET 
        pass

    def stop(self):
        """
        emergency stop
        Freeze the motor
        """
        self.motor.stopFlag = True
        self.state_flag = 1
        self.update_elapsed_steps()
        self.motor.unlock


    def get_seringe_percent(self):
        #TODO return 0 if the seringe is full 0.5 if half full ect ect  
        return 1.0


    def get_elapsed_time(self):
        """
        Function for the UI guys
        """
        self.update_elapsed_steps()
        seconds = self.periode*self.elapsed_steps
        m,s = divmod(seconds,60)
        h,_ = divmod(m,60)
        return int(m),int(s),int(h)

    def get_injected_volume(self):
        """
        return the volume already injected
        """
        self.update_elapsed_steps()
        flow = self.total_ml/self.length_of_exp
        return flow*self.elapsed_steps

    def update_elapsed_steps(self):
        """
        the name is explicit ....
        """
        self.elapsed_steps = self.motor.curent_step


