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

    def __str__(self):
        return f"{self.name}"

    def add_players(self, player):
        assert type(player) == Player
        self.players.append(player)

    def delete_player(self, player):
        assert type(player) == Player
        self.players.remove(player)

    def add_round(self, round):
        self.rounds.append(round)

    def delete_round(self, round):
        self.rounds.remove(round)

    def order_players_by_last_name(self):
        self.players.sort(key=lambda player: player.lastname)
        # for player in self.players:
        #     print(player)

    def order_players_by_points_and_ranks(self):
        self.players.sort(key=lambda player: (player.points_gagnes, player.rank))
        # for player in self.players:
        #     print(player)
