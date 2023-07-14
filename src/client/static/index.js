import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App'
import axios from 'axios'

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <App />
);

function getOdds() {
    axios.get(`/odds`)
    .then(response => {
        // Handle the successful response
        console.log(response.data);
    })
    .catch(error => {
        // Handle any errors that occur during the request
        console.error(error);
    });
}

getOdds()
