def rounds_view(tournament):
    print("Liste des tours du tournoi:")
    for round in tournament.rounds:
        print(round)
    print("------------------")
    print("1/ Commencer un nouveau tour ?")
    print("2/ Supprimer un tour ?")
    print("3/ Gérer un match dans un tour ?")
    print("4/ Retour en arrière")
