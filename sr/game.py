class Game:
    def __init__(self, payoff_matrix):
        self.payoff_matrix = payoff_matrix
        self.n = len(payoff_matrix['C']) - 1

    def redistribute(self, alpha):
        pass

    def compute_cooperation(self):
        pass

    def __str__(self):
        return ""


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