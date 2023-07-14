from arb_finder import *

def test_yield():
    prices = [3.05, 3.3, 2.82]
    # prices = [2.66, 1.62]
    n = len(prices)
    total = 60
    ev = get_EV(*prices)
    if n == 2:
        s1, s2 = calc_yield(total, *prices)
    if n == 3:
        s1, s2, s3 = calc_yield(total, *prices)
    total_ret = s1 * prices[0]
    total_prof = total_ret - total
    prof_perc = total_prof / total * 100
    
    print(f"EV: {ev}")
    print(f"Willing to spend: {total}")
    if n == 2:
        print(f"Stake1: ${s1}, Stake2: ${s2}")
    if n == 3:
        print(f"Stake1: ${s1}, Stake2: ${s2}, Stake3: ${s3}")
    print(f"Total returned: {s1 * prices[0]}")
    print(f"Profit: ${total_prof} ({prof_perc}%)")

    print(f"theorised % prof: {perc_profit(*prices)}")

def test_sample_arb():
    data = [
        {
            "profit": 9.00,
            "sport": "NCAA",
            "game": "Duke v UNC",
            "outcomes": [
            {
                "price": 1.84,
                "team": "Duke",
                "book": "Betway"
            },
            {
                "price": 2.18,
                "team": "UNC",
                "book": "William Hill"
            },
            None
        ],
        "region": "au"
        },
        {
            "profit": 7.50,
            "sport": "NBA",
            "game": "Lakers v Clippers",
            "outcomes": [
            {
                "price": 2.05,
                "team": "Lakers",
                "book": "Bet365"
            },
            {
                "price": 2.35,
                "team": "Clippers",
                "book": "Bwin"
            },
            {
                "price": 4.1,
                "team": "Draw",
                "book": "Bwin"
            }
        ],
        "region": "us"
    }]
    return data

def test_db(sport_file, first_time):
    db = ArbDB()
    sport_keys = get_sports_list(sport_file, not first_time)
    db.insert_sports(sport_keys)

def main():
    test_yield()

if __name__ == '__main__':
    main()
