def ranking_controller(tournament):
    print(f"Le tournoi {tournament.name} se situant {tournament.place} "
          f"se déroule {tournament.date.lower()}.")
    print(f"Le contrôle du temps est le {tournament.time_control}, "
          f"et il doit comporter {tournament.number_of_rounds} tours.")
    print(
        f"Il y a actuellement {len(tournament.rounds)} tour(s) "
        f"dans le tournoi {tournament}."
    )
    print("Voici le classement des joueurs pour ce tournoi:")
    if not tournament.players:
        print("Il n'y a pas de joueurs qui participent à ce tournoi.")
    else:
        tournament.order_players_by_points_and_ranks()
        for player in tournament.players:
            player.rank = tournament.players.index(player) + 1
        for i, player in enumerate(tournament.players):
            print(f"{i + 1}/ {player}, points gagnés: {player.total_points}")
    print("----------------------")
