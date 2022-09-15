from views import matches_view
from .checks import check_int_input
from .rand_black_or_white import random_black_or_white


def matches_controller(tournament_round):
    matches_view(tournament_round)
    match_selected = input("Tapez le numéro du match à mettre à gérer: ")
    print("--------------")
    if not check_int_input(match_selected):
        print("Je n'ai pas compris votre choix.")
        matches_controller(tournament_round)
    else:
        match_selected = int(match_selected) - 1
        if match_selected < len(tournament_round.matches):
            match_selected_controller(tournament_round.matches[match_selected])
        else:
            print("Je n'ai pas compris votre choix.")
            matches_controller(tournament_round)


def match_selected_controller(match_selected):
    print("Que souhaitez-vous faire ?")
    print("--------------")
    print(f"1/ Lancer un choix aléatoire pour définir "
          f"la couleur à jouer pour le joueur {match_selected.contestants[0]}")
    print("2/ Mettre à jour le vainqueur de cette partie")
    print("3/ Retour en arrière")
    print("--------------")
    choice = input("Tapez le numéro souhaité pour sélectionner votre choix: ")
    print("--------------")
    if not check_int_input(choice):
        match_selected_controller(match_selected)
    else:
        choice = int(choice)
        if choice == 1:
            random_black_or_white(match_selected.contestants[0])
        elif choice == 2:
            update_winner(match_selected)
        elif choice == 3:
            pass
        else:
            print("Je n'ai pas compris votre choix")
            match_selected_controller(match_selected)


def update_winner(match_selected):
    print("Quel joueur a gagné ?")
    print("--------------")
    print(f"1/ Le joueur {match_selected.contestants[0]}")
    print(f"2/ Le joueur {match_selected.contestants[1]}")
    print("3/ Il y a eu égalité.")
    print("4/ Retour en arrière")
    print("--------------")
    winner = input("Tapez le nombre du choix à sélectionner: ")
    print("--------------")
    if not check_int_input(winner):
        print("Je n'ai pas comprix votre choix.")
        update_winner(match_selected)
    else:
        winner = int(winner)
        if winner == 1:
            match_selected.add_score_to_winner(match_selected.contestants[0])
            print(
                f"{match_selected.scores[0]} point ajouté "
                f"au joueur {match_selected.contestants[0]}"
            )
        elif winner == 2:
            match_selected.add_score_to_winner(match_selected.contestants[1])
            print(
                f"{match_selected.scores[1]} point ajouté "
                f"au joueur {match_selected.contestants[1]}"
            )
        elif winner == 3:
            match_selected.add_score_to_winner(None)
            print(f"{match_selected.scores[0]} point ajouté aux 2 joueurs")
        elif winner == 4:
            pass
        else:
            print("Je n'ai pas compris votre choix.")
            update_winner(match_selected)
