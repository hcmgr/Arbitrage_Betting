# Arbitrage Betting Project

### Background

[Arbitrage](https://en.wikipedia.org/wiki/Arbitrage_betting) opportunities allow one to make a guaranteed profit by betting both sides of a sports event. Because bookmakers aren't stupid, they always ensure no such opporunities arise from their own odds. However, they do not ensure this ACROSS bookmakers. For example, betting for and against Nadal at the same bookmaker always loses you money. However, betting for Nadal at SportsBet and against him at Pointsbet (ie: cross-betting), is occasionally profitable. By scowering these 'cross-bets', we can easily find arbitrage opportunities.

### Approach
We've built a React app to display all current arbitrate opporunities across 40 different sports in 5 global markets. 

### Stack
Front-end: React, Boostrap

Back-end: Flask web server, MongoDB database, hosted on personal Ubuntu droplet

## Installation

1. Clone the repository (ensuring to replace YOUR_USERNAME in the link)
    <br>
    ```bash
    https://github.com/{YOUR_USERNAME}/Arbitrage_Betting.git
    ```

2. Initialise your virtual environment
    <br>
    ```bash
    cd Arbitrage_Betting
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

5. If you simply want to run and test the arb. calculation code, run:
    ```bash
    chmod 777 scripts/arb_find.sh 
    ./scripts/arb_find.sh
    ```
    And watch the magic

    <br>

    NOTE: may have to go into src/server/arb_finder.py and uncomment out
          arb_caller() in the main function

### Instructions for running the website [For contributors and general interest]
If you want to actually host the full React app:

5. Ensure you have node.js installed
6. Run:
    ```bash
    npm init -y
    npm install
    ```
to install the necessary node modules

7. Ensure config/webpack.config.js has:
    ```bash
    bind = "127.0.0.1:5000"
    ```

7. Run:
    ```bash
    chmod run.sh 777
    ./scripts/run.sh
    ```
this will start a Flask web server on localhost 5000 

NOTE: to host remotely, simply change bind to appropriate IP address and port config

### Other helpful things ###
Sync local repo to remote repo using rsync:

```bash
rsync -avz --exclude=/venv --exclude=/node_modules  {path_to_local_repo} {user}@{remote_IP}:{path_to_remote_repo}
```
