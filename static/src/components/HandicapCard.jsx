import React from 'react';
import { Link } from 'react-router-dom';
import { makeStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';

const useStyles = makeStyles({
  handicapContext: {
    flex: 1,
  },
});

export default function Handicap({ handicapIndex, calculatedOn, enterRoundPath }) {
  const classes = useStyles();

  return (
    <React.Fragment>
      <Typography component="h2" variant="h6" color="primary" gutterBottom>
        Player Handicap:
      </Typography>
      <Typography component="p" variant="h4">
        {handicapIndex ? handicapIndex : "N/A"}
      </Typography>
      <Typography color="textSecondary" className={classes.handicapContext}>
        {calculatedOn ? "as of "+calculatedOn : ""}
      </Typography>
      <Button
        variant="contained"
        color="primary"
        component={Link}
        to={enterRoundPath}>
        Enter a Past Round
      </Button>
    </React.Fragment>
  );
}
