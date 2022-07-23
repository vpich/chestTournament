from models import Tournament, Player, Round


def tournament_controller():
    print("Un nouveau tournoi va commencer !")
    # name = input("Entrez le nom du tournoi: ")
    # place = input("Entrez le lieu où se déroule le tournoi: ")
    # date = input("Entrez la date du tournoi: ")
    # time_control = input("Entrez le type de contrôle de temps (bullet, blitz ou coup rapide): ")
    # number_of_rounds = int(input("Entrez le nombre de tours: "))
    # new_tournament = Tournament(name, place, date, time_control, number_of_rounds)
    new_tournament = Tournament("name", "place", "date", "time_control", 4)
    # description = input("Entrez la description du tournoi: ")
    # new_tournament.description = description
    print("Tournoi bien créé")
    return new_tournament


def main_view():
    print("Salut tu veux quoi ?")
    print("1/ Gérer les joueurs ?")
    print("2/ Gérer les rounds ?")
    print("3/ Afficher le classement des joueurs ?")


def main_controller(tournament):
    main_view()
    choice = int(input("Tapez 1, 2 ou 3: "))

    if choice == 1:
        players_controller(tournament)
    elif choice == 2:
        rounds_view(tournament)
    elif choice == 3:
        # affichage du classement
        pass
    else:
        return


def players_view(tournament):
    print("Liste des participants: ")
    for player in tournament.players:
        print(player)
    print("------------------")
    print("1/ Rajouter un joueur ?")
    print("2/ Modifier les informations d'un joueur ?")
    print("3/ Supprimer un joueur ?")
    print("4/ Retour en arrière")


def players_controller(tournament):
    print("---Début player controller")
    players_view(tournament)
    choice = int(input("Tapez 1, 2, 3 ou 4: "))

    if choice == 1:
        # il faut 8 joueurs
        add_player_view(tournament)
    elif choice == 2:
        modify_player_view(tournament)
    elif choice == 3:
        delete_player_view(tournament)
    elif choice == 4:
        main_controller(tournament)
    else:
        print("Je n'ai pas compris votre choix")
        players_controller(tournament)


def add_player_view(tournament):
    firstname = input("Entrez le prénom du joueur: ")
    lastname = input("Entrez le nom de famille du joueur: ")
    date_of_birth = input("Entrez la date de naissance du joueur: ")
    gender = input("Entrez le sexe du joueur: ")
    new_player = Player(firstname, lastname, date_of_birth, gender)
    tournament.players.append(new_player)
    print(f"Le joueur {firstname} {lastname} a bien été ajouté au tournoi.")
    players_controller(tournament)


def modify_player_view(tournament):
    for player, i in enumerate(tournament.players):
        print(f"{i}/ Supprimer joueur {player}")
    choice = int(input("Tapez le numéro du joueur à modifier: "))
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
    players_controller(tournament)


def delete_player_view(tournament):
    for player, i in enumerate(tournament.players):
        print(f"{i}/ Supprimer joueur {player}")
    choice = int(input("Tapez le numéro du joueur à supprimer: "))
    player_to_delete = tournament.players[choice]
    tournament.delete_player(player_to_delete)
    print("Le joueur a bien été supprimé")
    players_controller(tournament)


def rounds_view(tournament):
    print("Liste des rounds du tournoi:")
    for round in tournament.rounds:
        print(round)
    print("------------------")
    print("1/ Commencer un nouveau round ?")
    print("4/ Retour en arrière")


def rounds_controller(tournament):
    rounds_view(tournament)
    choice = int(input("Tapez 1 ou 2: "))

    if choice == 1:
        new_round = Round("round name") # nom temporaire
        # lister les rounds existants, si y'en a déjà trois print tournoi terminé
        # pour le joueur 1 tu regardes la liste des joueurs contre qui il a joué, prendre un des joueurs restants
        # exemple joueur 1 est avec 3, créer les deux matchs
        # envoyer vers match_controller

        # ajouter les matchs en faisant les pairs de joueurs qui vont s'affronter:
        #     1/ au 1er tour, trier les joueurs selon leur rang
        #     2/ diviser les joueurs en 2 partie, le meilleur de la 1ère partie affronte le 1er de la seconde moitié
        #     et ainsi de suite
        #     3/ au prochain tour, trier les joueurs selon les points gagnés (et si égalité, de leur rang aussi)
        #     4/ ensuite, associer les joueurs 1 et 2, 3 et 4, etc.
        #     5/ répéter les étapes 3 et 4
        tournament.rounds.append(new_round)
    elif choice == 2:
        pass

def match_controller():
    # print(tout les matchs)
    # modifier le score du quel ?
    # quel est le score ?
    # pour le match choisi faire match.add_score_to_winner()

def ranking_view():
    pass


tournament = tournament_controller()
main_controller(tournament)
