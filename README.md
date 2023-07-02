# Arbitrage Betting Project

This project is focused on arbitrage betting. Leveraging the Odds API, we analyse and compare odds across bookmakers to identify potential arbibtrage opportunities. The end goal is to display these opporunities and allow bettors to calculate their yields in a React App.

## Installation

NOTE: this is an installation guide for the arb calculator code, not the entire web app

1. Clone the repository:
    <br>
    ```bash
    git clone https://github.com/{YOUR_USERNAME}/arbitrage-betting.git
    ```

2. Initialise your virtual environment
    <br>
    ```bash
    python3 -v venv venv
    source ./venv/bin/activate
    ```

3. Install the project dependencies
    <br>
    ```bash
    pip install -r requirements.txt
    ```

4. Set up your API key
  - Obtain an API key from Odds API (https://www.oddsapi.io/)
  - Create a .env file and put the following line at the top:
    <br>
    ```dotenv
    ODDS_API_KEY={YOUR_API_KEY}
    ```

5. Run: 
    <br>
    ```bash
    python3 src/arb_finder.py
    ```
    And watch the magic


  

