import time
from flask import Flask
from flask import request
from flask import jsonify, make_response
from experiment import Experiment

app = Flask(__name__)
exp = Experiment()



@app.route('/api/launch_experience',methods = ['GET','POST'])
def launch_experience():
    data = request.get_json()
    diameter =  float(data['diameter'])
    length =  float(data['length'])
    volume =  float(data['volume'])
    print("Diameter =",diameter)
    print("Len =",length)
    print("Volume =",volume)
    print("======================Set experience=====================")
    exp.set_parameters(serynge_diam=diameter,total_ml=volume,length_of_exp=length)
    print("======================Launch experience=====================")
    exp.run()
    #LAUNCH CODE FOR EXPERIENCE
    return make_response(jsonify({'is_ok': True}),1234)

@app.route('/api/initialisation',methods = ['GET','POST'])
def initialisation():
    print("Launch initialisation")
    #LAUNCH CODE FOR INITIALISATION
    exp.find_nb_step_max()
    exp.init_position()
    return make_response(jsonify({'is_ok': True}), 100)

@app.route('/api/stop_experience',methods = ['GET','POST'])
def stop_experience():
    print("FORCED STOP")
    #LAUNCH CODE FOR STOPPING THE EXPERIENCE
    exp.stop()
    return make_response(jsonify({'is_ok': True}), 5678)

@app.route('/api/end_experience',methods = ['GET','POST'])
def end_experience():
    print("The experience has finished")
    #LAUNCH CODE if there is a code when the experience end
    #pour le moment j'ai pas de code a la fin
    return make_response(jsonify({'is_ok': True}), 990)


@app.route('/api/change_syringe',methods = ['GET','POST'])
def change_syringe():
    print("Change the syringe")
    #LAUNCH CODE WHEN SYRINGE ARE CHANGED
    exp.set_serynge_in_place()
    return make_response(jsonify({'is_ok': True}), 9091)

@app.route('/api/get_progress',methods = ['GET','POST'])
def get_progress():
    #LAUNCH CODE TO GET THE PROGRESS
    progress = int(exp.get_experiment_percent()) # progress = return of the model function
    if(progress > 98):
        progress = 100      
    progress2 = int(exp.get_syringe_percent()*100)
    print("percent exp = ",progress)
    print("percent syringe = ",progress2)
    return jsonify(percentage_exp = progress,percentage_syr = progress2)

@app.route('/api/syringe_empty_soon',methods = ['GET','POST'])
def syringe_empty_soon():
    #LAUNCH CODE TO GET THE STATE OF THE SYRINGE
    soon_empty = exp.get_syringe_percent()>0.80 and exp.get_syringe_percent()<0.90; # soon_empty = return of the model function (boolean)
    #print("serynge percent =",exp.get_syringe_percent())
    return jsonify(state = soon_empty)

@app.route('/api/syringe_empty',methods = ['GET','POST'])
def end_of_course():   
    empty = exp.get_syringe_percent()>=0.98;#exp.is_end_of_course(); # soon_empty = return of the model function (boolean)   

    return jsonify(state = empty)

@app.route('/api/syringe_empty_code',methods = ['GET','POST'])
def syringe_empty():
    print("Syringe empty")
    #LAUNCH CODE WHEN SYRINGE ARE EMPTY
    return make_response(jsonify({'is_ok': True}), 9091)  


@app.route('/api/syringe_remove',methods = ['GET','POST'])
def syringe_remove():
    exp.set_serynge_removed()
    return make_response(jsonify({'is_ok': True}), 9091)  

 