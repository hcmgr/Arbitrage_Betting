import React from 'react';
import ReactDOM from 'react-dom';
import App from './App'

// Render the component into the root element
ReactDOM.render(
  React.createElement(App, null),
  document.getElementById('root')
);
