import React from 'react';
import axios from 'axios';

import { ALL_SQUARE_API_ROOT } from '../constants';


const initialState = {
    isLoggedIn: false,
}

class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = initialState;

    }

    checkApiHealth = (url) => {
        axios.get(url)
        .then(res => {
           const results = res.data.results;
           console.log(results);
        })
        .catch(error => {
            console.log(error);
        });
    }

    componentDidMount() {
        let healthPath = "/health"
        let url = new URL(healthPath, ALL_SQUARE_API_ROOT);

        this.checkApiHealth(url);
    }

    render() {
        const isLoggedIn = this.state.isLoggedIn;
        console.log(isLoggedIn);
        return (
            <div>
                "Welcome to AllSquare your go-to Golf app for score-keeping, goal-setting, and course exploration"
            </div>
        )
    }
}

export default App;
