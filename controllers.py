from datetime import datetime
from tinydb import TinyDB

from models import AllTournaments, Tournament, Player, Round, Match
from views import tournaments_view, selected_tournament_view, players_view, matches_view, rounds_view

all_tournaments = AllTournaments()
db = TinyDB("db.json")


def delete_data():
    file_to_delete = input("Entrez le chemin du fichier à supprimer: ")
    db_file = TinyDB(file_to_delete)
    db_file.drop_table("_default")
    print("Suppression terminée")
    tournaments_controller()


def load_data():
    global player_one, player_two
    file_to_load = input("Entrez le chemin du fichier à charger: ")
    db_file = TinyDB(file_to_load)
    table = db_file.table("_default")
    for tournament in table:
        tournament_id = tournament["id"]
        name = tournament["Name"]
        place = tournament["Place"]
        date = tournament["Date"]
        time_control = tournament["TimeControl"]
        # number_of_rounds = tournament["NumberOfRounds"]
        new_tournament = Tournament(tournament_id, name, place, date, time_control)
        # new_tournament.description = tournament["Description"]
        all_tournaments.add_tournament(new_tournament)
        for player in tournament["Players"]:
            firstname = player["Firstname"]
            lastname = player["Lastname"]
            date_of_birth = player["DateOfBirth"]
            gender = player["Gender"]
            rank = int(player["Rank"])
            total_points = float(player["TotalPoints"])
            new_player = Player(firstname, lastname, date_of_birth, gender, rank)
            new_player.total_points = total_points
            new_tournament.add_players(new_player)
        for round in tournament["Rounds"]:
            name = round["Name"]
            new_round = Round(name)
            new_tournament.add_round(new_round)
            for match in round["Matches"]:
                player1 = match["Player1"]
                player2 = match["Player2"]
                for player in new_tournament.players:
                    if str(player) == player1:
                        player_one = player
                    elif str(player) == player2:
                        player_two = player
                new_match = Match(player_one, player_two)
                new_match.contestants = [player_one, player_two]
                new_match.scores = [float(match["ScorePlayer1"]), float(match["ScorePlayer2"])]
                new_match.in_progress = match["InProgress"]
                new_match.result = (new_match.contestants, new_match.scores)
                new_round.add_match(new_match)
    print("Chargement terminé")
    tournaments_controller()


def save_data(tournaments):
    for tournament in tournaments:
        tournament.save()
    print("Enregistrement terminé.")
    tournaments_controller()


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


def tournaments_controller():
    tournaments_view()
    choice = input("Tapez 1, 2, 3, 4 ou 5: ")

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
        save_data(all_tournaments.tournaments)
    elif choice == 6:
        load_data()
    elif choice == 7:
        delete_data()
    elif choice == 8:
        print("Vous quittez le programme.")
        exit()
    else:
        print("Je n'ai pas compris votre choix.")
        tournaments_controller()
    print("-----------------")


def manage_tournament_controller():
    #     print la liste des tournois avec chacun un numéro
    if len(all_tournaments.tournaments) == 0:
        print("Il n'y a aucun tounoi en cours")
        tournaments_controller()
    else:
        print("Quel tournoi souhaitez-vous modifier ?")
        for i, tournament in enumerate(all_tournaments.tournaments):
            print(f"{i + 1}/ Le {tournament} ?")
        selected_tournament = input("Tapez le numéro du tournoi à modifier: ")
        if check_int_input(selected_tournament):
            selected_tournament = int(selected_tournament) - 1
        else:
            manage_tournament_controller()

        if selected_tournament < 0:
            print("Je n'ai pas compris votre choix.")
            print(f"Veuillez saisir un chiffre entre 1 et {len(all_tournaments.tournaments)}.")
            manage_tournament_controller()
        elif selected_tournament >= len(all_tournaments.tournaments):
            print("Je n'ai pas compris votre choix.")
            print(f"Veuillez saisir un chiffre entre 1 et {len(all_tournaments.tournaments)}.")
            manage_tournament_controller()

        selected_tournament_controller(all_tournaments.tournaments[selected_tournament])


