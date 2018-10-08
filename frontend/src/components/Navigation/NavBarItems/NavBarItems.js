import React from 'react'
import { Nav, NavItem } from 'reactstrap'
import AppNavLink from '../AppNavLink/AppNavLink'

const navBarItems = props => {
  return (
    <Nav>
      <NavItem>
        <AppNavLink to="/profile">Profile</AppNavLink>
      </NavItem>
      <NavItem>
        <AppNavLink to="/auth/logout">Logout</AppNavLink>
      </NavItem>
      <NavItem>
        <AppNavLink to="/auth/register">Register</AppNavLink>
      </NavItem>
      <NavItem>
        <AppNavLink to="/auth/login">Login</AppNavLink>
      </NavItem>
    </Nav>
  )
}

export default navBarItems
