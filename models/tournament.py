from .player import Player
from tinydb import TinyDB, Query


class Tournament:
    def __init__(self, id, name, place, date, time_control, number_of_rounds: int = 4):
        self.id = id
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
        return f"Tournoi {self.name}"

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
        self.players.sort(key=lambda player: (player.total_points, player.rank))
        self.players.reverse()
        # for player in self.players:
        #     print(player)

    def save(self):
        db = TinyDB("db.json")
        data_rounds = []
        for round in self.rounds:
            data_matches = []
            for match in round.matches:
                data_matches.append({"Type": "Match",
                                     "Player1": f"{match.contestants[0]}",
                                     "Player2": f"{match.contestants[1]}",
                                     "ScorePlayer1": f"{match.scores[0]}",
                                     "ScorePlayer2": f"{match.scores[1]}",
                                     "InProgress": f"{match.in_progress}"})
            data_rounds.append({"Type": "Round",
                                "Name": f"{round.name}",
                                "Matches": data_matches})
        data_players = []
        for player in self.players:
            data_players.append({"Type": "Player",
                                 "Firstname": f"{player.firstname}",
                                 "Lastname": f"{player.lastname}",
                                 "Gender": f"{player.gender}",
                                 "DateOfBirth": f"{player.date_of_birth}",
                                 "Rank": f"{player.rank}",
                                 "TotalPoints": f"{player.total_points}"})
        data_tournoi = {"id": f"{self.id}",
                        "Name": f"{self.name}",
                        "Place": f"{self.place}",
                        "Date": f"{self.date}",
                        "TimeControl": f"{self.time_control}",
                        "Rounds": data_rounds,
                        "Description": f"{self.description}",
                        "Players": data_players}
        query = Query()
        exist = db.search(query.id == str(self.id))

        if exist:
            db.update(data_tournoi, query.id == f"{self.id}")
        else:
            db.insert(data_tournoi)
