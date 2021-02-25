import '../App.css';
import React from 'react';
import Button from 'react-bootstrap/Button'
import Form from 'react-bootstrap/Form'
import axios from 'axios';
import info from '../info.png';

class Initialisation extends React.Component{
  constructor(props) {
    super(props);
    this.state ={value : false};
    
  }

  HandleSubmit(e){
    e.preventDefault();
    const config = {
      headers:{
          'Content-Type' : 'application/json',
      }
  };
    axios.post("/api/initialisation",0,config)
    window.location.href="/Home"   
  }
  

     render(){
      return  <div className="App-main" >
                <img src={info} className="Image-info" alt=""/> <br></br>
                <h1>Remove the syringe to start the initalisation</h1><br></br>
                <Form action="/api/initialisation" method="post" onSubmit={this.HandleSubmit}>
                <Button  variant="primary" onClick={e => this.setState({ value: true })} value={this.state.value}>Done</Button><br></br>  
                <Button  variant="primary" type="submit" disabled={!this.state.value}>Start initialisation</Button>  
                </Form>
              </div>
    }




  }

  export default Initialisation
;
