import '../App.css';
import React from 'react';
import ProgressBar from 'react-bootstrap/ProgressBar'
import Button from 'react-bootstrap/Button'
import Form from 'react-bootstrap/Form'
import Modal from 'react-bootstrap/Modal'
import axios from 'axios';

class Running extends React.Component{
  constructor(props) {
    super(props);
    // expProgress = percentage of the progress bar experience (sent by the model)
    // syrProgress = percentage of the progress bar syringe (sent by the model)
    // show = boolean to know if we have to show the pop up of syringe change
    // show2 = boolean to know if we have to show the second pop up of syringe change
    // show3 = boolean to know if we have to show the pop up of experience stop
    // syringe_soon_empty = boolean to konw if we have to show the pop up of syringe empty (sent by the the model)     
    // syringe empty = boolean to know if we are at the end of the syringe (sent by the model)
    // block_pop_up = boolean to stop the soon empty pop up
    // block_pop_up2 = boolean to stop the empty pop up
    // name,temp and actual_name are for the pause/unpause button
    this.state={expProgress : 0,syrProgress : 0, show : false, show2 : false,show3 : false,syringe_soon_empty : false,syringe_empty : false, block_pop_up : false, block_pop_up2 : false, name : "Pause", temp : "Unpause",actual_name : 1};
    //ALLOW TO US KEY WORD "THIS" IN THOSE FUNCTIONS
    this.HandleSubmit = this.HandleSubmit.bind(this);  
    this.HandleSubmit2 = this.HandleSubmit2.bind(this); 
    this.HandleSubmit3 = this.HandleSubmit3.bind(this);
    this.HandleClose = this.HandleClose.bind(this);
    this.HandleClose2 = this.HandleClose2.bind(this);  
    this.HandleClose3 = this.HandleClose3.bind(this);  
    this.HandleClose4 = this.HandleClose4.bind(this); 
    this.HandleClose5 = this.HandleClose5.bind(this);
    this.HandleClose6 = this.HandleClose6.bind(this);        
  }
  
  // EXECUTE REQUESTS ALL SECONDS TO GET INFORMATION
  componentDidMount() { 
    setInterval(() => {
      const config = {
        headers:{
            'Content-Type' : 'application/json',
        }
      };
      // REQUEST PERCENTAGE OF EXPERIENCE PROGRESS FOR THE PROGRESS BAR
      axios.post("/api/get_progress", 0,config)
      .then(response => {
        this.setState({ expProgress: parseInt(response.data.percentage_exp) }) 
        this.setState({ syrProgress: parseInt(response.data.percentage_syr) }) 
      })
      if(!this.state.block_pop_up){
        // REQUEST TO KNOW IF THE SYRINGE IS SOON EMPTY      
        axios.post("/api/syringe_empty_soon",0,config)
        .then(response=>{
          this.setState({ syringe_soon_empty: response.data.state }) 
          
        })
      }
      if(!this.state.block_pop_up2){
        // REQUEST TO KNOW IF IT IS THE END OF COURSE
        axios.post("/api/syringe_empty",0,config)
        .then(response=>{
          this.setState({ syringe_empty: response.data.state })        
        })   
      }   
    }, 1000);                    
  }
  
  //STOP EXPERIENCE (stage 1)
  HandleSubmit(e){
    e.preventDefault();   
    this.setState({show3 : true});    
  }
  //STOP EXPERIENCE (stage 2-1)
  HandleClose3(e){
    e.preventDefault();
    this.setState({show3 : false});
    this.Stop_experience();
  }
  //STOP EXPERIENCE (stage 2-2)
  HandleClose4(e){
    e.preventDefault();
    this.setState({show3 : false});    
  }
  //STOP EXPERIENCE (stage 3)
  Stop_experience(){
    const config = {
      headers:{
          'Content-Type' : 'application/json',
      }
  };
    axios.post("/api/stop_experience", 0,config)
    .then(response => {
        console.log(response)
    })
    window.location.href="/Home"
  }

  //END EXPERIENCE
  HandleSubmit2(e){
    e.preventDefault();
    const config = {
      headers:{
          'Content-Type' : 'application/json',
      }
  };
    axios.post("/api/end_experience", 0,config)
    .then(response => {
        console.log(response)
    })
    window.location.href="/Home"
  }

  //CHANGE SYRINGE (stage 1)
  HandleSubmit3(e){
    e.preventDefault();
    //Launch code before removing syringe
    this.Stop_for_remove();
    this.setState({syringe_empty : false});     
    this.setState({show : true});           
  }
  
  Stop_for_remove(){
    const config = {
      headers:{
          'Content-Type' : 'application/json',
      }
    }; 
    axios.post("/api/stop_for_remove", 0,config)
    .then(response => {
        console.log(response)
    })
  }

  //CHANGE SYRINGE (stage 2)
  HandleClose(e){
    e.preventDefault();
    this.setState({show : false});
    this.Syringe_remove();
    this.setState({show2 : true});
  }

