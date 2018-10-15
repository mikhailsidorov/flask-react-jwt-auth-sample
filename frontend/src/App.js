import React, { Component } from 'react'
import { Route, Switch } from 'react-router-dom'
import AppLayout from './components/AppLayout/AppLayout'
import AppSignIn from './components/auth/AppSignIn/AppSignIn'
import AppUserProfile from './components/AppUserProfile/AppUserProfile'

class App extends Component {
  render() {
    let routes = (
      <Switch>
        <Route path="/auth/login" component={AppSignIn} />
        <Route path="/user/1/profile" component={AppUserProfile} />
      </Switch>
    )
    return (
      <React.Fragment>
        <AppLayout>{routes}</AppLayout>
      </React.Fragment>
    )
  }
}

export default App
