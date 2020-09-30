import { combineReducers } from 'redux';
import { rounds } from './playerRounds';
import { stats } from './roundStats';
import { statsSummary } from './roundStatsSummary';

import {
  LOGIN_REQUEST,
  LOGIN_SUCCESS,
  LOGIN_FAILURE,
  REGISTER_USER_REQUEST,
  REGISTER_USER_SUCCESS,
  REGISTER_USER_FAILURE,
  ACCESS_TOKEN_REQUEST,
  ACCESS_TOKEN_SUCCESS,
  ACCESS_TOKEN_FAILURE,
  LOGOUT_SUCCESS,
  GET_HANDICAP_SUCCESS,
} from '../actions/api';


const errorMessage = (state = null, action) => {
  const { errorMessage } = action;
  if (errorMessage) {
    return errorMessage;
  }

  return state;
}

const currentUser = (state = null, action) => {
  switch (action.type) {
    case LOGIN_SUCCESS:
      return Object.assign({}, state, {
        currentUser: action.payload.user_id
      })
    case REGISTER_USER_SUCCESS:
      return Object.assign({}, state, {
        currentUser: action.payload.user_id
      })
    case ACCESS_TOKEN_SUCCESS:
      return action.payload.user_id
    case LOGOUT_SUCCESS:
      return null
    default:
      return state
  }
}

const initialAuthState = {
  isFetching: false,
  isAuthenticated: localStorage.getItem('refresh_token') ? true : false,
  accessToken: '',
  hasAccessToken: false,
};

const auth = (state = initialAuthState, action) => {
  switch (action.type) {
    case LOGIN_REQUEST:
      return Object.assign({}, state, {
        isFetching: true,
        isAuthenticated: false,
        accessToken: '',
        hasAccessToken: false,
      })
    case LOGIN_SUCCESS:
      return Object.assign({}, state, {
        isFetching: false,
        isAuthenticated: true,
        accessToken: action.payload.access_token,
        hasAccessToken: true,
      })
    case LOGIN_FAILURE:
      return Object.assign({}, state, {
        isFetching: false,
        isAuthenticated: false,
        accessToken: '',
        hasAccessToken: false,
      })
    case REGISTER_USER_REQUEST:
      return Object.assign({}, state, {
        isFetching: true,
        isAuthenticated: false,
        accessToken: '',
        hasAccessToken: false,
      })
    case REGISTER_USER_SUCCESS:
      return Object.assign({}, state, {
        isFetching: false,
        isAuthenticated: true,
        accessToken: action.payload.access_token,
        hasAccessToken: true,
      })
    case REGISTER_USER_FAILURE:
      return Object.assign({}, state, {
        isFetching: false,
        isAuthenticated: false,
        accessToken: '',
        hasAccessToken: false,
      })
    case ACCESS_TOKEN_REQUEST:
      return Object.assign({}, state, {
        isFetching: true,
        accessToken: '',
        hasAccessToken: false,
      })
    case ACCESS_TOKEN_SUCCESS:
      return Object.assign({}, state, {
        isFetching: false,
        isAuthenticated: true,
        accessToken: action.payload.access_token,
        hasAccessToken: true,
      })
    case ACCESS_TOKEN_FAILURE:
      return Object.assign({}, state, {
        isFetching: false,
        isAuthenticated: false,
        accessToken: '',
        hasAccessToken: false,
      })
    case LOGOUT_SUCCESS:
      return Object.assign({}, state, {
        isFetching: true,
        isAuthenticated: false,
        accessToken: '',
        hasAccessToken: false,
      })
    default:
      return state
  }
}

const initialHandicapState = {
  index: '',
  authorizedAssociation: '',
  lastCalculated: '',
};

const handicap = (state = initialHandicapState, action) => {
  switch (action.type) {
    case GET_HANDICAP_SUCCESS:
      return Object.assign({}, state, {
        index: action.payload.result.index,
        authorizedAssociation: action.payload.result.authorized_association,
        lastCalculated: action.payload.result.record_start_date,
      })
    default:
      return state
  }
}

const rootReducer = combineReducers({
  errorMessage,
  currentUser,
  auth,
  handicap,
  rounds,
  stats,
  statsSummary,
});

export default rootReducer;
