### messages.py ###
"""
Handles all error messages and encodings
"""

def divider():
    return "--------------\n"

def checking_sport(sport_key):
    msg = (
        f"""Checking {sport_key} for arb opporunities... \n"""
    )
    return msg

def game_to_str(game):
    msg = (
        f"""    id: {game["id"]} \n"""
        f"""    sport_key: {game["sport_key"]} \n"""
        f"""    game: {game["home_team"]} vs {game["away_team"]}"""
    )
    return msg

def arb_to_str(arb, game):
    msg = (
        f"""{game_to_str(game)}\n\n"""
        f"""{arb}"""
        f"""\n"""
    )
    return msg

def no_sport_data_found_err(sport_key):
    msg = (
        f"""No odds found for {sport_key}\n"""
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

def not_2_3_outcome_err():
    msg = "Only handle 2 or 3 outcomes games"
    return msg