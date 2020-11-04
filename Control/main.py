from motor_control import Motor_control

class OpenSryMain():
    def __init__(self):
        self.serynge_diam = None
        self.periode = None
        self.flow = None
        self.length_of_exp = None
        self.elapsed_steps = 0 
        self.motor = Motor_control()
        self.state_flag = 0



    def reset(self):
        self.serynge_diam = None
        self.periode = None
        self.flow = None
        self.length_of_exp = None
        self.elapsed_steps = 0
        self.state_flag = 0

        #TODO: ajouter un bout de code qui permet de replacer la base au bon endroit



    def run(self):
        if(self.state_flag == 1):
            print("the machine was stopped")
            print("Do you want to reset or to start where you stopped")

            
        nb_injections_total = self.length_of_exp / self.periode
        self.motor.move_time_freq(self.flow,self.periode,nb_injections_total,self.serynge_diam)



    def stop(self):
        self.motor.stopFlag = True
        self.state_flag = 1
        self.update_elapsed_steps()


    def continue_experiment(self):
        if(self.state_flag != 1):
            print("You need to have a stopped experiment to continue it")
        nb_injections_total = self.length_of_exp-(self.periode*self.elapsed_steps)/self.periode
        self.motor.move_time_freq(self.flow,self.periode,nb_injections_total,self.serynge_diam)


    def update_elapsed_steps(self):
        self.elapsed_steps = self.motor.curent_step


