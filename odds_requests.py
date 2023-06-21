### requests.py ###
"""
Handles all requests made to Odds API
"""

from dotenv import load_dotenv
import os
import requests

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