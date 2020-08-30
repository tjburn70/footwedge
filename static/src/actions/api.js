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

export const ENTER_ROUND_REQUEST = 'ENTER_ROUND_REQUEST';
export const ENTER_ROUND_SUCCESS = 'ENTER_ROUND_SUCCESS';
export const ENTER_ROUND_FAILURE = 'ENTER_ROUND_FAILURE';

export const enterGolfRound = (userId, data) => {
  const endPoint = 'http://127.0.0.1:8000/api/user/'+userId+'/golf-rounds';
  const {
    golfCourseId,
    teeBoxId,
    totalScore,
    towardsHandicap,
    playedOn
  } = data;

  const body = {
    golf_course_id: golfCourseId,
    tee_box_id: teeBoxId,
    gross_score: totalScore,
    towards_handicap: towardsHandicap,
    played_on: playedOn,
  };

  return {
    [ACCESS_TOKEN_REQUIRED]: {
      endpoint: endPoint,
      httpMethod: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: body,
      types: [
        ENTER_ROUND_REQUEST,
        ENTER_ROUND_SUCCESS,
        ENTER_ROUND_FAILURE,
      ]
    }
  }
}

export const GET_HANDICAP_REQUEST = 'FETCH_HANDICAP_REQUEST';
export const GET_HANDICAP_SUCCESS = 'FETCH_HANDICAP_SUCCESS';
export const GET_HANDICAP_FAILURE = 'FETCH_HANDICAP_FAILURE';

export const getHandicap = () => {
  const endPoint = 'http://127.0.0.1:8000/api/handicaps/';
  return {
    [ACCESS_TOKEN_REQUIRED]: {
      endpoint: endPoint,
      httpMethod: 'GET',
      headers: {},
      types: [
        GET_HANDICAP_REQUEST,
        GET_HANDICAP_SUCCESS,
        GET_HANDICAP_FAILURE,
      ]
    }
  }
}

export const GET_GOLF_ROUNDS_REQUEST = 'GET_GOLF_ROUNDS_REQUEST';
export const GET_GOLF_ROUNDS_SUCCESS = 'GET_GOLF_ROUNDS_SUCCESS';
export const GET_GOLF_ROUNDS_FAILURE = 'GET_GOLF_ROUNDS_FAILURE';

export const getGolfRounds = (userId) => {
  const endPoint = `http://127.0.0.1:8000/api/user/${userId}/golf-rounds`;
  return {
    [ACCESS_TOKEN_REQUIRED]: {
      endpoint: endPoint,
      httpMethod: 'GET',
      headers: {},
      types: [
        GET_GOLF_ROUNDS_REQUEST,
        GET_GOLF_ROUNDS_SUCCESS,
        GET_GOLF_ROUNDS_FAILURE,
      ]
    }
  }
}

export const ADD_ROUND_STAT_REQUEST = 'ADD_ROUND_STAT_REQUEST';
export const ADD_ROUND_STAT_SUCCESS = 'ADD_ROUND_STAT_SUCCESS';
export const ADD_ROUND_STAT_FAILURE = 'ADD_ROUND_STAT_FAILURE';

export const addRoundStat = (userId, roundId, holeId, data) => {
  const endPoint = `http://127.0.0.1:8000/api/user/${userId}/golf-rounds/${roundId}/golf-round-stats`;
  const {
    score,
    fairwayHit,
    greenInRegulation,
    totalPutts,
    totalChips,
    greenSideSandShots,
    totalPenalties,
  } = data;

  const body = {
    round_stats: [
      {
        golf_round_id: roundId,
        hole_id: holeId,
        gross_score: score,
        fairway_hit: fairwayHit,
        green_in_regulation: greenInRegulation,
        putts: totalPutts,
        chips: totalChips,
        greenside_sand_shots: greenSideSandShots,
        penalties: totalPenalties,
      }
    ]
  };

  return {
    [ACCESS_TOKEN_REQUIRED]: {
      endpoint: endPoint,
      httpMethod: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: body,
      types: [
        ADD_ROUND_STAT_REQUEST,
        ADD_ROUND_STAT_SUCCESS,
        ADD_ROUND_STAT_FAILURE,
      ]
    }
  }
}
