import React from 'react';
import logo from './logo.svg';
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
    const { data } = this.state

    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <p>
            {data && data.message}
          </p>
        </header>
      </div>
    );
  }
}

export default App;
