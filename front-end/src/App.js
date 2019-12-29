import React from 'react';
import { Route, Switch, BrowserRouter } from 'react-router-dom';
import Statistics from './containers/Statistics/Statistics.js';
import Model from './containers/Model/Model.js';
import Predict from './containers/Predict/Predict.js';
import NotFoundPage from './containers/NotFoundPage/index.js';
import './App.css';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      data: null,
    };
  }

  componentDidMount() {
    fetch('/train', {
      method: 'POST'
    })
      .then(res => res.json())
      .then(data => this.setState({data}))
  }
  
  render() {

    return (
      <BrowserRouter history="">
        <Switch>
          <Route exact path="/" component={Statistics}/>
          <Route exact path="/statistics" component={Statistics}/>
          <Route exact path="/Model" component={Model}/>
          <Route exact path="/predict" component={Predict}/>
          <Route path="" component={NotFoundPage} />
        </Switch>
      </BrowserRouter>
    );
  }
}

export default App;
