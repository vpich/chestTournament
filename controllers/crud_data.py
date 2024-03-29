from tinydb import TinyDB, Query
from pathlib import Path

from models import Tournament, Player, Round, Match
from views import CrudViews
from .checks import Check

from .tournaments import TournamentsController
from . import tournaments

all_tournaments = tournaments.all_tournaments
tournaments_self = TournamentsController()
db = TinyDB("db.json")
db_file_path = Path("db.json")


class Data:

    @staticmethod
    def save(tournaments_to_save):
        for tournament in tournaments_to_save:
            tournament.save()
        CrudViews.save()

    @staticmethod
    def delete_tournament(indice):
        query = Query()
        db.remove(query.id == f"{indice}")

    @staticmethod
    def delete():
        if Check.deletion():
            all_tournaments.tournaments = []
            db.truncate()
            CrudViews.delete()
            TournamentsController.main(tournaments_self)
        else:
            CrudViews.cancel_delete()
            TournamentsController.main(tournaments_self)

    @staticmethod
    def load():
        if not db_file_path.exists():
            CrudViews.file_not_found()
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
            CrudViews.load(db.all())
