from datetime import datetime
from tinydb import TinyDB

from models import AllTournaments, Tournament, Player, Round, Match
from views import (
    tournaments_view,
    selected_tournament_view,
    players_view,
    matches_view,
    rounds_view,
)

all_tournaments = AllTournaments()
db = TinyDB("db.json")


def save_data(tournaments):
    for tournament in tournaments:
        tournament.save()
    print("Enregistrement dans le fichier db.json terminé.")
    tournaments_controller()


def delete_data():
    # file_to_delete = input("Entrez le chemin du fichier à supprimer: ")
    if check_deletion():
        db_file = TinyDB("db.json")
        db_file.drop_table("_default")
        print("Suppression de tous les tournois du fichier db.json terminée")
        tournaments_controller()
    else:
        tournaments_controller()


def load_data():
    # file_to_load = input("Entrez le chemin du fichier à charger: ")
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
    print("Chargement du fichier db.json terminé.")
    # tournaments_controller()


def check_int_input(user_input):
    if user_input.isdigit():
        return True
    else:
        print("Je n'ai pas compris votre choix.")
        print("Veuillez saisir un chiffre pour sélectionner votre choix.")
        return False


def check_date_format(user_input):
    try:
        date_to_check = datetime.strptime(user_input, "%d/%m/%Y")
        return datetime.date(date_to_check)
    except ValueError:
        print("Format de date invalide.")
        return False


def check_deletion():
    print("Toute suppression est irrésersible.")
    choice = input("Souhaitez-vous vraiment effectuer la suppression ? (y/n)")
    if choice == "y":
        return True
    elif choice == "n":
        return False
    else:
        print("Je n'ai pas compris votre choix.")
        check_deletion()


def tournaments_controller():
    tournaments_view()
    choice = input("Tapez le nombre du choix à sélectionner: ")

    if check_int_input(choice):
        choice = int(choice)
    else:
        tournaments_controller()

    if choice == 1:
        add_tournament_controller()
    elif choice == 2:
        show_tournaments_controller()
    elif choice == 3:
        manage_tournament_controller()
    elif choice == 4:
        delete_tournament_controller()
    elif choice == 5:
        delete_data()
    elif choice == 6:
        print("Vous quittez le programme.")
        exit()
    elif choice == 7:
        save_data(all_tournaments.tournaments)
    elif choice == 8:
        load_data()
    else:
        print("Je n'ai pas compris votre choix.")
        tournaments_controller()
    print("-----------------")


def manage_tournament_controller():
    if not all_tournaments.tournaments:
        print("Il n'y a aucun tounoi en cours")
        tournaments_controller()
    else:
        print("Quel tournoi souhaitez-vous modifier ?")
        for i, tournament in enumerate(all_tournaments.tournaments):
            print(f"{i + 1}/ Le {tournament}")
        print(f"{len(all_tournaments.tournaments) + 1}/ Retour en arrière")
        selected_tournament = input("Tapez le numéro du tournoi à modifier: ")
        if check_int_input(selected_tournament):
            selected_tournament = int(selected_tournament) - 1
        else:
            manage_tournament_controller()

        if selected_tournament < 0:
            print("Je n'ai pas compris votre choix.")
            print(
                f"Veuillez saisir un chiffre "
                f"entre 1 et {len(all_tournaments.tournaments) + 1}."
            )
            manage_tournament_controller()
        elif selected_tournament == len(all_tournaments.tournaments):
            tournaments_controller()
        elif selected_tournament > len(all_tournaments.tournaments):
            print("Je n'ai pas compris votre choix.")
            print(
                f"Veuillez saisir un chiffre "
                f"entre 1 et {len(all_tournaments.tournaments) + 1}."
            )
            manage_tournament_controller()

        selected_tournament_controller(all_tournaments.tournaments[selected_tournament])


def show_tournaments_controller():
    print("---------------")
    print(
        f"Il y a actuellement "
        f"{len(all_tournaments.tournaments)} tournoi(s) enregistré(s)."
    )
    print("---------------")
    for tournament in all_tournaments.tournaments:
        ranking_controller(tournament)
    tournaments_controller()


