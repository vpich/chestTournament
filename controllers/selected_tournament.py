from datetime import datetime

from views import SelectedTournamentView, ErrorsViews, Utilitaries
from .checks import Check
from . import players
from .rounds import RoundsController
from .time_control import TimeControl
from . import tournaments, crud_data

players_controller_self = players.PlayersController()
rounds_controller_self = RoundsController()
time_control_self = TimeControl()


class SelectedTournamentController:
    def main(self, tournament):
        choice = SelectedTournamentView.main(tournament)

        if Check.int_input(choice):
            choice = int(choice)
        else:
            self.main(tournament)

        if choice == 1:
            self.edit_selected_tournament(tournament)
        elif choice == 2:
            players.PlayersController.main(players_controller_self, tournament)
        elif choice == 3:
            RoundsController.main(rounds_controller_self, tournament)
        elif choice == 4:
            tournaments_controller_self = tournaments.TournamentsController()
            tournaments.TournamentsController.main(tournaments_controller_self)
        else:
            ErrorsViews.unknown_choice()
            self.main(tournament)
        Utilitaries.empty_space()

    def edit_selected_tournament(self, tournament):
        choice = SelectedTournamentView.edit(tournament)
        if not Check.int_input(choice):
            self.edit_selected_tournament(tournament)
        else:
            choice = int(choice)
            if choice == 1:
                name = SelectedTournamentView.edit_choice(choice)
                tournament.name = name
            elif choice == 2:
                place = SelectedTournamentView.edit_choice(choice)
                tournament.place = place
            elif choice == 3:
                start_date = Check.date_format(SelectedTournamentView.edit_choice(choice))
                if not start_date:
                    self.edit_selected_tournament(tournament)
                else:
                    start_date = datetime.strptime(start_date, "%d/%m/%Y")
                tournament.date = start_date
            elif choice == 4:
                time_control = TimeControl.selection(time_control_self)
                tournament.time_control = time_control
            elif choice == 5:
                user_input = SelectedTournamentView.edit_choice(choice)
                if Check.int_input(user_input):
                    number_of_rounds = int(user_input)
                    tournament.number_of_rounds = number_of_rounds
                else:
                    ErrorsViews.unknown_choice()
                    self.edit_selected_tournament(tournament)
            elif choice == 6:
                self.main(tournament)
            else:
                ErrorsViews.unknown_choice()
                self.edit_selected_tournament(tournament)
            crud_data.Data.save(tournaments.all_tournaments.tournaments)
            SelectedTournamentView.edit_success(tournament)
            self.main(tournament)
