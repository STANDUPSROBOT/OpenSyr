from motor_control import Motor_control
import math
import time
class OpenSryMain():
    def __init__(self):
        self.serynge_diam = None
        self.total_ml = None
        self.length_of_exp = None
        self.periode = None
        self.min_ml_precision  = None


        self.motor = Motor_control()
        #constants
        self.driver_subdivision_mode = self.motor.driver_sub_division
        self.screw_thread = self.motor.thread
        self.motor_angular_precision = self.motor.angle_per_step

        
        self.reset()

    def set_parameters(self,serynge_diam,total_ml,length_of_exp):
        self.serynge_diam = serynge_diam
        self.total_ml = total_ml
        self.length_of_exp = length_of_exp
        #deducing some parameters
        lin_precision = (self.screw_thread/360)*(self.motor_angular_precision/self.driver_subdivision_mode)
        self.min_ml_precision = (math.pi*(self.serynge_diam/2)**2) * lin_precision
        
        #Using the miniaml ml to compute the mminimal period of injections
        ml_per_sec = self.total_ml/self.length_of_exp
        self.periode = 1/(ml_per_sec/self.min_ml_precision)
      



    def reset(self):
        self.elapsed_steps = 0
        self.state_flag = 0

        #TODO: ajouter un bout de code qui permet de replacer la base au bon endroit



    def run(self):
        flow = self.total_ml/self.length_of_exp
        start_time = time.time()

        if(self.state_flag == 1):
            print("Restart after a stop")
            nb_injections_total = self.length_of_exp-(self.periode*self.elapsed_steps)/self.periode
            self.motor.freq_hz = 1/self.periode
            self.motor.move_step(nb_injections_total)
        else:
            print("Normal start")
            nb_injections_total = int(self.length_of_exp / self.periode)
            self.motor.freq_hz = 1/self.periode
            self.motor.move_step(nb_injections_total)

        print("---Finished experiemnt in %s seconds ---" % (time.time() - start_time))

    def stop(self):
        self.motor.stopFlag = True
        self.state_flag = 1
        self.update_elapsed_steps()

    def get_elapsed_time(self):
        self.update_elapsed_steps()
        seconds = self.periode*self.elapsed_steps
        m,s = divmod(seconds,60)
        h,_ = divmod(m,60)
        return int(m),int(s),int(h)


    def get_injected_volume(self):
        self.update_elapsed_steps()
        flow = self.total_ml/self.length_of_exp
        return flow*self.elapsed_steps


    def update_elapsed_steps(self):
        self.elapsed_steps = self.motor.curent_step


