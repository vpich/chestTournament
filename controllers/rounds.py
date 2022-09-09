from models import Round, Match
from views import rounds_view
from .checks import check_int_input, check_deletion
from . import selected_tournament
from .matches import matches_controller


def rounds_controller(tournament):
    rounds_view(tournament)
    print("--------------")
    choice = input("Tapez le nombre du choix à sélectionner: ")
    print("--------------")

    if check_int_input(choice):
        choice = int(choice)
    else:
        rounds_controller(tournament)

    if choice == 1:
        add_round_controller(tournament)
    elif choice == 2:
        delete_round_controller(tournament)
    elif choice == 3:
        edit_round_controller(tournament)
    elif choice == 4:
        end_round_controller(tournament)
    elif choice == 5:
        selected_tournament.selected_tournament_controller(tournament)


def end_round_controller(tournament):
    if not tournament.rounds:
        print("--------------")
        print("Il n'y a pas encore de tour créé dans ce tournoi.")
        print("--------------")
        rounds_controller(tournament)
    else:
        round_to_end = tournament.rounds[-1]
        for match in round_to_end.matches:
            if match.in_progress:
                print(
                    "Vous ne pouvez pas clôturer ce tour, "
                    "tant que les matchs ne sont pas terminés"
                )
                rounds_controller(tournament)
        round_to_end.ending()
        print(f"Le {round_to_end} a bien été clôturé.")
        # save_data(all_tournaments.tournaments)
        rounds_controller(tournament)


def add_round_controller(tournament):
    if tournament.rounds:
        last_round = tournament.rounds[-1]
        if not last_round.end_time:
            print("--------------")
            print(
                "Vous ne pouvez pas créé de nouveau tour, "
                "tant que le tour précédent n'est pas clôturé"
            )
            print("--------------")
            rounds_controller(tournament)
    if len(tournament.players) != 8:
        print("--------------")
        print(
            "Vous ne pouvez pas commencer de parties "
            "tant que le nombre de joueurs est inférieur à 8."
        )
        print("--------------")
        rounds_controller(tournament)
    else:
        if len(tournament.rounds) >= tournament.number_of_rounds:
            print(
                "Vous avez atteint la limite du nombre de tours, "
                "le tournoi est déjà terminé."
            )
            selected_tournament.selected_tournament_controller(tournament)

        new_round_number = len(tournament.rounds) + 1
        new_round_name = f"Tour {new_round_number}"
        new_round = Round(new_round_name)
        new_round.starting()
        tournament.add_round(new_round)

        if len(tournament.rounds) == 1:
            tournament.order_players_by_points_and_ranks()
            half = len(tournament.players) // 2
            first_half = tournament.players[:half]
            second_half = tournament.players[half:]

            i = 0
            for player_one in first_half:
                player_two = second_half[i]
                new_match = Match(player_one, player_two)
                new_round.matches.append(new_match)
                print(
                    f"Le match joueur {player_one.firstname} "
                    f"contre joueur {player_two.firstname} "
                    f"a été ajouté au {new_round}"
                )
                i += 1

            # save_data(all_tournaments.tournaments)
            print("Premier tour créé")
            rounds_controller(tournament)

        elif len(tournament.rounds) > 1:
            players_history = tournament.get_players_history()
            tournament.order_players_by_points_and_ranks()

            assigned_players = []
            for player in tournament.players:
                # si on a déjà trouvé un match au joueur, on s'en occupe pas
                if player not in assigned_players:
                    # on parcourt tous les joueurs pour trouver un contestant
                    for other_player in tournament.players:
                        # un contestant est bon si
                        # - ce n'est pas le joueur lui même
                        # - ce contestant potentiel n'a pas déjà un match
                        # dans ce round
                        # - le joueur n'a jamais joué avec lui
                        if (
                                other_player != player
                                and other_player not in assigned_players
                                and other_player not in players_history[player.player_id]
                        ):
                            new_match = Match(player, other_player)
                            new_round.matches.append(new_match)
                            assigned_players.append(player)
                            assigned_players.append(other_player)
                            players_history[player.player_id].append(other_player)
                            players_history[other_player.player_id].append(player)
                            print(
                                f"Le match joueur {player.firstname} "
                                f"contre joueur {other_player.firstname} "
                                f"a été ajouté au {new_round}"
                            )
                            break

            # save_data(all_tournaments.tournaments)
            print("Fin de la création des matchs")

            print(f"Le {new_round} a été créé.")
            rounds_controller(tournament)


def delete_round_controller(tournament):
    if not tournament.rounds:
        print("Il n'y a pas encore de tour créé dans ce tournoi.")
        rounds_controller(tournament)
    else:
        for i, tournament_round in enumerate(tournament.rounds):
            print(f"{i + 1}/ Supprimer {tournament_round}")
        print(f"{len(tournament.rounds) + 1}/ Retour en arrière")
        choice = input("Tapez le numéro du tour à supprimer: ")
        if not check_int_input(choice):
            delete_round_controller(tournament)
        else:
            choice = int(choice) - 1
            if choice == len(tournament.rounds):
                rounds_controller(tournament)
            elif choice > len(tournament.rounds):
                print("Je n'ai pas compris votre choix.")
                delete_round_controller(tournament)
            if check_deletion():
                round_to_delete = tournament.rounds[choice]
                tournament.delete_round(round_to_delete)
                # save_data(all_tournaments.tournaments)
                print(f"Le {round_to_delete} a bien été supprimé.")
                print("-----------------------")
                rounds_controller(tournament)
            else:
                rounds_controller(tournament)


def edit_round_controller(tournament):
    if not tournament.rounds:
        print("Il n'y a pas encore de tour créé dans ce tournoi.")
        rounds_controller(tournament)
    else:
        # print("Quel tour souhaitez vous modifier ?")
        # for i, round in enumerate(tournament.rounds):
        #     print(f"{i + 1}/ {round} ?")
        # choice = input("Tapez le numéro du tour à sélectionner: ")
        # if not check_int_input(choice):
        #     print("Je n'ai pas compris votre choix.")
        #     edit_round_controller(tournament)
        # else:
        matches_controller(tournament.rounds[-1])
        # save_data(all_tournaments.tournaments)
        rounds_controller(tournament)
