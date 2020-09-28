import React, { useEffect } from 'react';
import { Route } from 'react-router';
import Container from '@material-ui/core/Container';
import Grid from '@material-ui/core/Grid';
import Handicap  from './HandicapCard';
import { getHandicap } from '../actions/api';

export const PlayerProfile = (props) => {
  const {
    hasAccessToken,
    handicap,
  } = props.data;
  const dispatch = props.dispatch;

  useEffect(() => {
    if (hasAccessToken) {
      dispatch(getHandicap());
    }
  }, [hasAccessToken, handicap.index, dispatch]);

  return (
    <div>
      <Container>
        <Grid>
          <Handicap
            handicapIndex={handicap.index}
            calculatedOn={handicap.lastCalculated}
            enterRoundPath={`${path}/enter-round`}
          />
        </Grid>
      </Container>
    </div>
  );
}
