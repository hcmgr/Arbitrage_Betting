import os
import requests
import json
from dotenv import load_dotenv
import textwrap
from itertools import combinations

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
                    trips.append((o1s[i], o2s[j], o3s[k]))
    return trips

def get_outcome_combos(outcomes, n):
    ## check all same number of outcomes
    if any(len(outcome) != n for outcome in outcomes):
        return None

    if n == 2:
        return get_outcome_pairs(*outcomes)
    if n == 3:
        return get_outcome_trips(*outcomes)

    return None

def get_n_tuple_combos(length, n):
    els = [i for i in range(length)]
    return list(combinations(els, n))

"""
Returns an 'arb', which is a dictionary holding the expected
value and bookie data of a given arbitrage opportunity
"""
def build_arb(ev, bookie_bet_combos):
    arb = {"ev": ev}
    for bookie, bet in bookie_bet_combos:
        arb[bookie["key"]] = {"team": bet["name"], "price": bet["price"]}
    return arb

def check_bookie_valid(bookie):
    markets = bookie.get("markets", None)
    return (markets != None and 
            len(markets) != 0 and
            markets[0]["outcomes"] != None)

def get_outcome_arbs(bookies, limit=1):
    outcomes = [b["markets"][0]["outcomes"] for b in bookies]
    outcome_combos = get_outcome_combos(outcomes, len(outcomes[0]))
    if not outcome_combos:
        return []

    arbs = []
    for combo in outcome_combos:
        prices = [o["price"] for o in combo]
        ev = get_EV(*prices)
        if ev < limit:
            arbs.append(build_arb(ev, zip(bookies, combo)))
    return arbs

def find_game_arbs(game):
    bookmakers = game.get("bookmakers", None)

    ## handle empty bookmakers
    if not bookmakers:
        # print(no_bookies_found_err(game))
        return None

    arbs = []
    n = len(bookmakers)

    num_outcomes = 3
    ind_combos = get_n_tuple_combos(n, num_outcomes)
    
    for inds in ind_combos:
        bookies = [bookmakers[x] for x in inds]
        if False in list(map(check_bookie_valid, bookies)):
            continue
        new_arbs = get_outcome_arbs(bookies, limit=1)
        arbs += new_arbs
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
        
    sport_ind = 2
    sample_sports = ["aussierules_afl", "rugbyleague_nrl", "boxing_boxing", "soccer_sweden_allsvenskan"]
    test_sport = {"sport_key": sample_sports[sport_ind], "regions": "au", "markets": "h2h"}

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