def time_control_selection():
    time_control_choices = ["Bullet", "Blitz", "Coup rapide"]
    print("Quel type de contrôle de temps souhaitez-vous ?")
    for i, choice in enumerate(time_control_choices):
        print(f"{i + 1}/ {choice}")

    user_choice = input("Entrez le numéro du choix à selectionner: ")

    if not check_int_input(user_choice):
        time_control_selection()
    else:
        user_choice = int(user_choice)
        if user_choice > 3:
            print("Je n'ai pas compris votre choix.")
            time_control_selection()
        elif user_choice == 1:
            return time_control_choices[0]
        elif user_choice == 2:
            return time_control_choices[1]
        elif user_choice == 3:
            return time_control_choices[2]
        else:
            print(
                "Je n'ai pas compris votre choix. "
                "Veuillez taper un nombre entre 1 et 3."
            )
            time_control_selection()


def add_tournament_controller():
    print("****************************")
    print("Un nouveau tournoi va commencer aujourd'hui")
    name = input("Entrez le nom du tournoi: ")
    place = input("Entrez le lieu où se déroule le tournoi: ")

    if not all_tournaments.tournaments:
        tournament_id = 1
    else:
        tournament_id = len(all_tournaments.tournaments)

    end_date = check_date_format(input("Entrez la date de fin de tournoi: "))
    today = datetime.date(datetime.now())
    if not end_date:
        add_tournament_controller()
    if end_date < today:
        print("La date ne peut pas être antérieure à aujourd'hui.")
        add_tournament_controller()
    else:
        date = f"Du {today.strftime('%d/%m/%Y')} " f"au {end_date.strftime('%d/%m/%Y')}"

    time_control = time_control_selection()
    number_of_rounds = input("Entrez le nombre de tours: ")

    if number_of_rounds == "":
        number_of_rounds = 4
    elif number_of_rounds == "0":
        print("Le nombre de tour ne peut pas être nul.")
        add_tournament_controller()
    elif not check_int_input(number_of_rounds):
        add_tournament_controller()
    else:
        number_of_rounds = int(number_of_rounds)

    new_tournament = Tournament(
        tournament_id, name, place, date, time_control, number_of_rounds
    )
    description = input("Entrez la description du tournoi: ")
    new_tournament.description = description
    print(f"{date}")
    print("Tournoi bien créé")
    all_tournaments.add_tournament(new_tournament)
    # save_data(all_tournaments.tournaments)
    print("*****************************")
    tournaments_controller()


def delete_tournament_controller():
    if len(all_tournaments.tournaments) == 0:
        print("Il n'y a aucun tounoi en cours")
        tournaments_controller()
    else:
        for i, tournament in enumerate(all_tournaments.tournaments):
            print(f"{i + 1}/ Supprimer {tournament.name} ?")
        print(f"{len(all_tournaments.tournaments) + 1}/ Retour en arrière")
        choice = input("Tapez le numéro du tournoi à supprimer: ")

        if check_int_input(choice):
            choice = int(choice) - 1
        else:
            delete_tournament_controller()

        if choice > len(all_tournaments.tournaments):
            print("Je n'ai pas compris votre choix.")
            print(
                f"Veuillez saisir un chiffre compris "
                f"entre 1 et {len(all_tournaments.tournaments)}"
            )
            delete_tournament_controller()

        if choice == len(all_tournaments.tournaments):
            tournaments_controller()

        tournament_to_delete = all_tournaments.tournaments[choice]
        if check_deletion():
            all_tournaments.delete_tournament(tournament_to_delete)
            # save_data(all_tournaments.tournaments)
            print(f"Le tournoi {tournament_to_delete.name} a bien été supprimé.")
            tournaments_controller()
        else:
            tournaments_controller()


def selected_tournament_controller(tournament):
    selected_tournament_view()
    choice = input("Tapez le numéro du choix à sélectionner: ")

    if check_int_input(choice):
        choice = int(choice)
    else:
        selected_tournament_controller(tournament)

    if choice == 1:
        edit_tournament_controller(tournament)
    elif choice == 2:
        players_controller(tournament)
    elif choice == 3:
        rounds_controller(tournament)
    elif choice == 4:
        ranking_controller(tournament)
        selected_tournament_controller(tournament)
    elif choice == 5:
        tournaments_controller()
    else:
        print("Je n'ai pas compris votre choix.")
        selected_tournament_controller(tournament)
    print("-----------------")


