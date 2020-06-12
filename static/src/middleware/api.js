import axios from 'axios';
import qs from "query-string";
import { normalize, schema } from 'normalizr';


export const CALL_API = "CALL_API";

export const apiMiddleware = store => next => action => {
  const apiAction = action[CALL_API];
  if (typeof apiAction === "undefined") {
    return next(action);
  }

  let { endpoint, httpMethod, body, query, headers } = apiAction;
  const { types, schema } = apiAction;

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
      console.log(res.statusCode);
      console.log(res.data);
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
        let statusCode = error.response.statusCode;
        console.log(statusCode);
        if (statusCode === 401) {
          console.log('Uh Oh... received a 401');
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
