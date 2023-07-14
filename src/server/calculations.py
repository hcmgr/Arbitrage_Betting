"""
calculations.py is the brains of the apparatus

It's purpose is two-fold:
    - perform EV, yield, perc gain etc. calculations 
    - handle combination/permutation logic
"""
import messages as msgs

"""
Returns the sum of reciprocals of the given outcomes
NOTE: used to calculate expected value of n-many outcomes
    eg: if 1/o1 + 1/o2 < 1, arbitrage opportunity
"""
def get_EV(*outcome_odds):
    total = 0
    for o in outcome_odds:
        total += (1/o)
    return total

"""
Given a total one is willing to spend,
calculate the amount one should stake on each outcome
TODO: make arbitrary for n-many odds
"""
def calc_yield(total, *outcome_odds):
    n = len(outcome_odds)
    if n == 2:
        o1, o2 = outcome_odds
        s1 = total / (1 + o1/o2)
        s2 = total - s1
        return s1, s2
    elif n == 3:
        o1, o2, o3 = outcome_odds
        s1 = total / (1 + (o1/o2) + (o1/o3))
        s2 = total / (1 + (o2/o1) + (o2/o3))
        s3 = total / (1 + (o3/o1) + (o3/o2))
        return s1,s2,s3
    else:
        print(msgs.not_2_3_outcome_err())
        return None

"""
Calculates %profit of an arbitrage opportunity
NOTE: we only need odds to compute this
"""
def perc_profit(*outcome_odds):
    n = len(outcome_odds)
    o1 = outcome_odds[0]
    total = 1
    for i in range(1, n):
        total += (o1/outcome_odds[i])
    return ((o1 / total) - 1) * 100

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

"""
For the given outcomes list, return all n-tuple combinations
TODO: make arbitary for all n-tuples (only 2 and 3 atm)
"""
def get_outcome_combos(outcomes, n):
    ## check all same number of outcomes
    if any(len(outcome) != n for outcome in outcomes):
        return None
    if n == 2:
        return get_outcome_pairs(*outcomes)
    elif n == 3:
        return get_outcome_trips(*outcomes)
    else:
        print(msgs.not_2_3_outcome_err())
    return None

"""
Returns all possible permutations of indexes 0 - length-1
"""
def get_all_index_combos(length, n):
    els = [i for i in range(length)]
    return list(combinations(els, n))