def edit_tournament_controller(tournament):
    print(
        f"Nom: {tournament.name}, Lieu: {tournament.place}, "
        f"Date(s): {tournament.date}, "
        f"Contrôle du temps: {tournament.time_control}, "
        f"Nombre de tours: {tournament.number_of_rounds}"
    )
    print("Que souhaitez-vous modifier ?")
    print("1/ Le nom")
    print("2/ Le lieu")
    print("3/ Les dates")
    print("4/ Le contrôle du temps")
    print("5/ Le nombre de tours")
    print("6/ Retour en arrière")
    choice = input("Taper un chiffre entre 1 et 6: ")
    if check_int_input(choice):
        choice = int(choice)
        if choice == 1:
            name = input("Entrez le nom du tournoi: ")
            tournament.name = name
        elif choice == 2:
            place = input("Entrez le lieu: ")
            tournament.place = place
        elif choice == 3:
            end_date = check_date_format(input("Entrez la date de fin de tournoi: "))
            today = datetime.date(datetime.now())
            if not end_date:
                edit_tournament_controller(tournament)
            if end_date < today:
                print("La date ne peut pas être antérieure à aujourd'hui.")
                edit_tournament_controller(tournament)
            else:
                date = (
                    f"Du {today.strftime('%d/%m/%Y')} "
                    f"au {end_date.strftime('%d/%m/%Y')}"
                )
            tournament.date = date
        elif choice == 4:
            time_control = time_control_selection()
            tournament.time_control = time_control
        elif choice == 5:
            user_input = input("Entrez le nombre de tours: ")
            if check_int_input(user_input):
                number_of_rounds = int(user_input)
                tournament.number_of_rounds = number_of_rounds
            else:
                print("Saisie invalide. Veuillez rentrer un chiffre entier.")
                edit_tournament_controller(tournament)
        elif choice == 6:
            selected_tournament_controller(tournament)
        else:
            print("Je n'ai pas compris votre choix.")
            edit_tournament_controller(tournament)
        # save_data(all_tournaments.tournaments)
        selected_tournament_controller(tournament)


def players_controller(tournament):
    players_view(tournament)
    choice = input("Tapez le nombre du choix à sélectionner: ")

    if check_int_input(choice):
        choice = int(choice)
    else:
        players_controller(tournament)

    if choice == 1:
        add_player_controller(tournament)
    elif choice == 2:
        edit_player_controller(tournament)
    elif choice == 3:
        delete_player_controller(tournament)
    elif choice == 4:
        selected_tournament_controller(tournament)
    else:
        print("Je n'ai pas compris votre choix")
        players_controller(tournament)


def add_player_controller(tournament):
    if len(tournament.players) >= 8:
        print("Vous avez atteint le nombre maximal de 8 joueurs.")
        players_controller(tournament)
    else:
        if not tournament.players:
            player_id = 1
        else:
            player_id = len(tournament.players)
        firstname = input("Entrez le prénom du joueur: ")
        lastname = input("Entrez le nom de famille du joueur: ")
        date_of_birth = check_date_format(
            input("Entrez la date de naissance du joueur " "(format JJ/MM/AAAA): ")
        )
        if not date_of_birth:
            print(
                "La date de naissance est invalide, "
                "veuillez taper une date au format JJ/MM/AAAA"
            )
            add_player_controller(tournament)
        gender = input("Entrez le sexe du joueur: ")
        new_player = Player(player_id, firstname, lastname, date_of_birth, gender)
        tournament.players.append(new_player)
        # save_data(all_tournaments.tournaments)
        print(f"Le joueur {firstname} {lastname} " f"a bien été ajouté au tournoi.")
        players_controller(tournament)


def edit_player_controller(tournament):
    if not tournament.players:
        print("Il n'y a aucun joueur d'enregistrés.")
        players_controller(tournament)
    else:
        for i, player in enumerate(tournament.players):
            print(f"{i + 1}/ Modifier {player}")
        choice = input("Tapez le numéro du joueur à modifier: ")

        if check_int_input(choice):
            choice = int(choice) - 1
        else:
            edit_player_controller(tournament)

        if choice > len(tournament.players):
            print("Je n'ai pas compris votre choix.")
            print(
                f"Veuillez saisir un chiffre compris "
                f"entre 1 et {len(tournament.players)}"
            )
            edit_player_controller(tournament)

        player_to_modify = tournament.players[choice]
        print("Que souhaitez-vous modifier ?")
        print("1/ Son prénom")
        print("2/ Son nom de famille")
        print("3/ Sa date de naissance")
        print("4/ Son sexe")
        print("5/ Son score")
        print("6/ Retour en arrière")
        choice = int(input("Tapez le numéro à modifier: "))
        if choice == 1:
            firstname = input("Entrez le prénom du joueur: ")
            player_to_modify.firstname = firstname
        elif choice == 2:
            lastname = input("Entrez le nom de famille du joueur: ")
            player_to_modify.lastname = lastname
        elif choice == 3:
            date_of_birth = check_date_format(
                input("Entrez la date de naissance du joueur: ")
            )
            if not date_of_birth:
                print(
                    "La date de naissance est invalide, "
                    "veuillez taper une date au format JJ/MM/AAAA"
                )
                edit_player_controller(tournament)
            player_to_modify.date_of_birth = date_of_birth
        elif choice == 4:
            gender = input("Entrez le sexe du joueur: ")
            player_to_modify.gender = gender
        elif choice == 5:
            rank = input("Entrez le score du joueur: ")
            if check_int_input(rank):
                rank = int(rank)
            else:
                edit_player_controller(tournament)
            player_to_modify.rank = rank
        elif choice == 6:
            players_controller(tournament)
        else:
            print("Je n'ai pas compris votre choix.")
            edit_player_controller(tournament)
        # save_data(all_tournaments.tournaments)
        print("La modification a été enregistrée.")
        players_controller(tournament)


