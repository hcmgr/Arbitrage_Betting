import React from 'react';
import ReactDOM from 'react-dom';

// Define a simple React component
function App() {
  return (
    React.createElement('div', null,
      React.createElement('h1', null, 'Hello, React!'),
      React.createElement('p', null, 'This is a minimal React app.')
    )
  );
}

// Render the component into the root element
ReactDOM.render(
  React.createElement(App, null),
  document.getElementById('root')
);
