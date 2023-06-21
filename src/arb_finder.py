### arb_finder.py ###

"""
Main driver code of project
"""

import json
import textwrap
from itertools import combinations

import messages as msgs
import odds_requests as reqs

def get_sports_list(filename=None):
    sports = []

    if filename: ## retreive from file
        with open(filename, "r") as file:
            for line in file:
                if line.startswith("## "): ## commented out sport
                    continue
                line = line.strip()  
                sports.append(line)

    else: ## retreive from API
        url = reqs.sports_url()
        data = reqs.general_get_req(url)
        f = lambda x: x["key"]
        sports = list(map(f, data))

    return sports

"""
Write all possible sports to a file 'sports_list'
NOTE: so we don't torch our API limit before
      we've got a db up and running 
"""
def write_sports_to_file():
    all_sport_keys = get_sports_list()
    filename = "utils/sports_list.txt"
    f = open(filename, "w")
    for sport in all_sport_keys:
        f.write(str(sport) + '\n')
    f.close()

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
    num_outcomes = [len(b["markets"][0]["outcomes"]) for b in bookies]
    return most_frequent_element(num_outcomes)

def find_game_arbs(game, limit=1):
    bookmakers = game.get("bookmakers", [])

    ## handle empty bookmakers
    if len(bookmakers) <= 1:
        # print(no_bookies_found_err(game))
        return None

    arbs = []
    n = len(bookmakers)

    num_outcomes = find_num_outcomes(bookmakers)
    ind_combos = get_n_tuple_combos(n, num_outcomes)
    
    for inds in ind_combos:
        bookies = [bookmakers[x] for x in inds]
        if False in list(map(check_bookie_valid, bookies)):
            continue
        new_arbs = get_outcome_arbs(bookies, limit=limit)
        arbs += new_arbs
    return arbs

def find_sport_arbs(all_games_data, limit=1):
    for game in all_games_data:
        arbs = find_game_arbs(game, limit=limit)
        if arbs and len(arbs) > 0:
            for arb in arbs:
                print(msgs.arb_to_str(arb, game))
    return None

def find_arbs_all_sports(sport_keys, regions, markets, limit=1, sport_file=None):
    sport_obj = {"sport_key": None, "regions": regions, "markets": markets}

    for s_key in sport_keys:
        print(msgs.checking_sport(s_key))
        sport_obj["sport_key"] = s_key
        url = reqs.odds_url(sport_obj)
        data = reqs.general_get_req(url)
        if not data:
            # print(msgs.no_sport_data_found_err(s_key))
            continue
        find_sport_arbs(data, limit=limit)
    return None

def main():
    first_time = False ## NOTE CHANGE TO TRUE IF FIRST TIME RUNNING NOTE ##
    testing = False ## NOTE CHANGE TO TRUE IF WANT TO FULLY SEARCH FOR ABRS NOTE ##
    regions = "au,eu,us,us2,uk"
    markets = "h2h"
    limit = 1

    sport_file = "src/utils/sports_list.txt"
    if first_time:
        write_sports_to_file(sport_file)
    
    if testing:
        sport_keys = ["aussierules_afl", "rugbyleague_nrl"]
    else:
        sport_keys = get_sports_list(sport_file)
    
    find_arbs_all_sports(sport_keys, regions, markets, limit=limit)
    
if __name__ == '__main__':
    main()