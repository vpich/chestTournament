from models import Tournament, Player, Round

# def tournament_view():
tournament = Tournament()


def players_view():
    print("Liste des participants: ")
    for player in tournament.players:
        print(player)
    print("------------------")
    print("1/ Rajouter un joueur ?")
    print("2/ Modifier les informations d'un joueur ?")
    print("3/ Supprimer un joueur ?")
    print("4/ Retour en arrière")


def players_controller():
    players_view()
    choice = input("Tapez 1, 2, 3 ou 4: ")

    if choice == 1:
        add_player_view()
    elif choice == 2:
        modify_player_view()
    elif choice == 3:
        delete_player_view()
    elif choice == 4:
        main_controller()
    else:
        return


def add_player_view():
    firstname = input("Entrez le prénom du joueur: ")
    lastname = input("Entrez le nom de famille du joueur: ")
    date_of_birth = input("Entrez la date de naissance du joueur: ")
    gender = input("Entrez le sexe du joueur: ")
    new_player = Player(firstname, lastname, date_of_birth, gender)
    tournament.players.append(new_player)
    print(f"Le joueur {firstname} {lastname} a bien été ajouté au tournoi.")
    main_controller()


def modify_player_view():
    for player, i in enumerate(tournament.players):
        print(f"{i}/ Supprimer joueur {player}")
    choice = input("Tapez le numéro du joueur à modifier: ")
    player_to_modify = tournament.players[choice]
    print("Que souhaitez-vous modifier ?")
    print("1/ Son prénom ?")
    print("2/ Son nom de famille ?")
    print("3/ Sa date de naissance ?")
    print("4/ Son sexe ?")
    print("5/ Son score ?")
    choice = input("Tapez le numéro à modifier: ")
    if choice == 1:
        firstname = input("Entrez le prénom du joueur: ")
        player_to_modify.firstname = firstname
    elif choice == 2:
        lastname = input("Entrez le nom de famille du joueur: ")
        player_to_modify.lastname = lastname
    elif choice == 3:
        date_of_birth = input("Entrez la date de naissance du joueur: ")
        player_to_modify.date_of_birth = date_of_birth
    elif choice == 4:
        gender = input("Entrez le sexe du joueur: ")
        player_to_modify.gender = gender
    elif choice == 5:
        rank = input("Entrez le score du joueur: ")
        player_to_modify.rank = rank
    else:
        return
    print("La modification a été enregistrée.")
    main_controller()


def delete_player_view():
    for player, i in enumerate(tournament.players):
        print(f"{i}/ Supprimer joueur {player}")
    choice = input("Tapez le numéro du joueur à supprimer: ")
    player_to_delete = tournament.players[choice]
    tournament.delete_player(player_to_delete)
    main_controller()


def main_view():
    print("Salut tu veux quoi ?")
    print("1/ Gérer les joueurs ?")
    print("2/ Gérer les rounds ?")
    print("3/ Afficher le classement des joueurs ?")


def main_controller():
    main_view()
    choice = input("Tapez 1, 2 ou 3: ")

    if choice == 1:
        players_controller()
    elif choice == 2:
        rounds_view()
    elif choice == 3:
        # affichage du classement
        pass
    else:
        return


def rounds_view():
    print("Liste des rounds du tournoi:")
    for round in tournament.rounds:
        print(round)
    print("------------------")
    print("1/ Ajouter un round ?")
    print("2/ Commencer un round ?")
    print("3/ Terminer un round ?")
    print("4/ Retour en arrière")


def rounds_controller():
    rounds_view()
    choice = input("Tapez 1 ou 2: ")

    if choice == 1:
        new_round = Round("round name") # nom temporaire
        tournament.rounds.append(new_round)
    elif choice == 2:
        pass


main_controller()
