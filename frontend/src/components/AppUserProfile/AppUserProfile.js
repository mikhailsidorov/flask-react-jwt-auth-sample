import React from 'react'
import { Button, Col, Container, Row, TabPane, ListGroup, ListGroupItem, Form, FormGroup } from 'reactstrap'

const appUserProfile = porps => {
  return (
    <div>
      <Container>
        <Row>
          <Col sm="10">
            <h1>User name</h1>
          </Col>
        </Row>
        <Row>
          <Col sm="3">
            <div className="text-center">
              <img
                src="http://ssl.gstatic.com/accounts/ui/avatar_2x.png"
                class="avatar img-circle img-thumbnail"
                alt="avatar"
              />
              <h6>Upload a different photo...</h6>
              <input type="file" class="text-center center-block file-upload" />
            </div>
            <hr />
            <br />
          </Col>
          <Col sm="9">
            <div class="tab-pane active" id="home">
              <Form class="form" action="##" method="post" id="registrationForm">
                <div class="form-group">
                  <Col xs="6">
                    <label for="first_name">
                      <h4>First name</h4>
                    </label>
                    <input
                      type="text"
                      class="form-control"
                      name="first_name"
                      id="first_name"
                      placeholder="first name"
                      title="enter your first name if any."
                    />
                  </Col>
                </div>

                <div class="form-group">
                  <Col xs="6">
                    <label for="last_name">
                      <h4>Last name</h4>
                    </label>
                    <input
                      type="text"
                      class="form-control"
                      name="last_name"
                      id="last_name"
                      placeholder="last name"
                      title="enter your last name if any."
                    />
                  </Col>
                </div>

                <div class="form-group">
                  <Col xs="6">
                    <label for="phone">
                      <h4>Phone</h4>
                    </label>
                    <input
                      type="text"
                      class="form-control"
                      name="phone"
                      id="phone"
                      placeholder="enter phone"
                      title="enter your phone number if any."
                    />
                  </Col>
                </div>

                <div class="form-group">
                  <Col xs="6">
                    <label for="mobile">
                      <h4>Mobile</h4>
                    </label>
                    <input
                      type="text"
                      class="form-control"
                      name="mobile"
                      id="mobile"
                      placeholder="enter mobile number"
                      title="enter your mobile number if any."
                    />
                  </Col>
                </div>
                <div class="form-group">
                  <Col xs="6">
                    <label for="email">
                      <h4>Email</h4>
                    </label>
                    <input
                      type="email"
                      class="form-control"
                      name="email"
                      id="email"
                      placeholder="you@email.com"
                      title="enter your email."
                    />
                  </Col>
                </div>
                <div class="form-group">
                  <Col xs="6">
                    <label for="email">
                      <h4>Location</h4>
                    </label>
                    <input
                      type="email"
                      class="form-control"
                      id="location"
                      placeholder="somewhere"
                      title="enter a location"
                    />
                  </Col>
                </div>
                <div class="form-group">
                  <Col xs="6">
                    <label for="password">
                      <h4>Password</h4>
                    </label>
                    <input
                      type="password"
                      class="form-control"
                      name="password"
                      id="password"
                      placeholder="password"
                      title="enter your password."
                    />
                  </Col>
                </div>
                <div class="form-group">
                  <Col xs="6">
                    <label for="password2">
                      <h4>Verify</h4>
                    </label>
                    <input
                      type="password"
                      class="form-control"
                      name="password2"
                      id="password2"
                      placeholder="password2"
                      title="enter your password2."
                    />
                  </Col>
                </div>
                <div class="form-group">
                  <Col xs="12">
                    <br />
                    <Button color="success" size="large" type="submit">
                      <i class="glyphicon glyphicon-ok-sign" /> Save
                    </Button>
                    <Button size="large" type="reset">
                      <i class="glyphicon glyphicon-repeat" /> Reset
                    </Button>
                  </Col>
                </div>
              </Form>
              <hr />
            </div>
          </Col>
        </Row>
      </Container>
    </div>
  )
}

export default appUserProfile
