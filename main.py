from models import Tournament, Player, Round, Match


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
        rounds_controller(tournament)
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
        for round in tournament.rounds:
            print(round)
        if len(tournament.rounds) == len(tournament.players)-1:
            print("Vous avez atteint la limite du nombre de tours, le tournoi est déjà terminé.")
            main_controller(tournament)

        new_round_number = len(tournament.rounds) + 1
        new_round_name = f"Round {new_round_number}"
        new_round = Round(new_round_name)
        new_round.starting()
        tournament.add_round(new_round)

        players_history = {}
        for player in tournament.players:
            players_history[player.lastname] = []

        for round in tournament.rounds:
            for match in round.matches:
                player1 = match.contestants[0]
                player2 = match.contestants[1]
                players_history[player1.lastname].append(player2)
                players_history[player2.lastname].append(player1)


        assigned_players = []
        for player in tournament.players:
            # si on a déjà trouvé un match au joueur, on s'en occupe pas
            if player not in assigned_players:
                # on parcourt tous les joueurs pour trouver un contestant
                for other_player in tournament.players:
                    # un contestant est bon si
                    # - ce n'est pas le joueur lui même
                    # - ce contestant potentiel n'a pas déjà un match dans ce round
                    # - le joueur n'a jamais joué avec lui
                    if (other_player != player
                            and other_player not in assigned_players
                            and other_player not in players_history[player.lastname]):
                        new_match = Match(player, other_player)
                        new_round.matches.append(new_match)
                        assigned_players.append(player)
                        assigned_players.append(other_player)
                        break


        # ajouter les matchs en faisant les pairs de joueurs qui vont s'affronter:
        #     1/ au 1er tour, trier les joueurs selon leur rang
        tournament.order_players_by_rank()
        #     2/ diviser les joueurs en 2 partie, le meilleur de la 1ère partie affronte le 1er de la seconde moitié
        #     et ainsi de suite
        half = len(tournament.players)/2
        first_half = tournament.players[:half]
        second_half = tournament.players[half:]

        for player_one, player_two in first_half, second_half:
            new_match = Match(player_one, player_two)
            new_round.matches.append(new_match)

        #     3/ au prochain tour, trier les joueurs selon les points gagnés (et si égalité, de leur rang aussi)
        #     4/ ensuite, associer les joueurs 1 et 2, 3 et 4, etc.
        #     5/ répéter les étapes 3 et 4
            tournament.rounds.append(new_round)
            print("nouveau tour créé")
            rounds_controller(tournament)
    elif choice == 2:
        pass


def match_controller():
    pass
    # print(tout les matchs)
    # modifier le score du quel ?
    # quel est le score ?
    # pour le match choisi faire match.add_score_to_winner()


def ranking_view():
    pass


tournament = tournament_controller()
main_controller(tournament)
