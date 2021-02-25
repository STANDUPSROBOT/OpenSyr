import React from 'react';
import '../App.css';
import Main from './Main';
import {Container, Row, Col} from 'reactstrap';
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'


class App extends React.Component{

  render() {
    
    return (<div className="App">
              <main>
                <div className="App-header" >
                  <Container fluid>
                      <Navbar bg="primary" variant="dark">
                      <Navbar.Brand href="home">Home</Navbar.Brand>
                        <Nav className="mr-auto">
                          <Nav.Link href="Initialisation">Initialisation</Nav.Link>  
                          <Nav.Link href="OpenSYR">OpenSYR</Nav.Link> 
                          <Nav.Link href="Running" disabled>Running</Nav.Link>                                                  
                        </Nav>
                      </Navbar>
                    <Row className="justify-content-md-center">
                      <Col></Col>
                      <Col xs={8}>
                        <Main/>
                      </Col>
                      <Col></Col>
                    </Row>
                  </Container>
                </div>
              </main>

              <div className="App-footer" >
              <footer>
                  <Container>
                      About the project : Projet realized by five UPSSITECH engineering school students in collaboration with the INSERM of Toulouse.  
                  </Container>
              </footer>
              </div>
              
            </div>
    );
  }
}

export default App;