import React from 'react';
import { Switch, Route } from 'react-router-dom';

import Home from './Home';
import OpenSYR from './OpenSYR';
import Initialisation from './Initialisation';
import Running from './Running';
const Main = () => {
  return (
    <Switch> {/* The Switch decides which component to show based on the current URL.*/}
      <Route exact path='/' component={Home}></Route>
      <Route exact path='/home' component={Home}></Route>
      <Route exact path='/OpenSYR' component={OpenSYR}></Route>
      <Route exact path='/Initialisation' component={Initialisation}></Route>
      <Route exact path='/Running' component={Running}></Route>
    </Switch>
  );
}

export default Main;