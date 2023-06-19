import os
import requests
import json
from dotenv import load_dotenv
import textwrap

# Load the environment variables from the .env file
load_dotenv('.env')

# Read the API key from the environment variables
api_key = os.getenv('ODDS_API_KEY')

HOST = "https://api.the-odds-api.com"

def general_get_req(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Request failed with code: ", response.status_code)
        return None

def sports_url():
    return HOST + f"/v4/sports/?apiKey={api_key}"

def odds_url(odds_dic: dict[str: str]):
    return (HOST +
        f'''/v4/sports/{odds_dic["sport_key"]}/odds/'''
        f'''?apiKey={api_key}'''
        f'''&regions={odds_dic["regions"]}'''
        f'''&markets={odds_dic["markets"]}''')

def get_sports_list():
    url = sports_url()
    data = general_get_req(url)
    f = lambda x: {"sport": x["title"], "key": x["key"]}
    sports = list(map(f, data))
    for sport in sports:
        print(sport, end='\n\n')

def get_odds():
    odds_dic = {"sport_key": "aussierules_afl", "regions": "au", "markets": "h2h" }
    url = odds_url(odds_dic)
    data = general_get_req(url)
    test_game = data[0]
    return 1
    # for bet in data:
    #     print(bet, end='\n\n')

def main():
    # get_sports_list()
    get_odds()

if __name__ == '__main__':
    main()

