from datetime import datetime

from models import AllTournaments, Tournament, Player, Round, Match
from views import tournaments_view, selected_tournament_view, players_view, matches_view, rounds_view

all_tournaments = AllTournaments()


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
        raise ValueError("Format de date invalide.")


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
        edit_tournament_controller()
    elif choice == 4:
        delete_tournament_controller()
    elif choice == 5:
        print("Vous quittez le programme.")
        exit()
    else:
        print("Je n'ai pas compris votre choix.")
        tournaments_controller()
    print("-----------------")


def edit_tournament_controller():
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
            edit_tournament_controller()

        if selected_tournament < 0:
            print("Je n'ai pas compris votre choix.")
            print(f"Veuillez saisir un chiffre entre 1 et {len(all_tournaments.tournaments)}.")
            edit_tournament_controller()
        elif selected_tournament >= len(all_tournaments.tournaments):
            print("Je n'ai pas compris votre choix.")
            print(f"Veuillez saisir un chiffre entre 1 et {len(all_tournaments.tournaments)}.")
            edit_tournament_controller()

        selected_tournament_controller(all_tournaments.tournaments[selected_tournament])


def show_tournaments_controller():
    #     faire comme les joueurs: print la liste des tournois
    #     avec chacun un numéro et pour celui sélectionné print toutes les infos du tournoi
    print(f"Il y a actuellement {len(all_tournaments.tournaments)} tournoi(s) enregistré(s).")
    for tournament in all_tournaments.tournaments:
        ranking_controller(tournament)
    # print("Pour quel tournoi souhaitez-vous éditer un rapport ?")
    # for i, tournament in enumerate(all_tournaments.tournaments):
    #     print(f"{i + 1}/ Le {tournament} ?")
    # selected_tournament = int(input("Tapez le numéro du tournoi choisi: ")) - 1
    # print(f"Vous avez choisi le tournoi {all_tournaments.tournaments[selected_tournament].name}")
    # ranking_view(all_tournaments.tournaments[selected_tournament])
    tournaments_controller()


def add_tournament_controller():
    print("****************************")
    print("Un nouveau tournoi va commencer !")
    # name = input("Entrez le nom du tournoi: ")
    # place = input("Entrez le lieu où se déroule le tournoi: ")
    end_date = check_date_format(input("Entrez la date de fin de tournoi: "))
    # time_control = input("Entrez le type de contrôle de temps (bullet, blitz ou coup rapide): ")
    # number_of_rounds = int(input("Entrez le nombre de tours: "))
    # new_tournament = Tournament(name, place, date, time_control, number_of_rounds)
    today = datetime.date(datetime.now())
    if end_date < today:
        raise print("La date ne peut pas être antérieure à aujourd'hui.")
    else:
        date = f"Du {today.strftime('%d/%m/%Y')} au {end_date.strftime('%d/%m/%Y')}"
    new_tournament = Tournament("name", "place", date, "time_control", 4)
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
        players_controller(tournament)
    elif choice == 2:
        rounds_controller(tournament)
    elif choice == 3:
        ranking_controller(tournament)
        selected_tournament_controller(tournament)
    elif choice == 4:
        tournaments_controller()
    else:
        print("Je n'ai pas compris votre choix.")
        selected_tournament_controller(tournament)
    print("-----------------")


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
    gender = input("Entrez le sexe du joueur: ")
    new_player = Player(firstname, lastname, date_of_birth, gender)
    tournament.players.append(new_player)
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
        matches_controller(tournament)
    elif choice == 4:
        selected_tournament_controller(tournament)


def add_round_controller(tournament):
    # Pas de début de tournoi si nombre pair a rajouter
    if len(tournament.rounds) == len(tournament.players) - 1:
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
        # ajouter les matchs en faisant les pairs de joueurs qui vont s'affronter:
        #     1/ au 1er tour, trier les joueurs selon leur rang
        tournament.order_players_by_points_and_ranks()
        #     2/ diviser les joueurs en 2 partie, le meilleur de la 1ère partie affronte le 1er de la seconde moitié
        #     et ainsi de suite
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
        #     3/ au prochain tour, trier les joueurs selon les points gagnés (et si égalité, de leur rang aussi)
        previous_round = tournament.rounds[-1]
        for match in previous_round.matches:
            if match.scores[0] == 1:
                tournament.players.sort(key=match.contestants[1].__eq__)
            elif match.scores[0] == 0:
                tournament.players.sort(key=match.contestants[0].__eq__)
            elif match.scores[0] == 0.5:
                if match.contestants[0].rank > match.contestants[1].rank:
                    tournament.players.sort(key=match.contestants[1].__eq__)
                elif match.contestants[0].rank < match.contestants[1].rank:
                    tournament.players.sort(key=match.contestants[0].__eq__)
                elif match.contestants[0].rank == match.contestants[1].rank:
                    tournament.players.sort(key=match.contestants[1].__eq__)
                else:
                    # -- a modifier en mettant une vraie gestion d'erreur
                    print("Erreur")

        #     4/ ensuite, associer les joueurs 1 et 2, 3 et 4, etc.
        i = 0
        while i < len(tournament.players):
            player_one = tournament.players[i]
            player_two = tournament.players[i + 1]
            new_match = Match(player_one, player_two)
            new_round.matches.append(new_match)
            print(
                f"Le match joueur {player_one.firstname} contre joueur {player_two.firstname} a été ajouté au {new_round}"
            )
            i += 2
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


def matches_controller(tournament):
    matches_view(tournament)
    choice = int(input("Tapez 1 ou 2: "))
    if choice == 1:
        print("Quel match doit être modifié ?")
        for i, match in enumerate(tournament.rounds[-1].matches):
            print(f"{i + 1}/ {match}")
        match_selected = int(input(f"Tapez le numéro du match à mettre à jour: ")) - 1
        update_winner(tournament.rounds[-1].matches[match_selected])
        rounds_controller(tournament)
    elif choice == 2:
        rounds_controller(tournament)


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


tournaments_controller()
