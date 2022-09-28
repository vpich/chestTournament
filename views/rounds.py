class RoundsView:
    @staticmethod
    def rounds(tournament):
        print("--------------")
        print("Liste des tours du tournoi:")
        for each_round in tournament.rounds:
            print(each_round)
        print("--------------")
        print("Que souhaitez_vous faire ?")
        print("")
        print("1/ Commencer un nouveau tour")
        print("2/ Supprimer un tour")
        print("3/ Gérer un match dans le tour actuel")
        print("4/ Clôturer le tour actuel")
        print("5/ Retour en arrière")

        print("--------------")
        choice = input("Tapez le nombre du choix à sélectionner: ")
        print("")
        return choice

    @staticmethod
    def no_rounds():
        print("--------------")
        print("Il n'y a pas encore de tour créé dans ce tournoi.")
        print("")

    @staticmethod
    def end_round_fail():
        print(
            "Vous ne pouvez pas clôturer ce tour, "
            "tant que les matchs ne sont pas terminés"
        )

    @staticmethod
    def end_round_success(round_to_end):
        print(f"Le {round_to_end} a bien été clôturé.")

    @staticmethod
    def round_not_ended():
        print(
            "Vous ne pouvez pas créer de nouveau tour, "
            "tant que le tour précédent n'est pas clôturé"
        )

    @staticmethod
    def not_enough_player():
        print(
            "Vous ne pouvez pas commencer de parties "
            "tant que le nombre de joueurs est inférieur à 8."
        )

    @staticmethod
    def tournament_is_over():
        print(
            "Vous avez atteint la limite du nombre de tours, "
            "le tournoi est déjà terminé."
        )

    @staticmethod
    def new_match_in_round(player_one, player_two, new_round):
        print(
            f"Le match joueur {player_one.firstname} "
            f"contre joueur {player_two.firstname} "
            f"a été ajouté au {new_round}"
        )

    @staticmethod
    def new_match_in_round_same_opponent(player, other_player, new_round):
        print(
            f"Le match joueur {player.firstname} "
            f"contre joueur {other_player.firstname} "
            f"a été ajouté au {new_round} (bien qu'ils aient déjà joué ensemble)"
        )

    @staticmethod
    def add_round_success(new_round):
        print("Fin de la création des matchs")
        print(f"Le {new_round} a été créé.")

    @staticmethod
    def delete_round(tournament):
        print("--------------")
        print("Quel tour souhaitez-vous supprimer ?")
        print("")
        for i, tournament_round in enumerate(tournament.rounds):
            print(f"{i + 1}/ Supprimer {tournament_round}")
        print(f"{len(tournament.rounds) + 1}/ Retour en arrière")
        choice = input("Tapez le numéro du tour à supprimer: ")
        return choice

    @staticmethod
    def delete_round_success(round_to_delete):
        print(f"Le {round_to_delete} a bien été supprimé.")
