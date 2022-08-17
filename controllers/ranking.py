def ranking_controller(tournament):
    print(f"Il y a actuellement {len(tournament.rounds)} tour(s) dans le tournoi {tournament}")
    print(f"Voici le classement des joueurs pour ce tournoi:")
    if not tournament.players:
        print("Il n'y a pas de joueurs qui participent à ce tournoi.")
    else:
        tournament.order_players_by_points_and_ranks()
        for player in tournament.players:
            player.rank = tournament.players.index(player) + 1
        for i, player in enumerate(tournament.players):
            print(f"{i + 1}/ {player}")
    print("----------------------")
