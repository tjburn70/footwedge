import { combineReducers } from 'redux';
import { normalize } from 'normalizr';
import { round } from '../actions/schema';

import {
  GET_GOLF_ROUNDS_SUCCESS,
  ADD_ROUND_STAT_SUCCESS,
  ENTER_ROUND_SUCCESS,
} from '../actions/api';

const addRoundEntry = (state, action) => {
  const round = action.payload.result;

  return {
    ...state,
    [round.id]: round
  }
}

const addStat = (state, action) => {
  const stat = action.payload.result[0];
  const statId = stat.id;
  const roundId = stat.golf_round_id;
  const round = state[roundId];

  return {
    ...state,
    [roundId]: {
      ...round,
      stats: round.stats.concat(statId)
    }
  }
}

const roundsById = (state = {}, action) => {
  switch (action.type) {
    case GET_GOLF_ROUNDS_SUCCESS:
      const normalizedData = normalize(action.payload.result, [round]);
      return Object.assign({}, state, normalizedData.entities.rounds)
    case ENTER_ROUND_SUCCESS:
      return addRoundEntry(state, action)
    case ADD_ROUND_STAT_SUCCESS:
      return addStat(state, action)
    default:
      return state
  }
}

const addRoundId = (state, action) => {
  const round = action.payload.result;
  return state.concat(round.id)
}

const allRounds = (state = [], action) => {
  switch (action.type) {
    case GET_GOLF_ROUNDS_SUCCESS:
      const normalizedData = normalize(action.payload.result, [round]);
      return normalizedData.result
    case ENTER_ROUND_SUCCESS:
      return addRoundId(state, action)
    default:
      return state
  }
}

export const rounds = combineReducers({
  byId: roundsById,
  allIds: allRounds
});
