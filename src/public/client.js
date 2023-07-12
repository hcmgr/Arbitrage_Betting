import React from 'react';
import ReactDOM from 'react-dom';

class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            items: [],
            newItem: ''
        };
    }

    componentDidMount() {
        // Fetch initial data from the server or perform any necessary setup
        // For example, you can make an API request to retrieve existing items
        // and update the state with the response data
    }

    handleInputChange = (event) => {
        this.setState({ newItem: event.target.value });
    };

    handleSubmit = (event) => {
        event.preventDefault();

        // Perform actions to create a new item
        // For example, you can make an API request to create the item on the server
        // and update the state with the new item

        // Reset the newItem state value
        this.setState({ newItem: '' });
    };

    render() {
        return (
            <div>
                <h1>CRUD App</h1>
                <form onSubmit={this.handleSubmit}>
                    <input
                        type="text"
                        value={this.state.newItem}
                        onChange={this.handleInputChange}
                    />
                    <button type="submit">Add Item</button>
                </form>
                <ul>
                    {this.state.items.map((item, index) => (
                        <li key={index}>{item}</li>
                    ))}
                </ul>
            </div>
        );
    }
}

ReactDOM.render(<App />, document.getElementById('root'));
