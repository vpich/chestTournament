def matches_view(tournament):
    print("Liste des matchs de ce tour: ")
    for match in tournament.rounds[-1].matches:
        print(match)
    print("----------------------------------")
    print("Que souhaitez vous faire ?")
    print("1/ Mettre à jour les scores ?")
    print("2/ Retour en arrière")
