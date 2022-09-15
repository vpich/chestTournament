def ranking_controller(tournament):
    print("--------------")
    print(f"Voici le classement des joueurs pour le tournoi {tournament}:")
    print("--------------")
    if not tournament.players:
        print("Il n'y a pas de joueurs qui participent à ce tournoi.")
    else:
        tournament.order_players_by_points_and_ranks()
        for player in tournament.players:
            player.rank = tournament.players.index(player) + 1
        for i, player in enumerate(tournament.players):
            print(f"{i + 1}/ {player}, points gagnés: {player.total_points}")
    print("")


def filter_players_by_name(tournament):
    print("--------------")
    print("Voici la liste des joueurs triés par nom de famille:")
    print("--------------")
    if not tournament.players:
        print("Il n'y a pas de joueurs qui participent à ce tournoi.")
    else:
        tournament.order_players_by_last_name()
        for i, player in enumerate(tournament.players):
            print(f"{i + 1}/ Joueur {player.lastname} {player.firstname}")
