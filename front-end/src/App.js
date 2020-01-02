import React from 'react';
import { Route, Switch, BrowserRouter } from 'react-router-dom';
import Statistics from './containers/Statistics/Statistics.js';
import Navigation from './components/Navigation'
import Model from './containers/Model';
import Predict from './containers/Predict';
import NotFoundPage from './containers/NotFoundPage';
import './App.scss';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }
  
  render() {
    return (
      <BrowserRouter history="">
        <Route component={Navigation}/>
        <Switch>
          <Route exact path="/" component={Statistics}/>
          <Route exact path="/statistics" component={Statistics}/>
          <Route exact path="/model" component={Model}/>
          <Route exact path="/predict" component={Predict}/>
          <Route path="" component={NotFoundPage} />
        </Switch>
      </BrowserRouter>
    );
  }
}

export default App;
