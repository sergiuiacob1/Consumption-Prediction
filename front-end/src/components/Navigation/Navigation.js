import React from 'react';
import { Link } from 'react-router-dom'
import { Container, Row, Col, Nav } from 'react-bootstrap';
import './Navigation.scss';

export default class Navigation extends React.Component {
  constructor() {
    super();
    this.state = {};
  }

  render() {
    return (
      <Container>
        <Row>
          <Col>
            <Nav justify variant="tabs" defaultActiveKey={1}>
              <Nav.Item>
                <Nav.Link eventKey="1">
                  <Link to="/statistics">Statistics</Link>
                </Nav.Link>
              </Nav.Item>
              <Nav.Item>
                <Nav.Link eventKey="2">
                  <Link to="/model">Model</Link>
                </Nav.Link>
              </Nav.Item>
              <Nav.Item>
                <Nav.Link eventKey="3">
                  <Link to="/predict">Predict</Link>
                </Nav.Link>
              </Nav.Item>
            </Nav>
          </Col>
        </Row>
      </Container>
    )
  }
}
