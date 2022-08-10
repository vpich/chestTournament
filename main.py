from datetime import datetime

from models import Tournament, Player, Round, Match

# -- à rajouter:
#     -- création et enregistrement de rapport
#     -- blocage d'ajout de round quand celui en cours n'est pas terminé
#     -- classement dans le bon ordre

all_tournaments = []


def tournaments_view():
    # afficher tous les tournois de manière bourrine
    print("Salut tu veux quoi ?")
    print("1/ Créer un nouveau tournoi ?")
    print("2/ Générer le rapport d'un tournoi existant ?")
    print("3/ Modifier un tournoi ?")


def tournaments_controller():
    tournaments_view()
    choice = int(input("Tapez 1 ou 2: "))

    if choice == 1:
        add_tournament_controller()
    elif choice == 2:
        show_tournaments_controller()
    elif choice == 3:
        edit_tournament_controller()
    else:
        print("Je n'ai pas compris votre choix.")
        tournaments_controller()
    print("-----------------")


def edit_tournament_controller():
    #     print la liste des tournois avec chacun un numéro
    #     lui demander un input pour en sélectionner un
    #     main_controller(selected_tournament)
    pass


def show_tournaments_controller():
    #     faire comme les joueurs: print la liste des tournois avec chacun un numéro et pour celui sélectionné print toutes les infos du tournoi
    pass


def add_tournament_controller():
    print("****************************")
    print("Un nouveau tournoi va commencer !")
    # name = input("Entrez le nom du tournoi: ")
    # place = input("Entrez le lieu où se déroule le tournoi: ")
    end_date = check_date_format(input("Entrez la date de fin de tournoi: "))
    # time_control = input("Entrez le type de contrôle de temps (bullet, blitz ou coup rapide): ")
    # number_of_rounds = int(input("Entrez le nombre de tours: "))
    # new_tournament = Tournament(name, place, date, time_control, number_of_rounds)
    today = datetime.date(datetime.now())
    if end_date < today:
        raise print("La date ne peut pas être antérieure à aujourd'hui.")
    else:
        date = f"Du {today.strftime('%d/%m/%Y')} au {end_date.strftime('%d/%m/%Y')}"
    new_tournament = Tournament("name", "place", date, "time_control", 4)
    # description = input("Entrez la description du tournoi: ")
    # new_tournament.description = description
    print(f"{date}")
    print("Tournoi bien créé")
    all_tournaments.append(new_tournament)
    print("*****************************")
    tournaments_controller()


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
        ranking_view(tournament)
    else:
        print("Je n'ai pas compris votre choix.")
        main_controller(tournament)
    print("-----------------")


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
        modify_player_controller(tournament)
    elif choice == 3:
        delete_player_controller(tournament)
    elif choice == 4:
        main_controller(tournament)
    else:
        print("Je n'ai pas compris votre choix")
        players_controller(tournament)


def check_date_format(user_input):
    try:
        date_to_check = datetime.strptime(user_input, "%d/%m/%Y")
        return datetime.date(date_to_check)
    except ValueError:
        raise ValueError("Format de date invalide.")


def add_player_view(tournament):
    firstname = input("Entrez le prénom du joueur: ")
    lastname = input("Entrez le nom de famille du joueur: ")
    date_of_birth = check_date_format(
        input("Entrez la date de naissance du joueur (format JJ/MM/AAAA): ")
    )
    gender = input("Entrez le sexe du joueur: ")
    new_player = Player(firstname, lastname, date_of_birth, gender)
    tournament.players.append(new_player)
    print(f"Le joueur {firstname} {lastname} a bien été ajouté au tournoi.")
    players_controller(tournament)


def modify_player_controller(tournament):
    for player, i in enumerate(tournament.players):
        print(f"{i}/ Modifier {player}")
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
        date_of_birth = check_date_format(
            input("Entrez la date de naissance du joueur: ")
        )
        player_to_modify.date_of_birth = date_of_birth
    elif choice == 4:
        gender = input("Entrez le sexe du joueur: ")
        player_to_modify.gender = gender
    elif choice == 5:
        rank = int(input("Entrez le score du joueur: "))
        player_to_modify.rank = rank
    else:
        return
    print("La modification a été enregistrée.")
    players_controller(tournament)


def delete_player_controller(tournament):
    for i, player in enumerate(tournament.players):
        print(f"{i + 1}/ Supprimer {player} ?")
    choice = int(input("Tapez le numéro du joueur à supprimer: ")) - 1
    player_to_delete = tournament.players[choice]
    tournament.delete_player(player_to_delete)
    print(
        f"Le joueur {player_to_delete.firstname} {player_to_delete.lastname} a bien été supprimé."
    )
    players_controller(tournament)


