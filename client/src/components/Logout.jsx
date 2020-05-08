import React from 'react';
import { Redirect } from 'react-router-dom';
import Button from '@material-ui/core/Button';

export const Logout = ({ logoutUser }) => (
  <Button color="inherit" onClick={logoutUser}>
    Logout
  </Button>
)
