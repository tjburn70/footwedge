import React from 'react';
import { Link } from 'react-router-dom';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import Typography from '@material-ui/core/Typography';
import InputBase from '@material-ui/core/InputBase';
import { fade, makeStyles } from '@material-ui/core/styles';
import MenuIcon from '@material-ui/icons/Menu';
import SearchIcon from '@material-ui/icons/Search';
import GolfCourseIcon from '@material-ui/icons/GolfCourse';
import { logoutUser } from '../actions/api';
import { Logout } from './Logout';

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  menuButton: {
    marginRight: theme.spacing(2),
  },
  title: {
    display: 'none',
    [theme.breakpoints.up('sm')]: {
      display: 'block',
    },
  },
  search: {
    position: 'relative',
    borderRadius: theme.shape.borderRadius,
    backgroundColor: fade(theme.palette.common.white, 0.15),
    '&:hover': {
      backgroundColor: fade(theme.palette.common.white, 0.25),
    },
    width: '100%',
    [theme.breakpoints.up('sm')]: {
      marginLeft: theme.spacing(2),
      width: 'auto',
    },
  },
  searchIcon: {
    padding: theme.spacing(0, 2),
    height: '100%',
    position: 'absolute',
    pointerEvents: 'none',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  inputRoot: {
    color: 'inherit',
  },
  inputInput: {
    padding: theme.spacing(1, 1, 1, 0),
    // vertical padding + font size from searchIcon
    paddingLeft: `calc(1em + ${theme.spacing(4)}px)`,
    transition: theme.transitions.create('width'),
    width: '100%',
    [theme.breakpoints.up('sm')]: {
      width: '12ch',
      '&:focus': {
        width: '20ch',
      },
    },
  },
  loginButton: {
    marginLeft: '60%',
    color: 'inherit',
  },
  registerButton: {
    float: 'right',
    marginLeft: '6px',
    
  },
}));

export const NavBar = ({ isAuthenticated, dispatch }) => {
  const classes = useStyles();
  const renderButton = () => {
    if (isAuthenticated) {
      return (
        <Logout logoutUser={() => dispatch(logoutUser())}/>
      );
    } else {
      return (
        <>
          <Button 
            className={classes.loginButton} 
            component={Link} 
            to="/login"
          >
              Login
          </Button>
          <Button 
            className={classes.registerButton} 
            color="secondary"
            component={Link} 
            to="/register"
          >
            Register
          </Button>
        </>
      );
    }
  }

  return (
    <div className={classes.root}>
      <AppBar position="static">
        <Toolbar>
          <IconButton
            edge="start"
            className={classes.menuButton}
            color="inherit"
            aria-label="open drawer"
          >
            <MenuIcon />
          </IconButton>
          <Typography className={classes.title} variant="h6" noWrap>
            FootWedge
          </Typography>
          <GolfCourseIcon/>
          <div className={classes.search}>
            <div className={classes.searchIcon}>
              <SearchIcon />
            </div>
            <InputBase
              placeholder="Search Courses…"
              classes={{
                root: classes.inputRoot,
                input: classes.inputInput,
              }}
              inputProps={{ 'aria-label': 'search' }}
            />
          </div>
          {renderButton()}
        </Toolbar>
      </AppBar>
    </div>
  );
}
