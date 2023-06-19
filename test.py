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

"""
Returns the sum of reciprocals of the given outcomes
NOTE: used to calculate expected value of n-many outcomes
    eg: if 1/o1 + 1/o2 < 1, arbitrage opportunity
"""
def get_EV(*outcomes):
    total = 0
    for o in outcomes:
        total += (1/o)
    return total

"""
Returns all pairs (2-tuples) of outcomes
"""
def get_outcome_pairs(o1s, o2s):
    pairs = []
    n = 2
    if len(o1s) != n or len(o2s) != n:
        return None
    for i in range(n):
        for j in range(n):
            if i != j:
                pairs.append((o1s[i], o2s[j]))
    return pairs

"""
Returns all triples (3-tuples) of outcomes
"""
def get_outcome_trips(o1s, o2s, o3s):
    trips = []
    n = 3
    if len(o1s) != n or len(o2s) != n or len(o3s) != n:
        return None

    for i in range(n):
        for j in range(n):
            for k in range(n):
                if i != j and j != k and i != k:
                    trips.append(o1s[i], o2s[j], o3s[k])
    return trips

"""
TODO:
    -works for 2-outcome (ie: WIN/LOSS)
    -now make work for 3-outcome (ie: WIN/LOSS/DRAW)
"""
def get_outcome_arbs(b1_key, b1_outs, b2_key, b2_outs, limit=1):
    pairs = get_outcome_pairs(b1_outs, b2_outs)
    arbs = []
    for bet1, bet2 in pairs:
        ev = get_EV(bet1["price"], bet2["price"])
        if ev < limit:
            arbs.append(build_arb(ev, b1_key, bet1, b2_key, bet2))
    return arbs

"""
Returns an 'arb', which is a dictionary holding the expected
value and bookie data of a given arbitrage opportunity
"""
def build_arb(ev, bookie1, bet1, bookie2, bet2):
    b1 = {"bookie_name": bookie1, "team": bet1["name"], "price": bet1["price"]}
    b2 = {"bookie_name": bookie2, "team": bet2["name"], "price": bet2["price"]}
    return {"ev": ev, "bookie1": b1, "bookie2": b2}


"""
For a given game, find all arbs between the markets
of different bookies

NOTE: find outline of JSON structure at EOF

TODO:
    -works for 2-outcome (ie: WIN/LOSS)
    -now make work for 3-outcome (ie: WIN/LOSS/DRAW)
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
        if not b1_markets or len(b1_markets) == 0: 
            continue

        b1_outs = b1_markets[0]["outcomes"]
        if not b1_outs:
            continue

        for j in range(i+1, n):
            b2 = bookmakers[j]
            b2_markets = b2.get("markets", None)
            if not b2_markets or len(b2_markets) == 0: 
                continue
                
            b2_outs = b2_markets[0]["outcomes"]
            if not b2_outs:
                continue

            res = get_outcome_arbs(b1["key"], b1_outs, b2["key"], b2_outs, limit=1.01)
            arbs += res
        
    return arbs

"""
Write all possible sports to a file 'sports_list'
NOTE: so we don't torch our API limit before
      we've got a db up and running 
"""
def write_sports_to_file():
    all_sport_keys = get_sports_list()
    filename = "sports_list.txt"
    f = open(filename, "w")
    for sport in all_sport_keys:
        f.write(str(sport) + '\n')
    f.close()

def main():
    first_time = False ## NOTE : SET TRUE ONLY FOR FIRST RUN : NOTE
    if first_time:
        write_sports_to_file()
        
    sport_ind = 0
    sample_sports = ["aussierules_afl", "rugbyleague_nrl", "boxing_boxing", "soccer_sweden_allsvenskan"]
    test_sport = {"sport_key": sample_sports[0], "regions": "au", "markets": "h2h"}

    url = odds_url(test_sport)
    data = general_get_req(url)

    for game in data:
        arbs = find_game_arbs(game)
        for arb in arbs:
            if len(arbs) > 0:
                print(game_to_str(game), end="\n\n")
                print(arb)
                print("-------\n")
    return 0

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