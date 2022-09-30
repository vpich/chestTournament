import random

from views import MatchesView, ErrorsViews, Utilitaries
from .checks import Check
from . import crud_data, tournaments


class MatchesController:

    def main(self, tournament_round):
        match_selected = MatchesView.main(tournament_round)
        if not Check.int_input(match_selected):
            ErrorsViews.unknown_choice()
            self.main(tournament_round)
        else:
            match_selected = int(match_selected) - 1
            if match_selected < len(tournament_round.matches):
                self.match_selected(tournament_round.matches[match_selected])
                self.main(tournament_round)
            elif match_selected == len(tournament_round.matches):
                pass
            else:
                ErrorsViews.unknown_choice()
                self.main(tournament_round)

    def match_selected(self, match):
        choice = MatchesView.match_selected(match)
        if not Check.int_input(choice):
            self.match_selected(match)
        else:
            choice = int(choice)
            if choice == 1:
                choices = ["noir", "blanc"]
                color = random.choice(choices)
                MatchesView.random_color(match.contestants[0], color)
                self.match_selected(match)
            elif choice == 2:
                self.update_winner(match)
            elif choice == 3:
                pass
            else:
                ErrorsViews.unknown_choice()
                self.match_selected(match)

    def update_winner(self, match):
        winner = MatchesView.update_winner(match)
        if not Check.int_input(winner):
            ErrorsViews.unknown_choice()
            self.update_winner(match)
        else:
            winner = int(winner)
            if winner == 1:
                match.add_score_to_winner(match.contestants[0])
                MatchesView.player_one_wins(match)
                crud_data.Data.save(tournaments.all_tournaments.tournaments)
                Utilitaries.empty_space()
            elif winner == 2:
                match.add_score_to_winner(match.contestants[1])
                MatchesView.player_two_wins(match)
                crud_data.Data.save(tournaments.all_tournaments.tournaments)
                Utilitaries.empty_space()
            elif winner == 3:
                match.add_score_to_winner(None)
                MatchesView.draw(match)
                crud_data.Data.save(tournaments.all_tournaments.tournaments)
                Utilitaries.empty_space()
            elif winner == 4:
                pass
            else:
                ErrorsViews.unknown_choice()
                self.update_winner(match)
