import '../App.css';
import React from 'react';
import Button from 'react-bootstrap/Button'
import Form from 'react-bootstrap/Form'
import axios from 'axios';
import {Container} from 'reactstrap'

class OpenSYR extends React.Component{
  constructor(props) {
    super(props);
    this.state = { diameter: "",length : "", volume : "",};
    this.HandleSubmit = this.HandleSubmit.bind(this);     
  }

  handleChange = (event) => {
    this.setState({[event.target.name]: event.target.value});
  }

  HandleSubmit(e){
    e.preventDefault();
    //console.log("SUBMIT")
    const formData = new FormData();

    //Using this config in my request, the response gives me the mentioned waring of missing boundary
    const config = {
        headers:{
            'Content-Type' : 'application/json',
        }
    };

    formData.append("file", this.state.to_upload);

    axios.post("/api/launch_experience", this.state, config)
    .then(response => {
        console.log(response)
    })
    window.location.href="/Running"

  }
  
    render(){
      return <div className="App-form" >
              <div className="App-main" >
              <Container>              
                <p>
                  Insert the data of the experience 
                </p>                  
              </Container>
              </div>
                <Form action="./api/init_python" method="post" onSubmit={this.HandleSubmit} >
                  <Form.Group>
                        <Form.Row>
                          <Form.Label column="lg" lg={0}>
                            Syringe diameter
                          </Form.Label>
                              <Form.Control type="text" name="diameter" placeholder="Syringe diameter (cm)" value={this.state.diameter}
                              onChange={this.handleChange} />
                        </Form.Row>
                        <br />
                        <Form.Row>
                          <Form.Label column="lg" lg={0}>
                            Length of the experience
                          </Form.Label>
                            <Form.Control type="text" name="length" placeholder="Length of the experience (s)" value={this.state.length}
                            onChange={this.handleChange}/>
                        </Form.Row>
                        <br />
                        <Form.Row>
                          <Form.Label column="lg" lg={0}>
                            Volume to inject
                          </Form.Label>
                            <Form.Control type="text" name="volume" placeholder="Volume to inject (mL)" value={this.state.volume}
                            onChange={this.handleChange}/>
                        </Form.Row>
                    </Form.Group>
                  <Button variant="primary" type="submit" disabled={!this.state.diameter || !this.state.length || !this.state.volume}>Launch experience</Button>                  
                </Form>
              </div>
      }

   
}   
export default OpenSYR;
