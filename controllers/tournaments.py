from models import AllTournaments, Tournament
from views import TournamentsView, QuitView, ErrorsViews, Utilitaries
from .checks import Check
from .ranking import SortPlayers
from . import crud_data
from .selected_tournament import SelectedTournamentController
from .time_control import TimeControl

all_tournaments = AllTournaments()
selected_tournament_self = SelectedTournamentController()


class TournamentsController:
    def main(self):
        choice = TournamentsView.main()

        if Check.int_input(choice):
            choice = int(choice)
        else:
            self.main()

        if choice == 1:
            self.add_tournament()
        elif choice == 2:
            self.show_tournaments()
        elif choice == 3:
            self.manage_tournament()
        elif choice == 4:
            self.delete_tournament()
        elif choice == 5:
            crud_data.Data.delete()
        elif choice == 6:
            QuitView.quit()
            exit()
        else:
            ErrorsViews.unknown_choice()
            self.main()
        Utilitaries.empty_space()

    def manage_tournament(self):
        if not all_tournaments.tournaments:
            TournamentsView.no_tournaments()
            self.main()
        else:
            selected_tournament = TournamentsView.manage(all_tournaments)
            if Check.int_input(selected_tournament):
                selected_tournament = int(selected_tournament) - 1
            else:
                self.manage_tournament()

            if selected_tournament < 0:
                ErrorsViews.unknown_choice()
                ErrorsViews.number_required()
                self.manage_tournament()
            elif selected_tournament == len(all_tournaments.tournaments):
                self.main()
            elif selected_tournament > len(all_tournaments.tournaments):
                ErrorsViews.unknown_choice()
                ErrorsViews.number_required()
                self.manage_tournament()

            SelectedTournamentController.main(selected_tournament_self,
                                              all_tournaments.tournaments[selected_tournament])

    def show_tournaments(self):
        TournamentsView.show(all_tournaments)
        for tournament in all_tournaments.tournaments:
            TournamentsView.show_each_tournament(tournament)
            SortPlayers.by_ranking(tournament)
        self.main()

    def add_tournament(self):
        new_tournament_info = TournamentsView.add()
        name = new_tournament_info["name"]
        place = new_tournament_info["place"]

        if not all_tournaments.tournaments:
            tournament_id = 1
        else:
            tournament_id = len(all_tournaments.tournaments) + 1

        start_date = Check.date_format(new_tournament_info["start_date"])
        if not start_date:
            self.add_tournament()
        else:
            start_date = start_date.strftime("%d/%m/%Y")

        time_control_signature = TimeControl()
        time_control = TimeControl.selection(time_control_signature)
        number_of_rounds = new_tournament_info["number_of_rounds"]

        if number_of_rounds == "":
            number_of_rounds = 4
        elif number_of_rounds == "0":
            TournamentsView.number_of_round_not_null()
            self.add_tournament()
        elif not Check.int_input(number_of_rounds):
            self.add_tournament()
        else:
            number_of_rounds = int(number_of_rounds)

        new_tournament = Tournament(
            tournament_id, name, place, start_date, time_control, number_of_rounds
        )
        description = new_tournament_info["description"]
        new_tournament.description = description
        TournamentsView.add_success()
        all_tournaments.add_tournament(new_tournament)
        crud_data.Data.save(all_tournaments.tournaments)
        self.main()

    def delete_tournament(self):
        if len(all_tournaments.tournaments) == 0:
            TournamentsView.no_tournaments()
            self.main()
        else:
            choice = TournamentsView.delete(all_tournaments)

            if Check.int_input(choice):
                choice = int(choice) - 1
            else:
                self.delete_tournament()

            if choice >= len(all_tournaments.tournaments):
                ErrorsViews.unknown_choice()
                ErrorsViews.number_required()
                self.delete_tournament()

            tournament_to_delete = all_tournaments.tournaments[choice]
            if Check.deletion():
                all_tournaments.delete_tournament(tournament_to_delete)
                crud_data.Data.delete_tournament(tournament_to_delete.tournament_id)
                TournamentsView.delete_success(tournament_to_delete)
                self.main()
            else:
                self.main()
