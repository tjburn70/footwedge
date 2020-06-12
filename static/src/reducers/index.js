import { combineReducers } from 'redux';

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
  LOGOUT_REQUEST,
  LOGOUT_FAILURE,
  GET_HANDICAP_SUCCESS,
} from '../actions/api';


const errorMessage = (state = null, action) => {
  const { type, errorMessage } = action;
  if (errorMessage) {
    console.log(errorMessage);
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
};

const auth = (state = initialAuthState, action) => {
  switch (action.type) {
    case LOGIN_REQUEST:
      return Object.assign({}, state, {
        isFetching: true,
        isAuthenticated: false,
        accessToken: '',
      })
    case LOGIN_SUCCESS:
      return Object.assign({}, state, {
        isFetching: false,
        isAuthenticated: true,
        accessToken: action.payload.access_token,
      })
    case LOGIN_FAILURE:
      return Object.assign({}, state, {
        isFetching: false,
        isAuthenticated: false,
        accessToken: '',
      })
    case REGISTER_USER_REQUEST:
      return Object.assign({}, state, {
        isFetching: true,
        isAuthenticated: false,
        accessToken: '',
      })
    case REGISTER_USER_SUCCESS:
      return Object.assign({}, state, {
        isFetching: false,
        isAuthenticated: true,
        accessToken: action.payload.access_token,
      })
    case REGISTER_USER_FAILURE:
      return Object.assign({}, state, {
        isFetching: false,
        isAuthenticated: false,
        accessToken: '',
      })
    case ACCESS_TOKEN_REQUEST:
      return Object.assign({}, state, {
        isFetching: true,
        accessToken: '',
      })
    case ACCESS_TOKEN_SUCCESS:
      return Object.assign({}, state, {
        isFetching: false,
        isAuthenticated: true,
        accessToken: action.payload.access_token,
      })
    case ACCESS_TOKEN_FAILURE:
      return Object.assign({}, state, {
        isFetching: false,
        isAuthenticated: false,
        accessToken: '',
      })
    case LOGOUT_SUCCESS:
      return Object.assign({}, state, {
        isFetching: true,
        isAuthenticated: false,
        accessToken: '',
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
        index: action.payload.index,
        authorizedAssociation: action.payload.authorized_association,
        lastCalculated: action.payload.record_start_date,
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
});

export default rootReducer;
