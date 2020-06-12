import React from 'react';
import { Route, Redirect } from 'react-router-dom';


const PrivateRoute = (
  { component: Component, isAuthenticated, data, dispatch, ...rest}
) => (
  <Route {...rest} render={(props) => (
    isAuthenticated === true
    ? <Component data={data} dispatch={dispatch} {...props} />
    : <Redirect to='/login' />
  )} />
)

export default PrivateRoute;
