def rounds_view(tournament):
    print("--------------")
    print("Liste des tours du tournoi:")
    for round in tournament.rounds:
        print(round)
    print("--------------")
    print("Que souhaitez_vous faire ?")
    print("--------------")
    print("1/ Commencer un nouveau tour")
    print("2/ Supprimer un tour")
    print("3/ Gérer un match dans le tour actuel")
    print("4/ Clôturer le tour actuel")
    print("5/ Retour en arrière")
