import { combineReducers } from 'redux';
import { GET_ROUND_STATS_SUMMARY_SUCCESS } from '../actions/api';


const statsSummaryByRoundId = (state = {}, action) => {
  switch (action.type) {
    case GET_ROUND_STATS_SUMMARY_SUCCESS:
      return Object.assign({}, state, action.payload.result);
    default:
      return state
  }
}

export const statsSummary = combineReducers({
  byId: statsSummaryByRoundId,
});
