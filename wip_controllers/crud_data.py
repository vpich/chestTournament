from tinydb import TinyDB

from models import AllTournaments, Tournament, Player, Round, Match

all_tournaments = AllTournaments()
db = TinyDB("db.json")


def save_data(tournaments):
    for tournament in tournaments:
        tournament.save()
    print("Enregistrement terminé.")
    tournaments_controller()


def delete_data():
    file_to_delete = input("Entrez le chemin du fichier à supprimer: ")
    db_file = TinyDB(file_to_delete)
    db_file.drop_table("_default")
    print("Suppression terminée")
    tournaments_controller()


def load_data():
    file_to_load = input("Entrez le chemin du fichier à charger: ")
    db_file = TinyDB(file_to_load)
    table = db_file.table("_default")
    for tournament in table:
        tournament_id = tournament["id"]
        name = tournament["Name"]
        place = tournament["Place"]
        date = tournament["Date"]
        time_control = tournament["TimeControl"]
        number_of_rounds = int(tournament["NumberOfRounds"])
        new_tournament = Tournament(tournament_id, name, place,
                                    date, time_control, number_of_rounds)
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
            new_player = Player(player_id, firstname, lastname,
                                date_of_birth, gender, rank)
            new_player.total_points = total_points
            new_tournament.add_players(new_player)
        for round in tournament["Rounds"]:
            name = round["Name"]
            new_round = Round(name)
            new_round.start_time = round["StartTime"]
            if round["EndTime"] == "None":
                new_round.end_time = None
            else:
                new_round.end_time = round["EndTime"]
            new_tournament.add_round(new_round)
            for match in round["Matches"]:
                player1 = match["Player1"]
                player2 = match["Player2"]
                contestants = []
                for player in new_tournament.players:
                    for other_player in new_tournament.players:
                        if (other_player != player
                                and str(player) == player1
                                and str(other_player) == player2):
                            contestants.append(player)
                            contestants.append(other_player)
                new_match = Match(contestants[0], contestants[1])
                new_match.scores = [float(match["ScorePlayer1"]),
                                    float(match["ScorePlayer2"])]
                in_progress_bool = None
                if match["InProgress"] == "True":
                    in_progress_bool = True
                elif match["InProgress"] == "False":
                    in_progress_bool = False
                new_match.in_progress = bool(in_progress_bool)
                new_match.result = (new_match.contestants, new_match.scores)
                new_round.add_match(new_match)
    print("Chargement terminé")
    tournaments_controller()
