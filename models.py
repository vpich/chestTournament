from datetime import datetime


class Player:
    def __init__(self, firstname, lastname, date_of_birth, gender, rank: int = 0):
        self.firstname = firstname
        self.lastname = lastname
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.rank = rank

    def __str__(self):
        return f"Joueur {self.firstname} {self.lastname}, classement: {self.rank}"


class Tournament:
    def __init__(self, name, place, date, time_control, number_of_rounds: int = 4):
        self.name = name
        self.place = place
        # la date pourra à l'avenir être plusieurs jours, et pas juste un jour
        self.date = date
        # le time_control sera forcément "bullet", "blitz" ou "coup rapide"
        self.time_control = time_control
        self.number_of_rounds = number_of_rounds

        self.rounds = []
        self.players = []
        # description = remarques générales du directeur de tournoi
        self.description = ""

    def add_players(self, player):
        assert type(player) == Player
        self.players.append(player)

    def delete_player(self, player):
        assert type(player) == Player
        self.players.remove(player)

    def add_round(self, round):
        self.rounds.append(round)

    def order_players_by_last_name(self):
        self.players.sort(key=lambda player: player.lastname)
        for player in self.players:
            print(player)

    def order_players_by_rank(self):
        self.players.sort(key=lambda player: player.rank)
        for player in self.players:
            print(player)


class Match:
    # chaque match doit être stocké sous la forme d'un tuple de 2 listes:
    # - une instance de joueur
    # - et un score
    def __init__(self, player_one, player_two):
        self.contestants = [player_one, player_two]
        self.scores = []

    def __str__(self):
        if not self.scores:
            return f"Cette partie oppose {self.contestants[0]} à {self.contestants[1]}, la partie est en cours."
        else:
            return f"Cette partie oppose {self.contestants[0]} à {self.contestants[1]}, la partie est terminé."

    def add_score_to_winner(self, winner: Player = None):
        score_player_one = 0
        score_player_two = 0

        if winner is None:
            score_player_one += 0.5
            score_player_two += 0.5
        elif winner == self.contestants[0]:
            score_player_one += 1
        elif winner == self.contestants[1]:
            score_player_two += 1

        self.scores.append(score_player_one)
        self.scores.append(score_player_two)


class Round:
    def __init__(self, name):
        self.name = name
        self.matches = []

        self.start_time = None
        self.end_time = None

    def __str__(self):
        return f"{self.name}"

    def add_match(self, match):
        self.matches.append(match)

    def starting(self):
        self.start_time = datetime.now()

    def ending(self):
        self.end_time = datetime.now()


joueur_1 = Player("Patrick", "Roger", "hier", "M", 12)
joueur_2 = Player("Sylvia", "Oliveira", "hier", "F", 1)
joueur_3 = Player("Jeannot", "Lumière", "hier", "M", 4)
joueur_4 = Player("Pouet", "Prout", "hier", "NA", 89)

tournoi_test = Tournament("Tournoi test", "place", "date", "time control")
tournoi_test.add_players(joueur_1)
tournoi_test.add_players(joueur_2)
tournoi_test.add_players(joueur_3)
tournoi_test.add_players(joueur_4)

tournoi_test.order_players_by_last_name()
print("=====")
tournoi_test.order_players_by_rank()
