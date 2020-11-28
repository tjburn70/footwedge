import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';

const useStyles = makeStyles((theme) => ({
  logoutButton: {
    marginLeft: '60%',
    color: 'inherit'
  },
}));

export const Logout = ({ logoutUser }) => {
  const classes = useStyles();
  return (
    <Button className={classes.logoutButton} onClick={logoutUser}>
      Logout
    </Button>
  );
}
