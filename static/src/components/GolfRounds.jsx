import React, { useEffect } from 'react';
import Container from '@material-ui/core/Container';
import Grid from '@material-ui/core/Grid';
import PastGolfRoundContainer from './PastGolfRoundContainer';
import { getGolfRounds } from '../actions/api';

export const GolfRounds = (props) => {
  const {
    rounds,
    stats,
    userId,
  } = props.data;
  const dispatch = props.dispatch;
  const numRounds = rounds.allIds.length;

  useEffect(() => {
    if (userId) {
      dispatch(getGolfRounds(userId));
    }
  }, [userId, numRounds, dispatch]);

  return (
    <div>
      <Container>
        <Grid>
          <PastGolfRoundContainer
            rounds={rounds}
            stats={stats}
            dispatch={dispatch}
          />
        </Grid>
      </Container>
    </div>
  );
}
