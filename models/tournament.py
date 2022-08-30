from .player import Player
from tinydb import TinyDB, Query


class Tournament:
    def __init__(self, tournament_id, name, place, date, time_control, number_of_rounds: int = 4):
        self.tournament_id = tournament_id
        self.name = name
        self.place = place
        self.date = date
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

    def order_players_by_points_and_ranks(self):
        self.players.sort(reverse=True, key=lambda player: (player.total_points, player.rank))

    def save(self):
        db = TinyDB("db.json")
        data_rounds = []
        for round in self.rounds:
            data_matches = []
            for match in round.matches:
                data_matches.append({"Player1": f"{match.contestants[0]}",
                                     "Player2": f"{match.contestants[1]}",
                                     "ScorePlayer1": f"{match.scores[0]}",
                                     "ScorePlayer2": f"{match.scores[1]}",
                                     "InProgress": f"{match.in_progress}"})
            data_rounds.append({"Name": f"{round.name}",
                                "Matches": data_matches})
        data_players = []
        for player in self.players:
            data_players.append({"Firstname": f"{player.firstname}",
                                 "Lastname": f"{player.lastname}",
                                 "Gender": f"{player.gender}",
                                 "DateOfBirth": f"{player.date_of_birth}",
                                 "Rank": f"{player.rank}",
                                 "TotalPoints": f"{player.total_points}"})
        data_tournoi = {"id": f"{self.tournament_id}",
                        "Name": f"{self.name}",
                        "Place": f"{self.place}",
                        "Date": f"{self.date}",
                        "TimeControl": f"{self.time_control}",
                        "Rounds": data_rounds,
                        "Description": f"{self.description}",
                        "Players": data_players}
        query = Query()
        exist = db.search(query.id == str(self.tournament_id))

        if exist:
            db.update(data_tournoi, query.id == f"{self.tournament_id}")
        else:
            db.insert(data_tournoi)

    def get_players_history(self):
        # example = {
        #     "Sofien": ["Virginie", "Toto"],
        #     "Virginie": ["Sofien", "Tata"],
        #     "Toto": ["Sofien", "Tata"],
        #     "Tata": ["Virginie", "Toto"]
        # }

        # to do: faire un id pour les players et l'utiliser ici
        players_history = {player.firstname: [] for player in self.players}

        for current_round in self.rounds:
            for match in current_round.matches:
                players_history[match.contestants[0].firstname].append(match.contestants[1])
                players_history[match.contestants[1].firstname].append(match.contestants[0])
        return players_history
