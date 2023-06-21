### messages.py ###
"""
Handles all error messages and encodings
"""

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
        f"""---------\n"""
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