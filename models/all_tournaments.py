from models import Tournament


class AllTournaments:
    def __init__(self):
        self.tournaments = []
        all_tournaments_data = db.all()
        for tournament_data in all_tournaments_data:
            list_players = []
            for player_data in tournament_data["Players"]:
                list_players.append(Player(player_data))
            tournament = Tournament(tournament_data)
            self.tournaments.append(tournament)

    def __str__(self):
        print("Voici tous les tournois enregistrés: ")
        for i, tournament in enumerate(self.tournaments):
            print(f"{i + 1}/ {tournament}")

    def add_tournament(self, tournament):
        assert type(tournament) == Tournament
        self.tournaments.append(tournament)

    def delete_tournament(self, tournament):
        assert type(tournament) == Tournament
        self.tournaments.remove(tournament)
