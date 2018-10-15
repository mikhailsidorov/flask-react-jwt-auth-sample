import React from 'react'
import { Button, Container, Col, Input, Form, FormGroup, Label } from 'reactstrap'
import styles from './AppSignIn.module.css'

const appSignInForm = props => {
  return (
    <Container>
      <Col sm={{ size: 8, offset: 2 }} md={{ size: 6, offset: 3 }} lg={{ size: 6, offset: 3 }}>
        <div className={styles.formBox + ' d-flex flex-column'}>
          <Form className="mt-auto mb-auto">
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
        </div>
      </Col>
    </Container>
  )
}

export default appSignInForm
