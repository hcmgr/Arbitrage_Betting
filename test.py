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

def game_to_str(game):
    msg = (
        f"""    id: {game["id"]} \n"""
        f"""    sport_key: {game["sport_key"]} \n"""
        f"""    game: {game["home_team"]} vs {game["away_team"]}"""
    )
    return msg

def no_bookies_found_err(game):
    msg = (
        f"""No bookmakers offered for following game: \n"""
        f"""{game_to_str(game)}"""
    )
    return msg

def no_market_offered_err(game, bookmaker):
    msg = (
        f"""Bookmaker: {bookmaker["key"]}\n"""
        f"""offers no markets for the following game: \n"""
        f"""{game_to_str(game)}"""
    )
    return msg

def get_sports_list():
    url = sports_url()
    data = general_get_req(url)
    f = lambda x: x["key"]
    return list(map(f, data))

def EV(o1, o2):
    return (1/o1) + (1/o2)

def build_arb(ev, bookie1, bet1, bookie2, bet2):
    b1 = {"key": bookie1, "team": bet1["name"], "price": bet1["price"]}
    b2 = {"key": bookie2, "team": bet2["name"], "price": bet2["price"]}
    return {"ev": ev, "bookie1": b1, "bookie2": b2}

"""
For a given game, find all arbs between the markets
of different bookies

NOTE: find outline of JSON structure at EOF
"""
def find_game_arbs(game):
    bookmakers = game.get("bookmakers", None)

    ## handle empty bookmakers
    if not bookmakers:
        # print(no_bookies_found_err(game))
        return None

    arbs = []
    n = len(bookmakers)

    ## retreive h2h markets offered by all pairs of bookies
    for i in range(n):
        b1 = bookmakers[i]
        b1_markets = b1.get("markets", None)

        ## handle empty markets
        if not b1_markets or len(b1_markets) == 0: 
            # print(no_market_offered_err(game, bookmakers[i]))
            continue

        for j in range(i+1, n):
            b2 = bookmakers[j]
            b2_markets = b2.get("markets", None)

            ## handle empty markets
            if not b2_markets or len(b2_markets) == 0: 
                # print(no_market_offered_err(game, bookmakers[j]))
                continue

            b1_home = b1_markets[0]["outcomes"][0]; b1_away = b1_markets[0]["outcomes"][1]
            b2_home = b2_markets[0]["outcomes"][1]; b2_away = b2_markets[0]["outcomes"][1]

            ## calculate and add arbs
            """
            TODO:
                -currently assumes home team listed first and away second
                -this is actually not guaranteed, so need to account for this
            """
            ev1 = EV(b1_home["price"], b2_away["price"])
            ev2 = EV(b1_away["price"], b2_home["price"])
            limit = 1.01
            if ev1 < limit:
                arbs.append(build_arb(ev1, b1["key"], b1_home, b2["key"], b2_away))
            if ev2 < limit:
                arbs.append(build_arb(ev2, b1["key"], b1_away, b2["key"], b2_home))
    return arbs

def main():
    all_sport_keys = get_sports_list() ## all available sports
    sport = "soccer_sweden_allsvenskan" ## sample sport
    test_sport = {"sport_key": sport, "regions": "au", "markets": "h2h"}
    url = odds_url(test_sport)
    data = general_get_req(url)
    for game in data:
        arbs = find_game_arbs(game)
        print(arbs, end="\n\n")

if __name__ == '__main__':
    main()

## NOTE: below is the JSON structure of a game ##

"""
Odds json 'game' structure:
    game (a given game ie: data[0], where data == the raw HTTP request data)

        id

        sport_key

        sport_title

        commence_time

        home_team

        away_team

        bookmakers
            bookie (ie: unibet, neds etc.)
                {
                    ...
                    ...
                    markets (list of dicts, usually len 1 (just h2h))
                        market (dic rep. given market, again, usually h2h)
                            ...
                            ...
                            outcomes (len 2 list)
                                home odds
                                away odds
                }
"""