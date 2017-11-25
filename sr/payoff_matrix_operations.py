def number_of_players(matrix):
    return len(matrix['C']) - 1

def coalition_payoff(matrix, coaliton_strategy: string, opponent_strategy: string):
    grand_coalition = coaliton_strategy + opponent_strategy
    profile = tuple(grand_coalition.count(a) for a in ['C', 'D'])
    pc = matrix['C'][profile[0]]
    pd = matrix['D'][profile[1]]
    return coaliton_strategy.count('C') * pc + coaliton_strategy.count('D') * pd

def best_reply_payoff(matrix, coalition_strategy):
    n = number_of_players(matrix)
    size_of_opponent_coalition = n - len(coalition_strategy)
    best_opponent_payoff = 0
    best_opponent_num_of_c_players = -1
    for c_players in range(size_of_opponent_coalition+1):
        d_players = size_of_opponent_coalition - c_players
        opponent_strategy = c_players * 'C' + d_players * 'D'
        opponent_payoff = coalition_payoff(matrix, opponent_strategy, coalition_strategy)
        if opponent_payoff > best_opponent_payoff:
            best_opponent_payoff = opponent_payoff
            best_opponent_num_of_c_players = c_players

    best_opponent_num_of_d_players = size_of_opponent_coalition - best_opponent_num_of_c_players
    best_opponent_strategy = best_opponent_num_of_c_players * 'C' + best_opponent_num_of_d_players * 'D'
    return coalition_payoff(matrix, coalition_strategy, best_opponent_strategy)

def spiteful_reply_payoff(matrix, coalition_strategy):
    n = number_of_players(matrix)
    size_of_opponent_coalition = n - len(coalition_strategy)
    possible_coalition_payoffs = []
    for c_players in range(size_of_opponent_coalition+1):
        d_players = size_of_opponent_coalition - c_players
        opponent_strategy = c_players * 'C' + d_players * 'D'
        possible_coalition_payoffs.append(coalition_payoff(
            matrix,
            coalition_strategy,
            opponent_strategy
        ))
    return min(possible_coalition_payoffs)

def coalitions(matrix, method):
    n = number_of_players(matrix)
    result = {
        "": 0 # empty coalition
    }
    # computing results for grand coalitions
    for c_players in range(n+1):
        strategy = c_players * 'C' + (n - c_players) * 'D'
        result[strategy] = coalition_payoff(matrix, strategy, '')
    # computing values of the other coalitions
    for coalition_size in range(1, n):
        for c_players in range(coalition_size + 1):
            strategy = c_players * 'C' + (coalition_size - c_players) * 'D'
            payoff_function = spiteful_reply_payoff if method == 'SR' else best_reply_payoff
            res[strategy] = payoff_function(matrix, strategy)
    return res
