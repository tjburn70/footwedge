import axios from 'axios';
import qs from "query-string";
import { getAccessToken, logoutUser } from '../actions/api';
import { REFRESH_TOKEN_REQUIRED, ACCESS_TOKEN_REQUIRED } from './auth';


export const CALL_API = "CALL_API";

const hasAuthHeaders = (apiAction) => {
  return (typeof apiAction.headers['Authorization'] !== 'undefined');
}

const isRefreshAction = (apiAction, refreshAction) => {
  return apiAction.endpoint === refreshAction[REFRESH_TOKEN_REQUIRED].endpoint;
}

export const apiMiddleware = store => next => action => {
  const apiAction = action[CALL_API];
  if (typeof apiAction === "undefined") {
    return next(action);
  }

  let { endpoint, httpMethod, body, query, headers } = apiAction;
  const { types } = apiAction;

  if (body) {
    body = JSON.stringify(body);
  }

  let queryString = '';
  if (query) {
    queryString += "?" + qs.stringify(query);
  }

  let url = queryString ? endpoint + queryString : endpoint;

  const config = {
    method: httpMethod,
    url: url,
    headers: headers,
    data: body,
  };

  const actionWith = data => {
    const finalAction = Object.assign({}, action, data);
    delete finalAction[CALL_API];
    return finalAction;
  };

  const [requestType, successType, failureType] = types;
  next(actionWith({ type: requestType }));

  return axios.request(config)
    .then(res => {
      const payload = res.data;
      // want to normalize the response
      next(actionWith({
        type: successType,
        payload: payload,
      }));
    })
    .catch(error => {
      let errorMessage = null
      if (error.response) {
        errorMessage = error.response.data.message;
        const statusCode = error.response.status;
        if (statusCode === 401 &&
            hasAuthHeaders(apiAction) &&
            !isRefreshAction(apiAction, getAccessToken())) {
          return store.dispatch(getAccessToken())
            .then(() => {
              const actionToRetry = {};
              // need to set this key so that auth middleware picks it up
              actionToRetry[ACCESS_TOKEN_REQUIRED] = apiAction;
              return store.dispatch(actionToRetry);
            })
        } else if (statusCode === 401 &&
                   hasAuthHeaders(apiAction) &&
                   isRefreshAction(apiAction, getAccessToken())) {
          console.log('invalid refresh token!');
          return store.dispatch(logoutUser());
        }
      } else if (error.request) {
        errorMessage = 'Uh Oh... Network Issue';
      }
      next(actionWith({
        type: failureType,
        errorMessage: errorMessage,
      }));
    })

}
