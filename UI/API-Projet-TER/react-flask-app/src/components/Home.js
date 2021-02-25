
import '../App.css'
import React from 'react'
import {Container} from 'reactstrap'

import upssitech from '../logo_upssitech.png';
import inserm from '../inserm.png';

class Home extends React.Component{
  constructor(props) {
    super(props);
    this.state = {
      currentTime: 0
    };
  }

    render(){
      
      
      return (        
        <div className="App-main" >
        <Container>              
          <p>
            Welcome to the OpenSYR project 
          </p><br></br>
          
          <img src={upssitech} alt="" className="Image-logo"/> <br></br><br></br><br></br> 
          <img src={inserm} alt="" className="Image-logo"/> 
                  
        </Container>
        </div>
      );
    }
  }

  export default Home
;
