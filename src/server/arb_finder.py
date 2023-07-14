### arb_finder.py ###

"""
Main driver code of project
"""
import json
import textwrap
from itertools import combinations
from db import ArbDB

import messages as msgs
import odds_requests as reqs
import calculations as calcs

def get_sports_list(filename, from_file=False):
    sports_data = []

    if from_file: ## retreive from file
        with open(filename, "r") as file:
            for line in file:
                if line.startswith("## "): ## commented out sport
                    continue
                line = line.strip()  
                sports_data.append(line)

    else: ## retreive from API, write to sports to file
        url = reqs.sports_url()
        data = reqs.general_get_req(url)
        f = lambda x: (x["key"], x["title"], x["description"])
        sports_data = list(map(f, data))
        write_sports_to_file(filename, sports_data)
    return sports_data

"""
Write all possible sports to a file 'sports_list'
NOTE: so we don't torch our API limit before
      we've got a db up and running 
"""
def write_sports_to_file(filename, sport_keys):
    f = open(filename, "w")
    for sport in sport_keys:
        f.write(str(sport) + '\n')
    f.close()



"""
Returns an 'arb', which is a dictionary holding the expected
value and bookie data of a given arbitrage opportunity
"""
def build_arb(ev, commence_time, bookie_bet_combos, min_outs):
    arb = {"profit": 0, "sport": "binky", "game": "thingo", "outcomes": [None] * min_outs}
    for i, (bookie_key, bet) in enumerate(bookie_bet_combos):
        arb_summary = {"team": bet["name"], "price": bet["price"], "book": bookie_key}
        arb["outcomes"][i] = arb_summary
    return arb

def check_bookie_valid(bookie):
    markets = bookie.get("markets", None)
    return (markets != None and 
            len(markets) != 0 and
            markets[0]["outcomes"] != None)

def get_outcome_arbs(bookies, commence_time, limit=1, min_outs=3):
    outcomes = [b["markets"][0]["outcomes"] for b in bookies]
    bookie_keys = [b["key"] for b in bookies]
    outcome_combos = calcs.get_outcome_combos(outcomes, len(outcomes))
    if not outcome_combos:
        return []

    arbs = []
    for combo in outcome_combos:
        prices = [o["price"] for o in combo]
        ev = calcs.get_EV(*prices)
        if ev < limit:
            arbs.append(build_arb(ev, commence_time, zip(bookie_keys, combo), min_outs))
    return arbs

"""
Returns the most frequent element of a list
"""
def most_frequent_element(lst):
    frequency = {}
    max_count = 0
    most_frequent = None
    
    for element in lst:
        if element in frequency:
            frequency[element] += 1
        else:
            frequency[element] = 1
        
        if frequency[element] > max_count:
            max_count = frequency[element]
            most_frequent = element
    
    return most_frequent

def find_num_outcomes(bookies):
    all_outcomes = [len(b["markets"][0]["outcomes"]) for b in bookies]
    k = most_frequent_element(all_outcomes)
    return k

def find_game_arbs(game, limit=1):
    bookmakers = game.get("bookmakers", [])

    ## handle empty bookmakers
    if len(bookmakers) <= 1:
        # print(no_bookies_found_err(game))
        return None

    arbs = []
    n = len(bookmakers)

    num_outcomes = find_num_outcomes(bookmakers)
    ind_combos = calcs.get_all_index_combos(n, num_outcomes)
    
    for inds in ind_combos:
        bookies = [bookmakers[x] for x in inds]
        if False in list(map(check_bookie_valid, bookies)):
            continue
        new_arbs = get_outcome_arbs(bookies, game.get("commence_time", "TBD"), limit=limit)
        arbs += new_arbs
    return arbs

def find_sport_arbs(all_games_data, limit=1):
    for game in all_games_data:
        arbs = find_game_arbs(game, limit=limit)
        if arbs and len(arbs) > 0:
            for arb in arbs:
                print(msgs.arb_to_str(arb, game))
    return None

def find_arbs_all_sports(sports_data, regions, markets, limit=1, sport_file=None):
    sport_obj = {"sport_key": None, "regions": regions, "markets": markets}

    for s_key, _, _ in sports_data:
        print(msgs.checking_sport(s_key))
        sport_obj["sport_key"] = s_key
        url = reqs.odds_url(sport_obj)
        data = reqs.general_get_req(url)
        
        if not data:
            # print(msgs.no_sport_data_found_err(s_key))
            continue
        find_sport_arbs(data, limit=limit)
    return None

def arb_caller(sport_file, regions="au", markets="h2h", limit=1.0, first_time=True, testing=False):
    if testing:
        sports_data = ["aussierules_afl", "rugbyleague_nrl"]
    else:
        sports_data = get_sports_list(sport_file, not first_time)
    
    find_arbs_all_sports(sports_data, regions, markets, limit)

def main():
    # regions = "au,eu,us,us2,uk" 
    regions = "au"
    markets = "h2h" 
    limit = 1.0
    first_time = True ## NOTE CHANGE TO TRUE IF FIRST TIME RUNNING NOTE ##
    testing = False ## NOTE CHANGE TO FALSE IF WANT TO FULLY SEARCH FOR ABRS NOTE ##
    sport_file = "src/server/utils/sports_list.txt"

    arb_caller(sport_file, regions, markets, limit, first_time, testing)
    
if __name__ == '__main__':
    main()
