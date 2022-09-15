def players_view(tournament):
    print("--------------")
    print(f"Liste des {len(tournament.players)} participants du tournoi {tournament}: ")
    for player in tournament.players:
        print(player)
    print("--------------")
    print("Que souhaitez-vous faire ?")
    print("--------------")
    print("1/ Rajouter un joueur")
    print("2/ Modifier les informations d'un joueur")
    print("3/ Supprimer un joueur")
    print("4/ Afficher le classement des joueurs")
    print("5/ Afficher les joueurs triés par noms de famille")
    print("6/ Retour en arrière")
