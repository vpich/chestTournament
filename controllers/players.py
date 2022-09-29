from views import PlayersView, ErrorsViews, Utilitaries
from models import Player
from .checks import Check
from .ranking import SortPlayers
from . import selected_tournament, tournaments
from . import crud_data


class PlayersController:

    def main(self, tournament):

        choice = PlayersView.main(tournament)

        if Check.int_input(choice):
            choice = int(choice)
        else:
            self.main(tournament)

        if choice == 1:
            self.add_player(tournament)
        elif choice == 2:
            self.edit_player(tournament)
        elif choice == 3:
            self.delete_player(tournament)
        elif choice == 4:
            SortPlayers.by_ranking(tournament)
            self.main(tournament)
        elif choice == 5:
            SortPlayers.by_name(tournament)
            self.main(tournament)
        elif choice == 6:
            selected_tournament_self = selected_tournament.SelectedTournamentController()
            selected_tournament.SelectedTournamentController.main(selected_tournament_self,
                                                                  tournament)
        else:
            PlayersView.unknown_choice()
            self.main(tournament)

    def add_player(self, tournament):

        if len(tournament.players) >= 8:
            PlayersView.max_players()
            self.main(tournament)
        else:
            if not tournament.players:
                player_id = 1
            else:
                player_id = len(tournament.players) + 1
            new_player_info = PlayersView.add_player()

            if new_player_info["rank"] == "":
                rank = 0
            else:
                if not Check.int_input(new_player_info["rank"]):
                    Utilitaries.empty_space()
                    self.add_player(tournament)
                else:
                    rank = int(new_player_info["rank"])

            if not Check.date_format(new_player_info["date_of_birth"]):
                Utilitaries.empty_space()
                self.add_player(tournament)

            new_player = Player(
                player_id,
                new_player_info["firstname"],
                new_player_info["lastname"],
                new_player_info["date_of_birth"],
                new_player_info["gender"],
                rank
            )
            tournament.players.append(new_player)
            crud_data.Data.save(tournaments.all_tournaments.tournaments)
            PlayersView.add_player_success(new_player)
            self.main(tournament)

    def edit_player(self, tournament):
        if not tournament.players:
            PlayersView.no_player()
            self.main(tournament)
        else:
            choice = PlayersView.edit_player_selection(tournament)

            if Check.int_input(choice):
                choice = int(choice) - 1
            else:
                self.edit_player(tournament)

            if choice > len(tournament.players):
                ErrorsViews.unknown_choice()
                ErrorsViews.number_required()
                self.edit_player(tournament)

            player_to_modify = tournament.players[choice]
            choice = PlayersView.edit_player_choices(player_to_modify)
            if choice == 1:
                firstname = PlayersView.edit_player(choice)
                player_to_modify.firstname = firstname
            elif choice == 2:
                lastname = PlayersView.edit_player(choice)
                player_to_modify.lastname = lastname
            elif choice == 3:
                date_of_birth = Check.date_format(PlayersView.edit_player(choice))
                if not date_of_birth:
                    self.edit_player(tournament)
                player_to_modify.date_of_birth = date_of_birth
            elif choice == 4:
                gender = PlayersView.edit_player(choice)
                player_to_modify.gender = gender
            elif choice == 5:
                rank = PlayersView.edit_player(choice)
                if Check.int_input(rank):
                    rank = int(rank)
                else:
                    self.edit_player(tournament)
                player_to_modify.rank = rank
            elif choice == 6:
                self.main(tournament)
            else:
                ErrorsViews.unknown_choice()
                self.edit_player(tournament)
            crud_data.Data.save(tournaments.all_tournaments.tournaments)
            PlayersView.edit_player_success()
            self.main(tournament)

    def delete_player(self, tournament):
        if not tournament.players:
            PlayersView.no_player()
            self.main(tournament)
        else:
            choice = PlayersView.delete_player(tournament)

            if Check.int_input(choice):
                choice = int(choice) - 1
            else:
                self.delete_player(tournament)

            if choice == len(tournament.players):
                self.main(tournament)

            if choice > len(tournament.players):
                ErrorsViews.unknown_choice()
                ErrorsViews.number_required()
                self.delete_player(tournament)

            player_to_delete = tournament.players[choice]
            if Check.deletion():
                tournament.delete_player(player_to_delete)
                crud_data.Data.save(tournaments.all_tournaments.tournaments)
                PlayersView.delete_player_success(player_to_delete)
                self.main(tournament)
            else:
                self.main(tournament)
