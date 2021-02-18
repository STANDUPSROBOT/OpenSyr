from motor import Motor
from sensor import Sensor
from syringe import Syringe
import math
import time
DEBUG = True
from threading import Thread


class Experiement():
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
        #ellapsed step pas trop chiant à coder pour pas grand chose ?
        self.elapsed_steps = None
        self.nb_step_max = None
        self.state_flag = 0 # 1 if experiment stoped 2 if changing seringe 

        #Loading the syringe class
        self.syringe = Syringe();
        
        #Loading the motor class
        self.motor = Motor()
        self.motor.unlock()
        
        self.sensor = Sensor()

        self.flag_is_init_position = False # flag to check if we are on the init position
        
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
        lin_precision = (self.motor.thread/360)*(self.motor.angle_per_step/self.motor.driver_sub_division)
        #One motor step precision in ml
        self.min_ml_precision = (math.pi*(self.serynge_diam/2)**2) * lin_precision
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

        self.elapsed_steps = 0
        self.state_flag = 0
        self.motor.reset()
        self.flag_is_init_position = False



    ## -------------------------- Fonction d'init ------------------------------------- ##

    def init_position(self):
        #TODO Drive the motor to the init position (nb_step_max/2 i guess)
        init_step =int(self.nb_step_max/2)

        if self.sensor.get_state() == 1:
            self.motor.move_step(init_step,2)
            self.flag_is_init_position = True
        elif self.sensor.get_state() == 2:
            self.motor.move_step(-init_step,2)
            self.flag_is_init_position = True
        elif self.sensor.get_state() == 0:
            # while self.sensor.get_state()==0:
            #     self.motor.move_step(10,2)
            self.motor.move_step(init_step,2)
            self.flag_is_init_position = True
            


    ## -------------- Fonction de recherche du nombre de step entre les supports ----------------- ##
    def find_nb_step_max(self):
        #TODO Use the sensor and the motor to determine the minimum
        #if self.motor.unlock()==True:
        #On envoi le chariot contre un capteur si il n'y est pas déjà
        self.nb_step_max = 0
        if(DEBUG):
            self.nb_step_max = 1600*2
        else:
            while self.sensor.get_state()==0:
                self.motor.move_step(-10,2)

            #Si il est sur le capteur 1, on fais tourner le moteur dans le sens classique 
            if self.sensor.get_state() == 1:
                while self.sensor.get_state()!=2:
                    self.motor.move_step(1,2)
                    #et on incremente le nb de pas max 
                    self.nb_step_max = self.nb_step_max + 1

            #pareil pour le cas où le chariot est sur le capteur 2         
            elif self.sensor.get_state() == 2:
                while self.sensor.get_state()!=1:
                    self.motor.move_step(-1,2)
                    self.nb_step_max = self.nb_step_max + 1


        #We have the number of steps between both supports, we can set the value of steps to empty a syringe
        assert self.nb_step_max != 0
        self.syringe.set_total_step_syringe(self.nb_step_max/2)
            
            
    def reset_nb_step_max(self):
        self.nb_step_max = None




    def replace_seringe(self):
        #TODO freeze the experiment to let the user change the seringe
        self.state_flag = 2
        #il faut attendre que l'API renvoi que les serigues aient été sorties pour appeler init_position
        pass

    def run(self):
        #TODO start un thread qui appelle le bon nombre de fois step
        # if the experiment  has not been initialised (nb_step_max is None) we cant run it
        # the experiment should stop if the state flag is 1 or 2
        if self.flag_is_init_position == True:
            self.motor.reset_step_exp()
            

        thread = Thread(target = self.run_thread)
        thread.start()
        thread.join()

        ## J'avais pour idée de pas faire de continue_experiment, tu fais un thread qui fait avancer de ##
        ## tant de ml (calculés grace à total_step_syringe*ml_per_step) et qui s'arrete si le flag est à 2 ##
        ## Et ce thread sera relancé en boucle tant que self.total_ml < ellapsed_step*ml_per_step. ##
        ## note: il y a un risque fort qu'on atteigne le total_ml lorsqu'une seringue n'est pas finie, donc lancer en simultane
        ## un thread qui calcul regulierement self.total_ml == ellapsed_step*ml_per_step
        ## note: ml_per_step se calcule facilement
        

    def ellapsed_step_update_thread(self):
        pass




    def run_thread(self):

        while(True):

            ml = self.total_ml - self.get_injected_volume()
        

            if(ml>self.syringe.total_step_syringe*self.min_ml_precision):
                ml = self.syringe.total_step_syringe*self.min_ml_precision

            #print("ml serynge",self.syringe.total_step_syringe*self.min_ml_precision)
            print("ml =",ml)

            return_ =  self.move_ml(ml,self.serynge_diam)

            self.replace_seringe()
            #interface trucs 
            #
            if(DEBUG):
                #print("=========Sringe changing procedure===========")
                #self.init_position()
                self.motor.current_step = int(self.nb_step_max/2)
        
            else:
                while(not self.serynge_out):
                    time.sleep(1)
                self.serynge_out = False
                self.init_position()


                while(not self.new_serynge_in):
                    time.sleep(1)
                self.new_serynge_in = False


            if(return_<0):
                print("experiment finished")
                break




    def move_ml(self,ml,diametre_ser):
        Vol_pas = self.motor.thread*(self.motor.angle_per_step/360.0)*math.pi*(diametre_ser/2)**2
        nb_pas = ml/Vol_pas
        for pas in range(math.ceil(nb_pas)):
            self.motor.move_step(1,1)

            #print(self.get_syringe_percent(),"%")
            if(self.total_step_experiment == self.get_elapsed_steps()):
                return -1
            done = self.state_flag != 0 or self.sensor.get_state() !=0 or self.get_syringe_percent() > 0.98
            if(done):
                return pas


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


    #TODO check for 900 

    def get_syringe_percent(self):
        #TODO return 0 if the seringe is full 0.5 if half full ect ect  
        return ((self.motor.current_step- int(self.nb_step_max/2))/self.syringe.total_step_syringe)


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
        return self.min_ml_precision*self.get_elapsed_steps()

    def get_elapsed_steps(self):
        """
        the name is explicit ....
        """
        return self.motor.nb_step_exp
        
        


exp = Experiement()
print("SET PARAMS")
exp.set_parameters(serynge_diam=2,total_ml=50,length_of_exp=1)
print("FIND NB STEPS")
exp.find_nb_step_max()
print("INIT POS")
exp.init_position()
print("RUN")
exp.run()