  Syringe_remove(){
    const config = {
      headers:{
          'Content-Type' : 'application/json',
      }
    }; 
    axios.post("/api/syringe_remove", 0,config)
    .then(response => {
        console.log(response)
    })
  }
  //CHANGE SYRINGE (stage 3)
  HandleClose2(e){
    e.preventDefault();    
    this.setState({show2 : false}); 
    this.Change_syringe();
    this.setState({block_pop_up : false});
    this.setState({block_pop_up2 : false});  
  }
  //CHANGE SYRINGE (stage 4)
  Change_syringe(){
    const config = {
      headers:{
          'Content-Type' : 'application/json',
      }
    }; 
    axios.post("/api/change_syringe", 0,config)
    .then(response => {
        console.log(response)
    })    
  }
  // SYRINGE SOON EMPTY
  HandleClose5(e){
    e.preventDefault();    
    this.setState({syringe_soon_empty : false});
    this.setState({block_pop_up : true});      
  }
  // SYRINGE EMPTY
  HandleClose6(e){
    e.preventDefault();   
    this.setState({syringe_empty : false});    
    this.Syringe_empty();
    this.setState({block_pop_up2 : true})
    this.setState({show : true});
  }

  Syringe_empty(){
    const config = {
      headers:{
          'Content-Type' : 'application/json',
      }
    };
    axios.post("/api/syringe_empty_code", 0,config);    
  }


  //Gestion du pause/unpause
  changeValue(e){
    e.preventDefault();
    //pause
    if(this.state.actual_name===1){
        var tempo = this.state.name;
        this.setState({name : this.state.temp});
        this.setState({temp : tempo});
        this.setState({actual_name : 2});
        this.pause_request();
    //unpause
    }else if(this.state.actual_name===2){
        tempo = this.state.temp;
        this.setState({temp :this.state.name});;
        this.setState({name : tempo});
        this.setState({actual_name : 1});
        this.unpause_request();
    }
  }

  pause_request(){
    const config = {
      headers:{
          'Content-Type' : 'application/json',
      }
    };
    axios.post("/api/pause_request", 0,config); 
  }

  unpause_request(){
    const config = {
      headers:{
          'Content-Type' : 'application/json',
      }
    };
    axios.post("/api/unpause_request", 0,config); 
  }

    render(){
      return <div className="App-main" >        
                <br></br>                 
                <h1>The experiment is running</h1><br></br><br></br><br></br>
                <h2>Experiment progress</h2>
                <ProgressBar variant="warning" now={this.state.expProgress} label={`${this.state.expProgress}% experiment progress`} />
                <br></br><h2>Syringe progress</h2>
                <ProgressBar variant="warning" now={this.state.syrProgress} label={`${this.state.syrProgress}% syringes progress`} />
                
                <Form action="./api/stop_experience" method="post" onSubmit={this.HandleSubmit} >
                  <Button variant="danger" type="submit" disabled={this.state.expProgress >= 100}>STOP EXPERIMENT</Button><br></br> 
                </Form>
                
                <Button  variant="primary" type="submit" onClick={this.changeValue.bind(this)} >{this.state.name}</Button>

                <Form action="./api/change_syringe" method="post" onSubmit={this.HandleSubmit3} >
                  <Button variant="primary" type="submit" disabled={this.state.expProgress >= 100}>Change syringes</Button>
                </Form> 
                
                <Form action="./api/end_experience" method="post" onSubmit={this.HandleSubmit2} >
                  <Button variant="primary" type="submit" disabled={this.state.expProgress < 100}>End experiment</Button>
                </Form>

                
                <Modal show={this.state.show} >
                  <Modal.Header >
                    <Modal.Title>Syringes removing</Modal.Title>
                  </Modal.Header>
                  <Modal.Body>Done removing the syringes ?</Modal.Body>
                  <Modal.Footer>
                    <Button id="1" variant="secondary" onClick={this.HandleClose}>
                      YES
                    </Button>                    
                  </Modal.Footer>
                </Modal>

                 <Modal show={this.state.show2}>
                  <Modal.Header >
                    <Modal.Title>Place new syringes</Modal.Title>
                  </Modal.Header>
                  <Modal.Body>Done placing the syringes ?</Modal.Body>
                  <Modal.Footer>
                    <Button id="2" variant="secondary" onClick={this.HandleClose2}>
                      YES
                    </Button>                    
                  </Modal.Footer>
                </Modal> 

                <Modal show={this.state.show3}>
                  <Modal.Header>
                    <Modal.Title>Stop experiment</Modal.Title>
                  </Modal.Header>
                  <Modal.Body>Are you sure you want to stop the experiment ?</Modal.Body>
                  <Modal.Footer>
                    <Button id="3" variant="secondary" onClick={this.HandleClose3}>
                      YES
                    </Button>
                    <Button id="4" variant="secondary" onClick={this.HandleClose4}>
                      NO
                    </Button>                    
                  </Modal.Footer>
                </Modal> 
                <Modal show={this.state.syringe_soon_empty}>
                  <Modal.Header>
                    <Modal.Title>Syringes empty soon</Modal.Title>
                  </Modal.Header>
                  <Modal.Body>Warning : the syringes are soon empty !!!</Modal.Body>
                  <Modal.Footer>
                    <Button id="5" variant="secondary" onClick={this.HandleClose5}>
                      OK
                    </Button>                                       
                  </Modal.Footer>
                </Modal>
                <Modal show={this.state.syringe_empty}>
                  <Modal.Header>
                    <Modal.Title>Syringes empty</Modal.Title>
                  </Modal.Header>
                  <Modal.Body>Syringes are empty, press ok to continue</Modal.Body>
                  <Modal.Footer>
                    <Button id="6" variant="secondary" onClick={this.HandleClose6}>
                      OK
                    </Button>                                       
                  </Modal.Footer>
                </Modal>             
            </div>
      }

   
}   
export default Running;
