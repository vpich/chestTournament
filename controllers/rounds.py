# from controllers import matches_controller, selected_tournament_controller
from models import Round, Match
from views import rounds_view


def rounds_controller(tournament):
    rounds_view(tournament)
    choice = int(input("Tapez le nombre souhaité: "))

    if choice == 1:
        add_round_controller(tournament)
    elif choice == 2:
        delete_round_controller(tournament)
    elif choice == 3:
        matches_controller(tournament)
    elif choice == 4:
        selected_tournament_controller(tournament)


def add_round_controller(tournament):
    # Pas de début de tournoi si nombre pair a rajouter
    if len(tournament.rounds) == len(tournament.players) - 1:
        print(
            "Vous avez atteint la limite du nombre de tours, le tournoi est déjà terminé."
        )
        selected_tournament_controller(tournament)

    new_round_number = len(tournament.rounds) + 1
    new_round_name = f"Tour {new_round_number}"
    new_round = Round(new_round_name)
    new_round.starting()
    tournament.add_round(new_round)

    if len(tournament.rounds) == 1:
        # ajouter les matchs en faisant les pairs de joueurs qui vont s'affronter:
        #     1/ au 1er tour, trier les joueurs selon leur rang
        tournament.order_players_by_points_and_ranks()
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
