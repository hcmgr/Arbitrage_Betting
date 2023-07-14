import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css'; // all sub-components of App can use this

const root = ReactDOM.createRoot(document.getElementById('root'));

async function getOdds() {
  try {
    const response = await axios.get('/odds');
    return response.data;
  } catch (error) {
    console.error(error);
  }
}

getOdds()
  .then(data => {
    root.render(<App data={data} />);
  });
