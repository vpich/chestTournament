class Match:
    # chaque match doit être stocké sous la forme d'un tuple de 2 listes:
    # - une instance de joueur
    # - et un score
    def __init__(self, player_one, player_two):
        self.contestants = [player_one, player_two]
        self.scores = []
        self.in_progress = True

    def __str__(self):
        if self.in_progress:
            return f"Cette partie oppose {self.contestants[0]} à {self.contestants[1]}, la partie est en cours."
        else:
            return f"Cette partie oppose {self.contestants[0]} à {self.contestants[1]}, la partie est terminée."

    def add_score_to_winner(self, winner: Player = None):
        score_player_one = 0
        score_player_two = 0

        if winner is None:
            score_player_one = 0.5
            score_player_two = 0.5
            self.contestants[0].points_gagnes += score_player_one
            self.contestants[1].points_gagnes += score_player_two
        elif winner == self.contestants[0]:
            score_player_one = 1
            self.contestants[0].points_gagnes += score_player_one
        elif winner == self.contestants[1]:
            score_player_two = 1
            self.contestants[1].points_gagnes += score_player_two

        self.scores.append(score_player_one)
        self.scores.append(score_player_two)
        self.in_progress = False
