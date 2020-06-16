import React, { useEffect } from 'react';
import { Route } from 'react-router';
import Container from '@material-ui/core/Container';
import Grid from '@material-ui/core/Grid';
import { EnterRound } from './EnterRound';
import Handicap  from './HandicapCard';
import PastGolfRoundContainer from './PastGolfRoundContainer';
import { enterGolfRound, getHandicap, getGolfRounds } from '../actions/api';

export const PlayerProfile = (props) => {
  const {
    userId,
    errorMessage,
    handicap,
    rounds,
    stats,
  } = props.data;
  const { path } = props.match;
  const dispatch = props.dispatch;

  useEffect(() => {
    if (userId) {
      dispatch(getHandicap(userId));
    }
  }, [userId, handicap.index, dispatch]);

  useEffect(() => {
    if (userId) {
      dispatch(getGolfRounds(userId));
    }
  }, [userId, Object.keys(rounds).length, dispatch]);

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
        <Grid>
          <PastGolfRoundContainer
            rounds={rounds}
            stats={stats}
            dispatch={dispatch}
          />
        </Grid>
      </Container>

      <Route path={`${path}/enter-round`}>
        <EnterRound
          enterGolfRound={
            (userId, data) => dispatch(enterGolfRound(userId, data))
          }
          userId={userId}
          errorMessage={errorMessage}
        />
      </Route>
    </div>
  );
}
