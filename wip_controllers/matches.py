from views import matches_view


# from controllers import rounds_controller


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
        f"1/ {match_selected.contestants[0]} ?"
    )
    print(
        f"2/ {match_selected.contestants[1]} ?"
    )
    print("3/ Il y a eu égalité.")
    winner = int(input("Tapez 1 ou 2 pour sélectionner le vainqueur: "))
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
        print(f"{match_selected.scores[0]} point ajouté "
              f"aux 2 joueurs")
    print("------------------------")
