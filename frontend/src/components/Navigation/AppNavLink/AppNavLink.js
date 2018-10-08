import React from 'react'
import { NavLink as RRNavlink } from 'react-router-dom'
import { NavLink } from 'reactstrap'

const appNavLink = props => {
  return (
    <NavLink tag={RRNavlink} {...props}>
      {props.children}
    </NavLink>
  )
}

export default appNavLink
