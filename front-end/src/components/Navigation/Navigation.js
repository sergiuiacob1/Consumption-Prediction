import React from 'react';
import { NavLink } from 'react-router-dom'
import './Navigation.scss';

export default class Navigation extends React.Component {
  constructor() {
    super();
    this.state = {};
  }

  render() {
    return (
      <div className="container">
        <div className="row">
          <div className="col">
            <ul className="nav nav-pills nav-justified">
              <li className="nav-item active">
                <NavLink className="nav-link" to="/statistics" activeClassName="active">Statistics</NavLink>
              </li>
              <li className="nav-item">
                <NavLink className="nav-link" to="/model" activeClassName="active">Model</NavLink>
              </li>
              <li className="nav-item">
                <NavLink className="nav-link" to="/predict" activeClassName="active">Predict</NavLink>
              </li>
            </ul>
          </div>
        </div>
      </div>
    )
  }
}