def show_tournaments_controller():
    print(f"Il y a actuellement {len(all_tournaments.tournaments)} tournoi(s) enregistré(s).")
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
            print("Je n'ai pas compris votre choix. Veuillez taper un nombre entre 1 et 3.")
            time_control_selection()


def add_tournament_controller():
    print("****************************")
    print("Un nouveau tournoi va commencer aujourd'hui")
    # name = input("Entrez le nom du tournoi: ")
    # place = input("Entrez le lieu où se déroule le tournoi: ")

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
        date = f"Du {today.strftime('%d/%m/%Y')} au {end_date.strftime('%d/%m/%Y')}"

    # print(time_control_selection())
    time_control = time_control_selection()
    # number_of_rounds = int(input("Entrez le nombre de tours: "))
    # new_tournament = Tournament(name, place, date, time_control, number_of_rounds)

    new_tournament = Tournament(tournament_id, "name", "place", date, time_control, 4)
    # description = input("Entrez la description du tournoi: ")
    # new_tournament.description = description
    print(f"{date}")
    print("Tournoi bien créé")
    all_tournaments.add_tournament(new_tournament)
    print("*****************************")
    tournaments_controller()


def delete_tournament_controller():
    if len(all_tournaments.tournaments) == 0:
        print("Il n'y a aucun tounoi en cours")
        tournaments_controller()
    else:
        for i, tournament in enumerate(all_tournaments.tournaments):
            print(f"{i + 1}/ Supprimer {tournament.name} ?")
        choice = input("Tapez le numéro du tournoi à supprimer: ")

        if check_int_input(choice):
            choice = int(choice) - 1
        else:
            delete_tournament_controller()

        if choice > len(all_tournaments.tournaments):
            print("Je n'ai pas compris votre choix.")
            print(f"Veuillez saisir un chiffre compris entre 1 et {len(all_tournaments.tournaments)}")
            delete_tournament_controller()

        tournament_to_delete = all_tournaments.tournaments[choice]
        all_tournaments.delete_tournament(tournament_to_delete)
        print(
            f"Le tournoi {tournament_to_delete.name} a bien été supprimé."
        )
        tournaments_controller()


def selected_tournament_controller(tournament):
    selected_tournament_view()
    choice = input("Tapez 1, 2 ou 3: ")

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
        f"Nom: {tournament.name}, Lieu: {tournament.place}, Date(s): {tournament.date}, Contrôle du temps: {tournament.time_control}, Nombre de tours: {tournament.number_of_rounds}")
    print("Que souhaitez-vous modifier ?")
    print("1/ Le nom ?")
    print("2/ Le lieu ?")
    print("3/ Les dates ?")
    print("4/ Le contrôle du temps ?")
    print("5/ Le nombre de tours ?")
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
                date = f"Du {today.strftime('%d/%m/%Y')} au {end_date.strftime('%d/%m/%Y')}"
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
        selected_tournament_controller(tournament)
    else:
        print("Je n'ai pas compris votre choix.")
        edit_tournament_controller(tournament)


def players_controller(tournament):
    print("---Début player controller")
    players_view(tournament)
    choice = input("Tapez 1, 2, 3 ou 4: ")

    if check_int_input(choice):
        choice = int(choice)
    else:
        players_controller(tournament)

    if choice == 1:
        # il faut 8 joueurs
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
    firstname = input("Entrez le prénom du joueur: ")
    lastname = input("Entrez le nom de famille du joueur: ")
    date_of_birth = check_date_format(
        input("Entrez la date de naissance du joueur (format JJ/MM/AAAA): ")
    )
    if not date_of_birth:
        print("La date de naissance est invalide, veuillez taper une date au format JJ/MM/AAAA")
        add_player_controller(tournament)
    gender = input("Entrez le sexe du joueur: ")
    new_player = Player(firstname, lastname, date_of_birth, gender)
    tournament.players.append(new_player)
    # tournament.save(all_tournaments)
    print(f"Le joueur {firstname} {lastname} a bien été ajouté au tournoi.")
    players_controller(tournament)


