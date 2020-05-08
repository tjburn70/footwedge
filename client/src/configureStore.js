import { createStore, applyMiddleware } from 'redux';
import { apiMiddleware } from './middleware/api';
import { applyAuthHeader, setRefreshToken, unsetRefreshToken } from './middleware/auth';
import rootReducer from './reducers';

export const configureStore = () => {
  const store = createStore(
    rootReducer,
    applyMiddleware(
      applyAuthHeader,
      apiMiddleware,
      setRefreshToken,
      unsetRefreshToken,
    )
  );

  return store;
};
