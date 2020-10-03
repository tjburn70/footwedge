import React from 'react';
import { Link } from 'react-router-dom';
import { List, ListItem, ListItemIcon, ListItemText } from '@material-ui/core';
import PersonIcon from '@material-ui/icons/Person';
import DashboardIcon from '@material-ui/icons/Dashboard';
import CreateIcon from '@material-ui/icons/Create';
import GolfCourseIcon from '@material-ui/icons/GolfCourse';
import InfoIcon from '@material-ui/icons/Info';

export const MenuOptions = () => {
  return (
    <div>
      <ListItem
        button
        key="player-profile"
        component={Link} to="/player-profile">
        <ListItemIcon>
            <PersonIcon />
        </ListItemIcon>
        <ListItemText primary="Player Profile" />
      </ListItem>
      <ListItem
        button
        key="dashboard"
        component={Link} to="/dashboard">
        <ListItemIcon>
            <DashboardIcon />
        </ListItemIcon>
        <ListItemText primary="Dashboard" />
      </ListItem>
      <ListItem
        button
        key="golf-rounds"
        component={Link} to="/golf-rounds">
        <ListItemIcon>
            <GolfCourseIcon />
        </ListItemIcon>
        <ListItemText primary="Golf Rounds" />
      </ListItem>
      <ListItem
        button
        key="enter-round"
        component={Link} to="/enter-round">
        <ListItemIcon>
            <CreateIcon />
        </ListItemIcon>
        <ListItemText primary="Enter Round" />
      </ListItem>
      <ListItem
        button
        key="info"
        component={Link} to="/info">
        <ListItemIcon>
            <InfoIcon />
        </ListItemIcon>
        <ListItemText primary="Info" />
      </ListItem>
    </div>
  );
}
