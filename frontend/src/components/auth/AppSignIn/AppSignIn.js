import React from 'react'
import { Button, Container, Col, Input, Form, FormGroup, Label, Row } from 'reactstrap'

const appSignInForm = props => {
  return (
    <Container>
      <Row>
        <Col xs="12" sm="12" md={{ size: 8, offset: 2 }} lg={{ size: 8, offset: 2 }}>
          <Form>
            <FormGroup>
              <Label for="email">Email address</Label>
              <Input type="email" id="email" placeholder="Enter email" autoComplete="email" />
            </FormGroup>
            <FormGroup>
              <Label for="password">Password</Label>
              <Input type="password" id="password" placeholder="Password" autoComplete="current-password" />
            </FormGroup>
            <Button color="primary">Login</Button>
          </Form>
        </Col>
      </Row>
    </Container>
  )
}

export default appSignInForm
