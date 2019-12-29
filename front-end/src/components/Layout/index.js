import React from 'react';
import { Link } from 'react-router-dom';
import './style.scss';

export default class Layout extends React.Component {
  constructor() {
    super();
    this.state = {
    };
  }
  render() {
    return (
      <div className="app-wrapper">
        <div className="header">
          	<Link className="tab" to="/predict">Predict</Link>
          	<Link className="tab" to="/statistics">Statistics</Link>
          	<Link className="tab" to="/model">Model</Link>
        </div>
        {this.props.children}
      </div>
    )
  }
}
