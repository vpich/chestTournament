from views import players_view
from models import Player
from .checks import (
    check_int_input,
    check_date_format, check_deletion)
from .ranking import ranking_controller, filter_players_by_name
from . import selected_tournament


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
        ranking_controller(tournament)
        players_controller(tournament)
    elif choice == 5:
        filter_players_by_name(tournament)
        players_controller(tournament)
    elif choice == 6:
        selected_tournament.selected_tournament_controller(tournament)
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
        print("--------------")
        print("Il n'y a aucun joueur d'enregistrés.")
        print("--------------")
        players_controller(tournament)
    else:
        print("--------------")
        print("Pour quel joueur souhaitez-vous modifier les informations ?")
        print("--------------")
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
        print("--------------")
        print(f"Vous allez éditer les informations de {player_to_modify}")
        print("Que souhaitez-vous modifier ?")
        print("--------------")
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
        print("--------------")
        print("Il n'y a aucun joueur d'enregistré.")
        print("--------------")
        players_controller(tournament)
    else:
        print("--------------")
        print("Quel joueur souhaitez-vous supprimer du tournoi ?")
        print("--------------")
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
