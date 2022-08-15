from models import Tournament


class AllTournaments:
    def __init__(self):
        self.tournaments = []

    def __str__(self):
        print("Voici tous les tournois enregistrés: ")
        for i, tournament in enumerate(self.tournaments):
            print(f"{i}/ {tournament}")

    def add_tournament(self, tournament):
        assert type(tournament) == Tournament
        self.tournaments.append(tournament)

    def delete_tournament(self, tournament):
        assert type(tournament) == Tournament
        self.tournaments.remove(tournament)
