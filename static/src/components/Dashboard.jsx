import React, { useEffect } from 'react';
import { GolfRoundChart } from './GolfRoundChart';
import { getGolfRounds, getRoundStatsSummary } from '../actions/api';

export const Dashboard = (props) => {
  const {
    rounds,
    stats,
    statsSummary,
    hasAccessToken,
  } = props.data;
  const dispatch = props.dispatch;
  const numRounds = rounds.allIds.length;
  const numStats = stats.allIds.length;

  useEffect(() => {
    if (hasAccessToken) {
      dispatch(getGolfRounds());
    }
  }, [hasAccessToken, numRounds, dispatch]);

  useEffect(() => {
    if (hasAccessToken) {
      dispatch(getRoundStatsSummary());
    }
  }, [hasAccessToken, numStats, dispatch]);

  return (
    <div>
      <GolfRoundChart
        rounds={rounds}
        stats={stats}
        statsSummary={statsSummary}
      />
    </div>
  );
}
