import React, { Fragment } from 'react'
import AppNavbar from '../Navigation/AppNavbar/AppNavbar'

const appLayout = props => {
  return (
    <Fragment>
      <AppNavbar />
      <main>{props.children}</main>
    </Fragment>
  )
}

export default appLayout
