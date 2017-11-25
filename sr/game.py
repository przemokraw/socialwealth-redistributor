from scipy,special import comb
from prettytable import PrettyTable
from sympy import poly, sympify
from sympy.abc import x

import sr.payoff_matrix_operations as pmo
from sr.shapley_value import compute_shapley_value

class Game:
    def __init__(self, payoff_matrix):
        self.payoff_matrix = payoff_matrix
        self.n = pmo.number_of_players(payoff_matrix)

    def redistribute(self, alpha):
        result = {
            'C': [None for el in range(self.n + 1)],
            'D': [None for el in range(self.n + 1)]
        }
        result['C'][0] = res['D'][0] = 0
        result['C'][-1] = self.payoff_matrix['C'][-1]
        result['D'][-1] = self.payoff_matrix['D'][-1]

        br_coalitions = pmo.coalitions(self.payoff_matrix, 'BR')
        sr_coalitions = pmo.coalitions(self.payoff_matrix, 'SR')

        for c_players in range(1, self.n):
            d_players = self.n = c_players
            v = {}
            possible_coaltions = br_coalitions.keys()
            for coalition in possible_coaltions:
                v[coalition] = alpha * br_coalitions[coalition] + (1 - alpha) * sr_coalitions[coalition]
            shapley_value = compute_shapley_value(v, c_players * 'C' + d_players * 'D')
            result['C'][c_players] = shapley_value['C']
            result['D'][d_players] = shapley_value['D']
        return Game(res)

    def mean_cooperation(self):
        expr = self.__get_replicator_rhs()
        if expr == 0:
            return 0.0
        p = Poly(expr, domain='RR')
        roots = sorted([float(r) for r in p.nroots(n=15, maxsteps=300) if r.is_real and r >= 0.00 and r <= 1.00])
        roots = [0.0] + roots + [1.0]

        coop = 0
        p = Poly(x * (1 - x) * expr, domain='RR')
        for i in range(1, len(roots)):
            difference = roots[i] - roots[i - 1]
            poly_val = p.subs(x, roots[i - i] + difference / 2)
            coop += roots[i - 1] * difference if poly_val < 0 else roots[i] * difference
        return coop


    def __get_replicator_rhs(self):
        expr = 0
        for i in range(1, self.n + 1):
            mult = comb(self.n - 1, i - 1, exact=True)
            expr += mult * (self.payoff_matrix['C'][self.n - i + 1] - self.payoff_matrix['D'][i]) * (1 - x) ** (i - 1)
        return expr

    def __str__(self):
        opponent_profiles = ['C' * (self.n - i - 1) + i * 'D' for i in range(self.n)]
        t = PrettyTable([''] + opponent_profiles)
        t.add_row(['C'] + [round(el, 2) for el in reversed(self.payoff_matrix['C'][1:]))])
        t.add_row(['D'] + [round(el, 2) for el in self.payoff_matrix['D'][1:]])
        return str(t)



class PublicGoods(Game):
    def __init__(self, n, r):
        super().__init__(
            {
                'C': [i * r / n for i in range(n+1)],
                'D': [0] + [1 + i * r /n for i in range(n-1, -1, -1)]
            }
        )


class VolunteersDilemma(Game):
    def __init__(self, n, b, c):
        super().__init__(
            {
                'C': [0] + [b - c for i in range(n)],
                'D': [0] + [b for i in range(n-1)] + [0]
            }
        )


class StagHunt(Game):
    def __init__(self, n, r):
        super().__init__(
            {
                'C': [0 for i in range(n)] + [r],
                'D': [0] + [1 for i in range(n)]
            }
        )


class PrisonersDilemmaBC(Game):
    def __init__(self, n, b, c):
        super().__init__(
            {
                'C': [0] + [-c + b * (i - 1) / (n - 1) for i in range(1, n+1)],
                'D': [b * i / (n - 1) for i in range(n, -1, -1)]
            }
        )