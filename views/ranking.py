class SortPlayersView:
    @staticmethod
    def by_ranking(tournament):
        print("--------------")
        print(f"Voici le classement des joueurs pour le tournoi {tournament}:")
        print("")

    @staticmethod
    def display_rank(i, player):
        print(f"{i + 1}/ {player}, points gagnés: {player.total_points}, rang: {player.rank}")

    @staticmethod
    def by_name():
        print("--------------")
        print("Voici la liste des joueurs triés par nom de famille:")
        print("")

    @staticmethod
    def display_name(i, player):
        print(f"{i + 1}/ Joueur {player.lastname} {player.firstname}")

    @staticmethod
    def no_player():
        print("Il n'y a pas de joueurs qui participent à ce tournoi.")

    @staticmethod
    def empty_space():
        print("")
