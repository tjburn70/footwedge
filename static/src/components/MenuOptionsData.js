import React from 'react';
import HomeIcon from '@material-ui/icons/Home';
import PersonIcon from '@material-ui/icons/Person';
import DashboardIcon from '@material-ui/icons/Dashboard';
import CreateIcon from '@material-ui/icons/Create';
import GolfCourseIcon from '@material-ui/icons/GolfCourse';
import InfoIcon from '@material-ui/icons/Info';



export const MenuOptionsData = [
    {
        title: 'Home',
        path: '/',
        icon: <HomeIcon />,
        className: 'menu-item-text' 
    },
    {
        title: 'Player Profile',
        path: '/player-profile',
        icon: <PersonIcon />,
        className: 'menu-item-text' 
    },
    {
        title: 'Dashboard',
        path: '/dashboard',
        icon: <DashboardIcon />,
        className: 'menu-item-text' 
    },
    {
        title: 'Golf Rounds',
        path: '/golf-rounds',
        icon: <GolfCourseIcon />,
        className: 'menu-item-text' 
    },
    {
        title: 'Enter Round',
        path: '/enter-round',
        icon: <CreateIcon />,
        className: 'menu-item-text' 
    },
    {
        title: 'Info',
        path: '/info',
        icon: <InfoIcon />,
        className: 'menu-item-text' 
    },
];
