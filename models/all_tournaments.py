from models import Tournament


class AllTournaments:
    def __init__(self):
        self.tournaments = []

    def add_tournament(self, tournament):
        assert type(tournament) == Tournament
        self.tournaments.append(tournament)

    def delete_tournament(self, tournament):
        assert type(tournament) == Tournament
        self.tournaments.remove(tournament)