def delete_player_controller(tournament):
    if not tournament.players:
        print("Il n'y a aucun joueur d'enregistré.")
        players_controller(tournament)
    else:
        for i, player in enumerate(tournament.players):
            print(f"{i + 1}/ Supprimer {player} ?")
        print(f"{len(tournament.players) + 1}/ Retour en arrière")
        choice = input("Tapez le numéro du joueur à supprimer: ")

        if check_int_input(choice):
            choice = int(choice) - 1
        else:
            delete_player_controller(tournament)

        if choice == len(tournament.players):
            players_controller(tournament)

        if choice > len(tournament.players):
            print("Je n'ai pas compris votre choix.")
            print(
                f"Veuillez saisir un chiffre compris "
                f"entre 1 et {len(tournament.players)}"
            )
            delete_player_controller(tournament)

        player_to_delete = tournament.players[choice]
        if check_deletion():
            tournament.delete_player(player_to_delete)
            # save_data(all_tournaments.tournaments)
            print(f"Le {player_to_delete} a bien été supprimé.")
            players_controller(tournament)
        else:
            players_controller(tournament)


def rounds_controller(tournament):
    rounds_view(tournament)
    choice = input("Tapez le nombre du choix à sélectionner: ")

    if check_int_input(choice):
        choice = int(choice)
    else:
        rounds_controller(tournament)

    if choice == 1:
        add_round_controller(tournament)
    elif choice == 2:
        delete_round_controller(tournament)
    elif choice == 3:
        edit_round_controller(tournament)
    elif choice == 4:
        end_round_controller(tournament)
    elif choice == 5:
        selected_tournament_controller(tournament)


def end_round_controller(tournament):
    if not tournament.rounds:
        print("Il n'y a pas encore de tour créé dans ce tournoi.")
        rounds_controller(tournament)
    else:
        # for i, round in enumerate(tournament.rounds):
        #     print(f"{i + 1}/ Clôturer {round}")
        # choice = input("Tapez le numéro du tour à clôturer: ")
        # if not check_int_input(choice):
        #     rounds_controller(tournament)
        # round_chosen = int(choice) - 1
        # round_to_end = tournament.rounds[round_chosen]
        round_to_end = tournament.rounds[-1]
        # last_round = tournament.rounds[round_chosen]
        for match in round_to_end.matches:
            if match.in_progress:
                print(
                    "Vous ne pouvez pas clôturer ce tour, "
                    "tant que les matchs ne sont pas terminés"
                )
                rounds_controller(tournament)
        round_to_end.ending()
        print(f"Le {round_to_end} a bien été clôturé.")
        # save_data(all_tournaments.tournaments)
        rounds_controller(tournament)


