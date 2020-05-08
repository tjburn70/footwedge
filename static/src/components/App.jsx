import React from 'react';
import { connect } from 'react-redux';
import { Route, Switch, Link } from 'react-router-dom';
import { getAccessToken, loginUser, registerUser } from '../actions/api';
import PrivateRoute from './PrivateRoute';
import { NavBar } from './NavBar';
import { Login } from './Login';
import { RegisterUser } from './RegisterUser';
import PlayerProfile from './PlayerProfile';


class App extends React.Component {

  constructor(props) {
    super(props);
  }

  componentDidMount() {
    let token = localStorage.getItem('refresh_token');
    if (token) {
      this.props.dispatch(getAccessToken());
    }
  }

  render() {
    const { dispatch, auth, currentUser, errorMessage } = this.props;

    return (
      <div>
        <div>
          <NavBar isAuthenticated={auth.isAuthenticated} dispatch={dispatch}/>
          <Switch>
            <Route path="/login">
              <Login
                loginUser={(data) => dispatch(loginUser(data))}
                isAuthenticated={auth.isAuthenticated}
                errorMessage={errorMessage}
              />
            </Route>
            <Route path='/register'>
              <RegisterUser
                registerUser={(data) => dispatch(registerUser(data))}
                errorMessage={errorMessage}
              />
            </Route>
            <PrivateRoute
              path='/player-profile'
              component={PlayerProfile}
              isAuthenticated={auth.isAuthenticated}
              currentUser={currentUser}>
            </PrivateRoute>
          </Switch>
        </div>
      </div>
    );
  }

}

const mapStateToProps = (state) => {
  return {
    auth: {
      isAuthenticated: state.auth.isAuthenticated,
      isFetching: state.auth.isFetching,
      accessToken: state.auth.accessToken,
    },
    errorMessage: state.errorMessage,
    currentUser: state.currentUser,
  }
};

export default connect(mapStateToProps)(App);
