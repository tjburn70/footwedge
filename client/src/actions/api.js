import { CALL_API } from '../middleware/api';
import {
  ACCESS_TOKEN_REQUIRED,
  REFRESH_TOKEN_REQUIRED
} from '../middleware/auth';


export const LOGIN_REQUEST = 'LOGIN_REQUEST';
export const LOGIN_SUCCESS = 'LOGIN_SUCCESS';
export const LOGIN_FAILURE = 'LOGIN_FAILURE';

export const loginUser = ({ email, password }) => ({
  [CALL_API]: {
    endpoint: 'http://127.0.0.1:8000/api/user/login',
    httpMethod: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: {email: email, password: password},
    types: [
      LOGIN_REQUEST,
      LOGIN_SUCCESS,
      LOGIN_FAILURE
    ]
  }
})

export const REGISTER_USER_REQUEST = 'REGISTER_USER_REQUEST';
export const REGISTER_USER_SUCCESS = 'REGISTER_USER_SUCCESS';
export const REGISTER_USER_FAILURE = 'REGISTER_USER_FAILURE';

export const registerUser = (formData) => {
  const {
    email,
    password,
    firstName,
    lastName,
    phoneNumber,
    dateOfBirth,
    gender
  } = formData;

  let body = {
    email: email,
    password: password,
    first_name: firstName,
    last_name: lastName,
    phone_number: phoneNumber,
    date_of_birth: dateOfBirth,
    gender: gender,
  }

  return {
    [CALL_API]: {
      endpoint: 'http://127.0.0.1:8000/api/user/register',
      httpMethod: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: body,
      types: [
        REGISTER_USER_REQUEST,
        REGISTER_USER_SUCCESS,
        REGISTER_USER_FAILURE
      ]
    }
  }
}

export const ACCESS_TOKEN_REQUEST = 'ACCESS_TOKEN_REQUEST';
export const ACCESS_TOKEN_SUCCESS = 'ACCESS_TOKEN_SUCCESS';
export const ACCESS_TOKEN_FAILURE = 'ACCESS_TOKEN_FAILURE';

// this should hit the auth middleware
// and add the refreshToken from localStorage
export const getAccessToken = () => ({
  [REFRESH_TOKEN_REQUIRED]: {
    endpoint: 'http://127.0.0.1:8000/api/auth/refresh',
    httpMethod: 'POST',
    headers: {},
    types: [
      ACCESS_TOKEN_REQUEST,
      ACCESS_TOKEN_SUCCESS,
      ACCESS_TOKEN_FAILURE,
    ]
  }
})

export const LOGOUT_REQUEST = 'LOGOUT_REQUEST';
export const LOGOUT_SUCCESS = 'LOGOUT_SUCCESS';
export const LOGOUT_FAILURE = 'LOGOUT_FAILURE';

export const logoutUser = () => ({
  [REFRESH_TOKEN_REQUIRED]: {
    endpoint: 'http://127.0.0.1:8000/api/user/logout',
    httpMethod: 'DELETE',
    headers: {},
    types: [
      LOGOUT_REQUEST,
      LOGOUT_SUCCESS,
      LOGOUT_FAILURE,
    ]
  }
})