def rounds_view(tournament):
    print("Liste des tours du tournoi:")
    for round in tournament.rounds:
        print(round)
    print("------------------")
    print("1/ Commencer un nouveau tour ?")
    print("2/ Supprimer un tour ?")
    print("3/ Gérer un match du tour en cours ?")
    print("4/ Retour en arrière")


def rounds_controller(tournament):
    rounds_view(tournament)
    choice = int(input("Tapez le nombre souhaité: "))

    if choice == 1:
        add_round_controller(tournament)
    elif choice == 2:
        delete_round_controller(tournament)
    elif choice == 3:
        match_controller(tournament)
    elif choice == 4:
        main_controller(tournament)


# il faut qu'on puisse à un endroit afficher l'état total du tournoi, c'est à dire
# la liste des rounds déjà fait avec les scores de chaque match
# la liste des joueurs
# le nombre de rounds à venir


def add_round_controller(tournament):
    # Pas de début de tournoi si nombre pair a rajouter
    if len(tournament.rounds) == len(tournament.players) - 1:
        print(
            "Vous avez atteint la limite du nombre de tours, le tournoi est déjà terminé."
        )
        main_controller(tournament)

    new_round_number = len(tournament.rounds) + 1
    new_round_name = f"Tour {new_round_number}"
    new_round = Round(new_round_name)
    new_round.starting()
    tournament.add_round(new_round)

    if len(tournament.rounds) == 1:
        # ajouter les matchs en faisant les pairs de joueurs qui vont s'affronter:
        #     1/ au 1er tour, trier les joueurs selon leur rang
        tournament.order_players_by_rank()
        #     2/ diviser les joueurs en 2 partie, le meilleur de la 1ère partie affronte le 1er de la seconde moitié
        #     et ainsi de suite
        half = len(tournament.players) // 2
        first_half = tournament.players[:half]
        second_half = tournament.players[half:]

        i = 0
        for player_one in first_half:
            player_two = second_half[i]
            new_match = Match(player_one, player_two)
            new_round.matches.append(new_match)
            print(
                f"Le match joueur {player_one.firstname} contre joueur {player_two.firstname} a été ajouté au {new_round}"
            )
            i += 1

        print("Premier tour créé")
        rounds_controller(tournament)

    elif len(tournament.rounds) > 1:
        #     3/ au prochain tour, trier les joueurs selon les points gagnés (et si égalité, de leur rang aussi)
        previous_round = tournament.rounds[-1]
        for match in previous_round.matches:
            if match.scores[0] == 1:
                tournament.players.sort(key=match.contestants[1].__eq__)
            elif match.scores[0] == 0:
                tournament.players.sort(key=match.contestants[0].__eq__)
            elif match.scores[0] == 0.5:
                if match.contestants[0].rank > match.contestants[1].rank:
                    tournament.players.sort(key=match.contestants[1].__eq__)
                elif match.contestants[0].rank < match.contestants[1].rank:
                    tournament.players.sort(key=match.contestants[0].__eq__)
                elif match.contestants[0].rank == match.contestants[1].rank:
                    tournament.players.sort(key=match.contestants[1].__eq__)
                else:
                    # -- a modifier en mettant une vraie gestion d'erreur
                    print("Erreur")

        #     4/ ensuite, associer les joueurs 1 et 2, 3 et 4, etc.
        i = 0
        while i < len(tournament.players):
            player_one = tournament.players[i]
            player_two = tournament.players[i + 1]
            new_match = Match(player_one, player_two)
            new_round.matches.append(new_match)
            print(
                f"Le match joueur {player_one.firstname} contre joueur {player_two.firstname} a été ajouté au {new_round}"
            )
            i += 2
        print("Fin de la création des matchs")

        print(f"Le {new_round} a été créé.")
        print("------------------")
        rounds_controller(tournament)


def delete_round_controller(tournament):
    for i, round in enumerate(tournament.rounds):
        print(f"{i + 1}/ Supprimer {round}")
    choice = int(input("Tapez le numéro du tour à supprimer: ")) - 1
    round_to_delete = tournament.rounds[choice]
    tournament.delete_round(round_to_delete)
    print(f"Le {round_to_delete} a bien été supprimé.")
    print("-----------------------")
    rounds_controller(tournament)


def match_view(tournament):
    print("Liste des matchs de ce tour: ")
    for match in tournament.rounds[-1].matches:
        print(match)
    print("----------------------------------")
    print("Que souhaitez vous faire ?")
    print("1/ Mettre à jour les scores ?")
    print("2/ Retour en arrière")


def match_controller(tournament):
    match_view(tournament)
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


def ranking_view(tournament):
    # actuellement, cela classe par score total du plus petit au plus grand
    # il faudra inverser l'ordre pour pouvoir avoir le classement des joueurs
    tournament.order_players_by_rank()
    for i, player in enumerate(tournament.players):
        print(f"{i + 1}/ {player}")
    print("----------------------")
    main_controller(tournament)


tournaments_controller()
