import React from 'react';

// Table head component
function TableHead() {
  return (
    <thead>
      <tr>
        <th>Profit</th>
        <th>League/Sport</th>
        <th>Game</th>
        <th>Outcome 1</th>
        <th>Outcome 2</th>
        <th>Outcome 3</th>
        <th>Region</th>
      </tr>
    </thead>
  );
}

// Table rows component
function TableRows({ data }) {
    console.log(data)
    return (
      <tbody>
        {data.map((item, index) => (
          <tr key={index}>
            <td>{item.profit}%</td>
            <td>{item.sport}</td>
            <td>{item.game}</td>
            <td>${item.o1}</td>
            <td>${item.o2}</td>
            <td>{item.o3 !== null ? `$${item.o3}` : 'N/A'}</td>
            <td>{item.region}</td>
          </tr>
        ))}
      </tbody>
    );
  }

// Main Table component
function Table({ tableData }) {
  return (
    <div className="container">
      <h1>CRUD App</h1>
      <table className="table-striped">
        <TableHead />
        <TableRows data={tableData} />
      </table>
    </div>
  );
}

export default Table;