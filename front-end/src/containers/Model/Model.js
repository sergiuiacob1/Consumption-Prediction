import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';

export default class Model extends React.Component {
  constructor() {
    super();
    this.state = {
    };
  }
  
  render() {
    return (
      <Container>
        <Row>
          <Col>
            <div>IN</div>
          </Col>
        </Row>
      </Container>
    );
  }
}
