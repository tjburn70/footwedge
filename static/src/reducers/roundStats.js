import { combineReducers } from 'redux';
import { normalize } from 'normalizr';
import { round, stat } from '../actions/schema';

import {
  ADD_ROUND_STAT_SUCCESS,
  GET_GOLF_ROUNDS_SUCCESS,
} from '../actions/api';


const addStatEntry = (state, action) => {
  const stat = action.payload.result[0];

  return {
    ...state,
    [stat.id]: stat
  }
}

const statsById = (state = {}, action) => {
  switch (action.type) {
    case ADD_ROUND_STAT_SUCCESS:
      return addStatEntry(state, action)
    case GET_GOLF_ROUNDS_SUCCESS:
      const normalizedData = normalize(action.payload.result, [round]);
      return Object.assign({}, state, normalizedData.entities.stats);
    default:
      return state
  }
}

const addStatId = (state, action) => {
  const stat = action.payload.result[0];
  return state.concat(stat.id)
}

const allStats = (state = [], action) => {
  switch (action.type) {
    case ADD_ROUND_STAT_SUCCESS:
      return addStatId(state, action)
    case GET_GOLF_ROUNDS_SUCCESS:
      const normalizedData = normalize(action.payload.result, [round]);
      const stats = normalizedData.entities.stats;
      const statIds = Object.keys(stats);
      return statIds
    default:
      return state
  }
}

export const stats = combineReducers({
  byId: statsById,
  allIds: allStats
});
