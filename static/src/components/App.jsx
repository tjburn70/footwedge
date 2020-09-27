import React from 'react';
import { connect } from 'react-redux';
import { Route, Switch } from 'react-router-dom';
import { getAccessToken, loginUser, registerUser } from '../actions/api';
import PrivateRoute from './PrivateRoute';
import { NavBar } from './NavBar';
import { Login } from './Login';
import { RegisterUser } from './RegisterUser';
import { PlayerProfile } from './PlayerProfile';
import { Dashboard } from './Dashboard';
import { GolfRounds } from './GolfRounds';
import { EnterRound } from './EnterRound';
import { InfoPage } from './InfoPage';
import { MenuOptions } from './MenuOptions';


class App extends React.Component {

  componentDidMount() {
    let token = localStorage.getItem('refresh_token');
    if (token) {
      this.props.dispatch(getAccessToken());
    }
  }

  render() {
    const {
      dispatch,
      auth,
      currentUser,
      handicap,
      rounds,
      stats,
      errorMessage
    } = this.props;

    return (
      <div>
        <div>
          <NavBar isAuthenticated={auth.isAuthenticated} dispatch={dispatch}/>
          <MenuOptions />
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
            <Route path='/info'>
              <InfoPage />
            </Route>
            <PrivateRoute
              path='/player-profile'
              component={PlayerProfile}
              isAuthenticated={auth.isAuthenticated}
              dispatch={dispatch}
              data={{
                accessToken: auth.accessToken,
                handicap: handicap,
              }}>
            </PrivateRoute>
            <PrivateRoute
              path='/dashboard'
              component={Dashboard}
              isAuthenticated={auth.isAuthenticated}
              dispatch={dispatch}
              data={{
                userId: currentUser,
                accessToken: auth.accessToken,
                errorMessage: errorMessage,
                handicap: handicap,
                rounds: rounds,
                stats: stats,
              }}>
            </PrivateRoute>
            <PrivateRoute
              path='/golf-rounds'
              component={GolfRounds}
              isAuthenticated={auth.isAuthenticated}
              dispatch={dispatch}
              data={{
                rounds: rounds,
                stats: stats,
                userId: currentUser,
              }}>
            </PrivateRoute>
            <PrivateRoute
              path='/enter-round'
              component={EnterRound}
              isAuthenticated={auth.isAuthenticated}
              dispatch={dispatch}
              data={{
                userId: currentUser,
                errorMessage: errorMessage,
              }}>
            </PrivateRoute>
          </Switch>
        </div>
      </div>
    );
  }

}

const mapStateToProps = (state) => {
  return {
    auth: state.auth,
    errorMessage: state.errorMessage,
    currentUser: state.currentUser,
    handicap: state.handicap,
    rounds: state.rounds,
    stats: state.stats,
  }
};

export default connect(mapStateToProps)(App);
