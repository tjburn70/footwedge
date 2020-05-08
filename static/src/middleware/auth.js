import { CALL_API } from './api';
import {
  LOGIN_SUCCESS,
  REGISTER_USER_SUCCESS,
  LOGOUT_SUCCESS,
  LOGOUT_FAILURE,
} from '../actions/api';


export const ACCESS_TOKEN_REQUIRED = '@@authorized_by_access_token';
export const REFRESH_TOKEN_REQUIRED = '@@authorized_by_refresh_token';

export const applyAuthHeader = (store) => (next) => (action) => {
  if (action[ACCESS_TOKEN_REQUIRED] || action[REFRESH_TOKEN_REQUIRED]) {
    const authKey = Object.keys(action)[0];
    let token = null;
    if (authKey === ACCESS_TOKEN_REQUIRED) {
      token = store.getState().auth.accessToken;
    } else if (authKey === REFRESH_TOKEN_REQUIRED) {
      token = localStorage.getItem('refresh_token');
    }

    const currentApiAction = {...action[authKey]};
    const currentHeaders = currentApiAction.headers
      ? {...currentApiAction.headers}
      : {}

    currentHeaders['Authorization'] = 'Bearer ' + token;
    currentApiAction.headers = currentHeaders;

    const newApiAction = {};
    newApiAction[CALL_API] = currentApiAction;

    return next(newApiAction);
  }

  return next(action);
}

export const setRefreshToken = store => next => action => {
  const validActions = [LOGIN_SUCCESS, REGISTER_USER_SUCCESS];
  if (validActions.indexOf(action.type) !== -1) {
    let refreshToken = action.payload.refresh_token;
    localStorage.setItem('refresh_token', refreshToken);
  }

  return next(action);
}

export const unsetRefreshToken = store => next => action => {
  const validActions = [LOGOUT_SUCCESS, LOGOUT_FAILURE];
  if (validActions.indexOf(action.type) !== -1) {
    localStorage.removeItem('refresh_token');
    let token = localStorage.getItem('refresh_token');
  }

  return next(action);
}
