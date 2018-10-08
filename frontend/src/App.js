import React, { Component } from 'react'
import { Route, Switch } from 'react-router-dom'
// import SignInForm from './components/SignInForm/SignInForm'
import AppLayout from './components/AppLayout/AppLayout'
import AppSignIn from './components/auth/AppSignIn/AppSignIn'
// import AppLogout from './components/auth/AppLogout/AppLogout'
// import AppRegister from './components/auth/AppRegister/AppRegister'
// import AppUserProfile from './components/AppUserProfile/AppUserProfile'

class App extends Component {
  render() {
    let routes = (
      <Switch>
        <Route path="/auth/login" component={AppSignIn} />
        {/* <Route path="/auth/register" component={asyncAuth} /> */}
        {/* <Redirect to="/" /> */}
      </Switch>
    )

    // if (this.props.isAuthenticated) {
    //   let routes = (
    //     <Switch>
    //       {/* <Route path="/auth/login" component={AppSignIn} /> */}
    //       <Route path="/auth/logout" component={AppLogout} />
    //       <Route path="/auth/register" component={AppRegister} />
    //       <Route path="/profile" exact component={AppUserProfile} />
    //       {/* <Redirect to="/" /> */}
    //     </Switch>
    //   )
    // }
    return (
      <React.Fragment>
        <AppLayout>{routes}</AppLayout>
      </React.Fragment>
    )
  }
}

export default App