def add_round_controller(tournament):
    if tournament.rounds:
        last_round = tournament.rounds[-1]
        if not last_round.end_time:
            print(
                "Vous ne pouvez pas créé de nouveau tour, "
                "tant que le tour précédent n'est pas clôturé"
            )
            rounds_controller(tournament)
    if len(tournament.players) != 8:
        print(
            "Vous ne pouvez pas commencer de parties "
            "tant que le nombre de joueurs est inférieur à 8."
        )
        rounds_controller(tournament)
    else:
        if len(tournament.rounds) >= tournament.number_of_rounds:
            print(
                "Vous avez atteint la limite du nombre de tours, "
                "le tournoi est déjà terminé."
            )
            selected_tournament_controller(tournament)

        new_round_number = len(tournament.rounds) + 1
        new_round_name = f"Tour {new_round_number}"
        new_round = Round(new_round_name)
        new_round.starting()
        tournament.add_round(new_round)

        if len(tournament.rounds) == 1:
            tournament.order_players_by_points_and_ranks()
            half = len(tournament.players) // 2
            first_half = tournament.players[:half]
            second_half = tournament.players[half:]

            i = 0
            for player_one in first_half:
                player_two = second_half[i]
                new_match = Match(player_one, player_two)
                new_round.matches.append(new_match)
                print(
                    f"Le match joueur {player_one.firstname} "
                    f"contre joueur {player_two.firstname} "
                    f"a été ajouté au {new_round}"
                )
                i += 1

            # save_data(all_tournaments.tournaments)
            print("Premier tour créé")
            rounds_controller(tournament)

        elif len(tournament.rounds) > 1:
            players_history = tournament.get_players_history()
            tournament.order_players_by_points_and_ranks()

            assigned_players = []
            for player in tournament.players:
                # si on a déjà trouvé un match au joueur, on s'en occupe pas
                if player not in assigned_players:
                    # on parcourt tous les joueurs pour trouver un contestant
                    for other_player in tournament.players:
                        # un contestant est bon si
                        # - ce n'est pas le joueur lui même
                        # - ce contestant potentiel n'a pas déjà un match
                        # dans ce round
                        # - le joueur n'a jamais joué avec lui
                        if (
                                other_player != player
                                and other_player not in assigned_players
                                and other_player not in players_history[player.player_id]
                        ):
                            new_match = Match(player, other_player)
                            new_round.matches.append(new_match)
                            assigned_players.append(player)
                            assigned_players.append(other_player)
                            players_history[player.player_id].append(other_player)
                            players_history[other_player.player_id].append(player)
                            print(
                                f"Le match joueur {player.firstname} "
                                f"contre joueur {other_player.firstname} "
                                f"a été ajouté au {new_round}"
                            )
                            break

            # save_data(all_tournaments.tournaments)
            print("Fin de la création des matchs")

            print(f"Le {new_round} a été créé.")
            rounds_controller(tournament)


def delete_round_controller(tournament):
    if not tournament.rounds:
        print("Il n'y a pas encore de tour créé dans ce tournoi.")
        rounds_controller(tournament)
    else:
        for i, round in enumerate(tournament.rounds):
            print(f"{i + 1}/ Supprimer {round}")
        print(f"{len(tournament.rounds) + 1}/ Retour en arrière")
        choice = input("Tapez le numéro du tour à supprimer: ")
        if not check_int_input(choice):
            delete_round_controller(tournament)
        else:
            choice = int(choice) - 1
            if choice == len(tournament.rounds):
                rounds_controller(tournament)
            elif choice > len(tournament.rounds):
                print("Je n'ai pas compris votre choix.")
                delete_round_controller(tournament)
            if check_deletion():
                round_to_delete = tournament.rounds[choice]
                tournament.delete_round(round_to_delete)
                # save_data(all_tournaments.tournaments)
                print(f"Le {round_to_delete} a bien été supprimé.")
                print("-----------------------")
                rounds_controller(tournament)
            else:
                rounds_controller(tournament)


def edit_round_controller(tournament):
    if not tournament.rounds:
        print("Il n'y a pas encore de tour créé dans ce tournoi.")
        rounds_controller(tournament)
    else:
        # print("Quel tour souhaitez vous modifier ?")
        # for i, round in enumerate(tournament.rounds):
        #     print(f"{i + 1}/ {round} ?")
        # choice = input("Tapez le numéro du tour à sélectionner: ")
        # if not check_int_input(choice):
        #     print("Je n'ai pas compris votre choix.")
        #     edit_round_controller(tournament)
        # else:
        matches_controller(tournament.rounds[-1])
        # save_data(all_tournaments.tournaments)
        rounds_controller(tournament)


def matches_controller(round):
    matches_view(round)
    match_selected = input("Tapez le numéro du match à mettre à jour: ")
    if not check_int_input(match_selected):
        print("Je n'ai pas compris votre choix.")
        matches_controller(round)
    else:
        match_selected = int(match_selected) - 1
        if match_selected < len(round.matches):
            update_winner(round.matches[match_selected])
        else:
            print("Je n'ai pas compris votre choix.")
            matches_controller(round)


