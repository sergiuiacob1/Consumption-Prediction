import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';

export default class Statistics extends React.Component {
  constructor() {
    super();
    this.state = {
    };
  }

  componentDidMount() {
    fetch('/api/models')
      .then(res => res.json())
      .then(res => {
        console.log(res);
      })
  }
  

  render() {
    return (
      <Container>
        <Row>
          <Col>
            <div>PULA</div>
          </Col>
        </Row>
      </Container>
    );
  }
}
