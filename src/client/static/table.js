import React from 'react';

function Table() {
  const tableData = [
    { id: 1, name: 'John', age: 25, email: 'john@example.com' },
    { id: 2, name: 'Alice', age: 32, email: 'alice@example.com' },
  ];

  return (
    <div className="container">
      <h1>CRUD App</h1>
      <table className="table table-striped">
        <thead>
          <tr>
            <th>Profit</th>
            <th>League/Sport</th>
            <th>Game</th>
            <th>Outcome 1</th>
            <th>Outcome 2</th>
            <th>Outcome 3 (optional)</th>
            <th>Region</th>
          </tr>
        </thead>
        <tbody>
          {tableData.map((item) => (
            <tr key={item.id}>
              <td>{item.id}</td>
              <td>{item.name}</td>
              <td>{item.age}</td>
              <td>{item.email}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Table;
