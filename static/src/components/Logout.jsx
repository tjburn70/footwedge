import React from 'react';
import Button from '@material-ui/core/Button';

export const Logout = ({ logoutUser }) => (
  <Button color="inherit" onClick={logoutUser}>
    Logout
  </Button>
)
