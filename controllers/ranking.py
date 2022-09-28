from views import SortPlayersView


class SortPlayers:
    @staticmethod
    def by_ranking(tournament):
        SortPlayersView.by_ranking(tournament)
        if not tournament.players:
            SortPlayersView.no_player()
        else:
            tournament.order_players_by_points_and_ranks()
            for i, player in enumerate(tournament.players):
                SortPlayersView.display_rank(i, player)
        SortPlayersView.empty_space()

    @staticmethod
    def by_name(tournament):

        if not tournament.players:
            SortPlayersView.no_player()
        else:
            tournament.order_players_by_last_name()
            for i, player in enumerate(tournament.players):
                SortPlayersView.display_name(i, player)
