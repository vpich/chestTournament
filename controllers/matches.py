from views import matches_view


# from controllers import rounds_controller


def matches_controller(tournament):
    matches_view(tournament)
    choice = int(input("Tapez 1 ou 2: "))
    if choice == 1:
        print("Quel match doit être modifié ?")
        for i, match in enumerate(tournament.rounds[-1].matches):
            print(f"{i + 1}/ Supprimer {match}")
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