def edit_player_controller(tournament):
    for i, player in enumerate(tournament.players):
        print(f"{i + 1}/ Modifier {player}")
    choice = input("Tapez le numéro du joueur à modifier: ")

    if check_int_input(choice):
        choice = int(choice) - 1
    else:
        edit_player_controller(tournament)

    if choice > len(tournament.players):
        print("Je n'ai pas compris votre choix.")
        print(f"Veuillez saisir un chiffre compris entre 1 et {len(tournament.players)}")
        edit_player_controller(tournament)

    player_to_modify = tournament.players[choice]
    print("Que souhaitez-vous modifier ?")
    print("1/ Son prénom ?")
    print("2/ Son nom de famille ?")
    print("3/ Sa date de naissance ?")
    print("4/ Son sexe ?")
    print("5/ Son score ?")
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
            print("La date de naissance est invalide, veuillez taper une date au format JJ/MM/AAAA")
            edit_player_controller(tournament)
        player_to_modify.date_of_birth = date_of_birth
    elif choice == 4:
        gender = input("Entrez le sexe du joueur: ")
        player_to_modify.gender = gender
    elif choice == 5:
        rank = int(input("Entrez le score du joueur: "))
        player_to_modify.rank = rank
    else:
        return
    print("La modification a été enregistrée.")
    players_controller(tournament)


def delete_player_controller(tournament):
    for i, player in enumerate(tournament.players):
        print(f"{i + 1}/ Supprimer {player} ?")
    choice = input("Tapez le numéro du joueur à supprimer: ")

    if check_int_input(choice):
        choice = int(choice) - 1
    else:
        delete_player_controller(tournament)

    if choice > len(tournament.players):
        print("Je n'ai pas compris votre choix.")
        print(f"Veuillez saisir un chiffre compris entre 1 et {len(tournament.players)}")
        delete_player_controller(tournament)

    player_to_delete = tournament.players[choice]
    tournament.delete_player(player_to_delete)
    print(
        f"Le joueur {player_to_delete.firstname} {player_to_delete.lastname} a bien été supprimé."
    )
    players_controller(tournament)


def rounds_controller(tournament):
    rounds_view(tournament)
    choice = int(input("Tapez le nombre souhaité: "))

    if choice == 1:
        add_round_controller(tournament)
    elif choice == 2:
        delete_round_controller(tournament)
    elif choice == 3:
        edit_round_controller(tournament)
    elif choice == 4:
        selected_tournament_controller(tournament)


def add_round_controller(tournament):
    if len(tournament.players) % 2 != 0:
        print("Vous ne pouvez pas commencer de parties tant que le nombre de joueurs est impair.")
        selected_tournament_controller(tournament)
    else:
        # if len(tournament.rounds) == len(tournament.players) - 1:
        if len(tournament.rounds) >= tournament.number_of_rounds:
            print(
                "Vous avez atteint la limite du nombre de tours, le tournoi est déjà terminé."
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
                    f"Le match joueur {player_one.firstname} contre joueur {player_two.firstname} a été ajouté au {new_round}"
                )
                i += 1

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
                        # - ce contestant potentiel n'a pas déjà un match dans ce round
                        # - le joueur n'a jamais joué avec lui
                        if (other_player != player
                                and other_player not in assigned_players
                                and other_player not in players_history[player.firstname]):
                            new_match = Match(player, other_player)
                            new_round.matches.append(new_match)
                            assigned_players.append(player)
                            assigned_players.append(other_player)
                            players_history[player.firstname].append(other_player)
                            players_history[other_player.firstname].append(player)
                            print(
                                f"Le match joueur {player.firstname} contre joueur {other_player.firstname} a été ajouté au {new_round}"
                            )
                            break

            print(players_history)
            print("Fin de la création des matchs")

            print(f"Le {new_round} a été créé.")
            print("------------------")
            rounds_controller(tournament)


def delete_round_controller(tournament):
    for i, round in enumerate(tournament.rounds):
        print(f"{i + 1}/ Supprimer {round}")
    choice = int(input("Tapez le numéro du tour à supprimer: ")) - 1
    round_to_delete = tournament.rounds[choice]
    tournament.delete_round(round_to_delete)
    print(f"Le {round_to_delete} a bien été supprimé.")
    print("-----------------------")
    rounds_controller(tournament)


