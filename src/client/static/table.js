import React from 'react';

// Table head component
// TODO: table creates maximum needed outcome columns
// (Don't just hard code for 3 outcomes)
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

function OutcomeCell(outcome) {
    if (!outcome) {
        return (
            <td>-</td>
        )
    } 
    return (
        <td>
            <div>${outcome.price}</div>
            <div>{outcome.book}</div>
            <div>{outcome.team}</div>
        </td>
    )
}

// Table rows component
function TableRows({ data }) {
    return (
      <tbody>
        {data.map((item, index) => (
          <tr key={index}>
            <td>{item.profit}%</td>
            <td>{item.sport}</td>
            <td>{item.game}</td>
            {item.outcomes.map((outcome, _) => (
            <td>{OutcomeCell(outcome)}</td>
            ))}
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