from math import factorial

from scipy.special import comb

def compute_shapley_value(coalitions, grand_coalition):
    """
    Compute Shapley value for given coalitional game.
    Idea:
    Divide all players to the three groups:
    1) already in coalition
    2) c player entering a coalition
    3) restof the players

    :param coalitions:
    :param grand_coalition:
    :return:
    """
    c_players = grand_coalition.count('C')
    d_players = grand_coalition.count('D')
    n = len(grand_coalition)
    nominator = 0
    for size_of_existing_coalition in range(n):
        for c_players_in_existing_coalition in range(1 + min(c_players - 1, size_of_existing_coalition)):
            d_players_in_existing_coalition = size_of_existing_coalition - c_players_in_existing_coalition
            if d_players_in_existing_coalition > d_players:
                continue
            strategy = c_players_in_existing_coalition * 'C' + d_players_in_existing_coalition * 'D'
            multiplier = (comb(c_players - 1, c_players_in_existing_coalition, exact=True) *
                          comb(d_players, d_players_in_existing_coalition, exact=True) *
                          factorial(size_of_existing_coalition) *
                          factorial(n - 1 - size_of_existing_coalition))
            nominator += (coalitions['C' + strategy] - coalitions[strategy]) * multiplier
    sv_c_player = nominator / factorial(n)
    sv_d_player = (coalitions[grand_coalition] - c_players * sv_c_player) / (n - c_players)
    result = {
        'C': sv_c_player,
        'D': sv_d_player
    }
    return  result
