from tinydb import TinyDB, Query
from pathlib import Path

from models import Tournament, Player, Round, Match
from .checks import Checks

from .tournaments import tournaments_controller
from . import tournaments

all_tournaments = tournaments.all_tournaments
db = TinyDB("db.json")
db_file_path = Path("db.json")


class Data:

    @staticmethod
    def save(tournaments_to_save):
        for tournament in tournaments_to_save:
            tournament.save()
        print("Enregistrement dans le fichier db.json terminé.")

    @staticmethod
    def delete_tournament(indice):
        query = Query()
        db.remove(query.id == f"{indice}")

    @staticmethod
    def delete():
        if Checks.deletion():
            all_tournaments.tournaments = []
            db.truncate()
            print("Suppression de tous les tournois du fichier db.json terminée")
            tournaments_controller()
        else:
            print("Suppression annulée")
            tournaments_controller()

    @staticmethod
    def load():
        if not db_file_path.exists():
            print("Le fichier db.json est introuvable.")
            print("Aucun chargement de données n'a pu être effectué.")
        else:
            db_file = TinyDB("db.json")
            table = db_file.table("_default")
            for tournament in table:
                tournament_id = tournament["id"]
                name = tournament["Name"]
                place = tournament["Place"]
                date = tournament["Date"]
                time_control = tournament["TimeControl"]
                number_of_rounds = int(tournament["NumberOfRounds"])
                new_tournament = Tournament(
                    tournament_id, name, place, date, time_control, number_of_rounds
                )
                new_tournament.description = tournament["Description"]
                all_tournaments.add_tournament(new_tournament)
                for player in tournament["Players"]:
                    player_id = int(player["PlayerId"])
                    firstname = player["Firstname"]
                    lastname = player["Lastname"]
                    date_of_birth = player["DateOfBirth"]
                    gender = player["Gender"]
                    rank = int(player["Rank"])
                    total_points = float(player["TotalPoints"])
                    new_player = Player(
                        player_id, firstname, lastname, date_of_birth, gender, rank
                    )
                    new_player.total_points = total_points
                    new_tournament.add_players(new_player)
                for tournament_round in tournament["Rounds"]:
                    name = tournament_round["Name"]
                    new_round = Round(name)
                    new_round.start_time = tournament_round["StartTime"]
                    if tournament_round["EndTime"] == "None":
                        new_round.end_time = None
                    else:
                        new_round.end_time = tournament_round["EndTime"]
                    new_tournament.add_round(new_round)
                    for match in tournament_round["Matches"]:
                        player1 = match["Player1"]
                        player2 = match["Player2"]
                        contestants = []
                        for player in new_tournament.players:
                            for other_player in new_tournament.players:
                                if (
                                        other_player != player
                                        and str(player) == player1
                                        and str(other_player) == player2
                                ):
                                    contestants.append(player)
                                    contestants.append(other_player)
                        new_match = Match(contestants[0], contestants[1])
                        new_match.scores = [
                            float(match["ScorePlayer1"]),
                            float(match["ScorePlayer2"]),
                        ]
                        in_progress_bool = None
                        if match["InProgress"] == "True":
                            in_progress_bool = True
                        elif match["InProgress"] == "False":
                            in_progress_bool = False
                        new_match.in_progress = bool(in_progress_bool)
                        new_match.result = (new_match.contestants, new_match.scores)
                        new_round.add_match(new_match)
            if not db.all():
                print("Aucune donnée n'a été chargée.")
            else:
                print("Chargement du fichier db.json terminé.")