def edit_round_controller(tournament):
    if not tournament.rounds:
        print("Il n'y a pas encore de tour créé dans ce tournoi.")
        rounds_controller(tournament)
    else:
        print("Quel tour souhaitez vous modifier ?")
        for i, round in enumerate(tournament.rounds):
            print(f"{i + 1}/ {round} ?")
        choice = input("Tapez le numéro du tour à sélectionner: ")
        if not check_int_input(choice):
            print("Je n'ai pas compris votre choix.")
            edit_round_controller(tournament)
        else:
            matches_controller(tournament.rounds[int(choice) - 1])
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
    print(
        f"1/ {match_selected.contestants[0].firstname} {match_selected.contestants[0].lastname} ?"
    )
    print(
        f"2/ {match_selected.contestants[1].firstname} {match_selected.contestants[1].lastname} ?"
    )
    print("3/ Il y a eu égalité.")
    winner = int(input("Tapez 1 ou 2 pour sélectionner le vainqueur: "))
    if winner == 1:
        match_selected.add_score_to_winner(match_selected.contestants[0])
        print(
            f"{match_selected.scores[0]} point ajouté au {match_selected.contestants[0]}"
        )
    elif winner == 2:
        match_selected.add_score_to_winner(match_selected.contestants[1])
        print(
            f"{match_selected.scores[1]} point ajouté au {match_selected.contestants[1]}"
        )
    elif winner == 3:
        match_selected.add_score_to_winner(None)
        print(f"{match_selected.scores[0]} point ajouté aux 2 joueurs")
    print("------------------------")


def ranking_controller(tournament):
    print(f"Il y a actuellement {len(tournament.rounds)} tour(s) dans le tournoi {tournament}")
    print(f"Voici le classement des joueurs pour ce tournoi:")
    if not tournament.players:
        print("Il n'y a pas de joueurs qui participent à ce tournoi.")
    else:
        tournament.order_players_by_points_and_ranks()
        for player in tournament.players:
            player.rank = tournament.players.index(player) + 1
        for i, player in enumerate(tournament.players):
            print(f"{i + 1}/ {player}")
    print("----------------------")


if __name__ == "__main__":
    # Tournoi1 = Tournament(1, "Premier", "Ici", "Du 23/08/2022 au 23/08/2022", "Blitz", 6)
    # Tournoi2 = Tournament(2, "Deuxième", "Là-bas", "Du 23/08/2022 au 23/08/2022", "Bullet", 4)
    # Joueur1 = Player("Mario", "Super", datetime.strptime("01/01/2000", "%d/%m/%Y"), "M")
    # Joueur2 = Player("Master", "Chief", datetime.strptime("02/02/2000", "%d/%m/%Y"), "M")
    # Joueur3 = Player("Samus", "Metroid", datetime.strptime("03/03/2000", "%d/%m/%Y"), "F")
    # Joueur4 = Player("Chun", "Li", datetime.strptime("04/04/2000", "%d/%m/%Y"), "F")
    # Joueur5 = Player("Bruce", "Wayne", datetime.strptime("05/05/2000", "%d/%m/%Y"), "M")
    # Joueur6 = Player("Coco", "Pops", datetime.strptime("06/06/2000", "%d/%m/%Y"), "M")
    # Joueur7 = Player("Pizza", "Saumon", datetime.strptime("07/07/2000", "%d/%m/%Y"), "F")
    # Joueur8 = Player("Bonbon", "Cicaplast", datetime.strptime("08/08/2000", "%d/%m/%Y"), "F")
    # Tournoi1.players.append(Joueur1)
    # Tournoi1.players.append(Joueur2)
    # Tournoi1.players.append(Joueur3)
    # Tournoi1.players.append(Joueur4)
    # Tournoi1.players.append(Joueur5)
    # Tournoi1.players.append(Joueur6)
    # Tournoi1.players.append(Joueur7)
    # Tournoi1.players.append(Joueur8)
    # Joueur9 = Player("Clavier", "Souris", datetime.strptime("09/09/2000", "%d/%m/%Y"), "M")
    # Joueur10 = Player("Casque", "Ecran", datetime.strptime("10/10/2000", "%d/%m/%Y"), "F")
    # Tournoi2.players.append(Joueur9)
    # Tournoi2.players.append(Joueur10)
    # all_tournaments.add_tournament(Tournoi1)
    # all_tournaments.add_tournament(Tournoi2)

    tournaments_controller()