def update_winner(match_selected):
    print("Qui a gagné ?")
    print(f"1/ {match_selected.contestants[0]}")
    print(f"2/ {match_selected.contestants[1]}")
    print("3/ Il y a eu égalité.")
    print("4/ Retour en arrière")
    winner = input("Tapez le nombre du choix à sélectionner: ")
    if not check_int_input(winner):
        print("Je n'ai pas comprix votre choix.")
        update_winner(match_selected)
    else:
        winner = int(winner)
        if winner == 1:
            match_selected.add_score_to_winner(match_selected.contestants[0])
            print(
                f"{match_selected.scores[0]} point ajouté "
                f"au {match_selected.contestants[0]}"
            )
        elif winner == 2:
            match_selected.add_score_to_winner(match_selected.contestants[1])
            print(
                f"{match_selected.scores[1]} point ajouté "
                f"au {match_selected.contestants[1]}"
            )
        elif winner == 3:
            match_selected.add_score_to_winner(None)
            print(f"{match_selected.scores[0]} point ajouté aux 2 joueurs")
        elif winner == 4:
            pass
        else:
            print("Je n'ai pas compris votre choix.")
            update_winner(match_selected)


def ranking_controller(tournament):
    print(f"Le tournoi {tournament.name} se situant {tournament.place} "
          f"se déroule {tournament.date.lower()}.")
    print(f"Le contrôle du temps est le {tournament.time_control}, "
          f"et il doit comporter {tournament.number_of_rounds} tours.")
    print(
        f"Il y a actuellement {len(tournament.rounds)} tour(s) "
        f"dans le tournoi {tournament}."
    )
    print("Voici le classement des joueurs pour ce tournoi:")
    if not tournament.players:
        print("Il n'y a pas de joueurs qui participent à ce tournoi.")
    else:
        tournament.order_players_by_points_and_ranks()
        for player in tournament.players:
            player.rank = tournament.players.index(player) + 1
        for i, player in enumerate(tournament.players):
            print(f"{i + 1}/ {player}, points gagnés: {player.total_points}")
    print("----------------------")


if __name__ == "__main__":
    # Tournoi1 = Tournament(1, "Premier", "Ici", "Du 23/08/2022 au 23/08/2022", "Blitz", 6)
    # Tournoi2 = Tournament(2, "Deuxième", "Là-bas", "Du 23/08/2022 au 23/08/2022", "Bullet", 4)
    # Joueur1 = Player(1, "Mario", "Super", datetime.strptime("01/01/2000", "%d/%m/%Y"), "M")
    # Joueur2 = Player(2, "Master", "Chief", datetime.strptime("02/02/2000", "%d/%m/%Y"), "M")
    # Joueur3 = Player(3, "Samus", "Metroid", datetime.strptime("03/03/2000", "%d/%m/%Y"), "F")
    # Joueur4 = Player(4, "Chun", "Li", datetime.strptime("04/04/2000", "%d/%m/%Y"), "F")
    # Joueur5 = Player(5, "Bruce", "Wayne", datetime.strptime("05/05/2000", "%d/%m/%Y"), "M")
    # Joueur6 = Player(6, "Coco", "Pops", datetime.strptime("06/06/2000", "%d/%m/%Y"), "M")
    # Joueur7 = Player(7, "Pizza", "Saumon", datetime.strptime("07/07/2000", "%d/%m/%Y"), "F")
    # Joueur8 = Player(8, "Bonbon", "Cicaplast", datetime.strptime("08/08/2000", "%d/%m/%Y"), "F")
    # Tournoi1.players.append(Joueur1)
    # Tournoi1.players.append(Joueur2)
    # Tournoi1.players.append(Joueur3)
    # Tournoi1.players.append(Joueur4)
    # Tournoi1.players.append(Joueur5)
    # Tournoi1.players.append(Joueur6)
    # Tournoi1.players.append(Joueur7)
    # Tournoi1.players.append(Joueur8)
    # Joueur9 = Player(9, "Clavier", "Souris", datetime.strptime("09/09/2000", "%d/%m/%Y"), "M")
    # Joueur10 = Player(10, "Casque", "Ecran", datetime.strptime("10/10/2000", "%d/%m/%Y"), "F")
    # Tournoi2.players.append(Joueur9)
    # Tournoi2.players.append(Joueur10)
    # all_tournaments.add_tournament(Tournoi1)
    # all_tournaments.add_tournament(Tournoi2)

    tournaments_controller()
