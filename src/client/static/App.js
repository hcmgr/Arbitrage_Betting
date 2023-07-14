import React from 'react';
import Table from './table'

// Define a simple React component
function App({ data }) {
    return (
        <div className="App">
            <p>Ze music TM</p>
            <Table tableData={data} />
        </div>
    );
}

export default App

