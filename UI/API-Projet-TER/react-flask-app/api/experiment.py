from motor import Motor
from sensor import Sensor
from syringe import Syringe
import math
import time
DEBUG = True
from threading import Thread


class Experiment():
    def __init__(self):
        
        #===Experiment parameters===
        
        self.total_ml = None
        #
        self.length_of_exp = None
        #
        self.min_ml_precision  = None
        #
        self.total_step_experiment = None
        #===
        self.elapsed_steps = None
        self.nb_step_max = None
        self.state_flag = 0 # 1 if experiment stoped 2 if changing seringe 

        #Loading the syringe class
        self.syringe = Syringe()
        
        #Loading the motor class
        self.motor = Motor()
        self.motor.unlock()
        
        self.sensor = Sensor()
        self.sensor.setup()

        self.flag_is_init_position = False # flag to check if we are on the init position
        self.is_initialised = False
        #flags pour l'interface
        self.serynge_out = False
        self.new_serynge_in = False
        self.reset()


    def set_parameters(self,serynge_diam,total_ml,length_of_exp):
        """
        Method called by the UI to set the experiment parameters
        """

        self.serynge_diam = serynge_diam
        self.total_ml = total_ml
        self.length_of_exp = length_of_exp
        #deducing some parameters
        # One motor step precision in mm
        lin_precision = (self.motor.angle_per_step/360)*(self.motor.thread/self.motor.driver_sub_division)
        #One motor step precision in ml
        self.min_ml_precision = (math.pi*(self.serynge_diam/2)**2) * lin_precision
        #nombre de step à faire pour tant de ml
        self.total_step_experiment = int(self.total_ml/self.min_ml_precision)
        #Using the minimal ml to compute the mminimal period of injections
        #ml per secondes that we have to inject to meet injection of "total_ml" during "length_of_exp"
        ml_per_sec = self.total_ml/self.length_of_exp
        # setting minimal frequence of injection
        self.motor.freq_hz=(ml_per_sec/self.min_ml_precision)
        print()

    def reset(self):
        """
        Method to reset the experiment
        """
        print("==================RESET=======================")
        self.state_flag = 0
        self.motor.reset()
        self.flag_is_init_position = False
        
        print('self.motornb_step_exp=',self.motor.nb_step_exp)
        print("==================END  RESET=======================")

    def stop(self):
        """
        emergency stop
        Freeze the motor
        """
        self.motor.stopFlag = True
        self.state_flag = 1
        self.motor.unlock()


    ## -------------------------- Fonction d'init ------------------------------------- ##

    def init_position(self):
        print("init_position() -> start")
        #TODO Drive the motor to the init position (nb_step_max/2 i guess)
        init_step =self.nb_step_max
        if self.sensor.get_state() == 2:
            self.motor.move_step(-init_step,2)
            self.flag_is_init_position = True
        elif self.sensor.get_state() == 0:
            while self.sensor.get_state()==0:
                self.motor.move_step(-2,2)
            self.flag_is_init_position = True
        elif self.sensor.get_state() == 1:
            self.is_initialised = True
        self.motor.current_step = 0
        self.state_flag = 0
        print("init_position() -> stop")
        


    ## -------------- Fonction de recherche du nombre de step entre les supports ----------------- ##
    def find_nb_step_max(self):
        #TODO Use the sensor and the motor to determine the minimum
        #if self.motor.unlock()==True:
        #On envoi le chariot contre un capteur si il n'y est pas deja
        self.nb_step_max = 0
        self.motor.stopFlag = False

        while self.sensor.get_state()==0:
            self.motor.move_step(1,2)
            #Si il est sur le capteur 1, on fais tourner le moteur dans le sens classique 
        if self.sensor.get_state() == 1:
            while self.sensor.get_state()!=2:
                self.motor.move_step(1,2)
                #et on incremente le nb de pas max 
                self.nb_step_max = self.nb_step_max + 1


        #pareil pour le cas ou le chariot est sur le capteur 2         
        elif self.sensor.get_state() == 2:
            while self.sensor.get_state()!=1:
                self.motor.move_step(-1,2)
                self.nb_step_max = self.nb_step_max + 1


        #We have the number of steps between both supports, we can set the value of steps to empty a syringe
        assert self.nb_step_max != 0
        self.syringe.set_total_step_syringe(self.nb_step_max)
        #print("step max syringe: " + str(self.syringe.total_step_syringe))
            
            
    def reset_nb_step_max(self):
        self.nb_step_max = None




    def replace_seringe(self):
        self.state_flag = 2

    def run(self):
        # if the experiment  has not been initialised (flag_is_init_position is False) we cant run it
        # the experiment should stop if the state flag is 1 or 2
        if self.flag_is_init_position == True:
            self.motor.reset_step_exp()
        
        thread = Thread(target = self.run_thread)
        thread.start()
        thread.join()



    def run_thread(self):
        self.motor.reset_step_exp()
        while(True):
            print("total_ml: " + str(self.total_ml))
            print("get_elapsed_step: " + str(self.get_elapsed_steps()))
            print("get_injected_volume: " + str(self.get_injected_volume()))
            ml = self.total_ml - self.get_injected_volume()
            


            if(ml>self.syringe.total_step_syringe*self.min_ml_precision):
                print("if seringue sup au volume ")
                print("volume dans la seringue: " + str(self.syringe.total_step_syringe*self.min_ml_precision))
                ml = self.syringe.total_step_syringe*self.min_ml_precision
    
            #print("ml serynge",self.syringe.total_step_syringe*self.min_ml_precision)
            print("ml =",ml)
            
            return_ =  self.move_ml(ml,self.serynge_diam)
            if(return_ == 0):

                print(self.get_injected_volume())
                exit(0)

            #Interface
            #print("pulling syringe out ...")
            #time.sleep(3)
            #self.serynge_out=True
            while(not self.serynge_out):
                time.sleep(1)
            self.serynge_out = False
            self.init_position()
            
            #print("put new syringe int ...")
            #time.sleep(3)
            #self.new_serynge_in=True
            while(not self.new_serynge_in):
                time.sleep(1)
            self.new_serynge_in = False
            self.state_flag = 0


            if(return_<0):
                print("experiment finished")
                self.exp_finished = True
                self.motor.unlock()

                break
            



    def move_ml(self,ml,diametre_ser):
        Vol_pas = self.motor.thread*(self.motor.angle_per_step/360.0)*math.pi*(diametre_ser/2)**2
        print("vol_pas: " +str(Vol_pas))
        nb_pas = ml/Vol_pas
        print("nb_pas = ",math.ceil(nb_pas))
        for pas in range(int(math.ceil(nb_pas))):
            self.motor.move_step(1,1)
            if(self.total_step_experiment == self.get_elapsed_steps()):
                return -1
            #print(self.state_flag != 0)
            #print('sensor =',self.sensor.get_state() !=0)
            #print(self.get_syringe_percent() > 1)
            done = self.state_flag != 0 or self.sensor.get_state() ==2 or self.get_syringe_percent() > 0.98
            if(done):
                print("done")
                return pas
        print("test return")
        return pas






    #TODO check for 900 

    def get_syringe_percent(self):
        #TODO return 0 if the seringe is full 0.5 if half full ect ect
        #test = ((int(self.nb_step_max)-self.motor.current_step)/self.syringe.total_step_syringe)
        test = self.motor.current_step/self.syringe.total_step_syringe
        print('self.motor.current_step = ',self.motor.current_step)
        print('self.syringe.total_step_syringe = ',self.syringe.total_step_syringe)

        return test
        #return self.motor.current_step/self.syringe.total_step_syringe

    def get_experiment_percent(self):
        return (self.get_injected_volume()/self.total_ml)*100

    def get_elapsed_time(self):
        """
        Function for the UI guys
        """
        seconds = self.periode*self.get_elapsed_steps()
        m,s = divmod(seconds,60)
        h,_ = divmod(m,60)
        return int(m),int(s),int(h)

    def get_injected_volume(self):
        """
        return the volume already injected
        """
        print('self.min_ml_precision',self.min_ml_precision)
        print('self.get_elapsed_steps()',self.get_elapsed_steps())

        return self.min_ml_precision*self.get_elapsed_steps()

    def get_elapsed_steps(self):
        """
        the name is explicit ....
        """
        return self.motor.nb_step_exp
        
        
    def is_end_of_course(self):
        return self.sensor.get_state() !=0 


    def set_serynge_removed(self):
        self.serynge_out = True

    def set_serynge_in_place(self):
        self.new_serynge_in = True

    def is_ready(self):
        return not(self.nb_step_max == None) and self.state_flag != 1



# exp = Experiment()
# exp.find_nb_step_max()
# exp.init_position()
# exp.set_parameters(serynge_diam=2,total_ml=50,length_of_exp=100)
# exp.run()