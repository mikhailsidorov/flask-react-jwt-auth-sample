import React from 'react'
import { Navbar, NavbarBrand } from 'reactstrap'
import NavBarItems from '../Navigation/NavBarItems/NavBarItems'

const appNavbar = props => {
  return (
    <Navbar color="dark">
      <NavbarBrand href="/">JWT Auth Example</NavbarBrand>
      <NavBarItems />
    </Navbar>
  )
}

export default appNavbar
