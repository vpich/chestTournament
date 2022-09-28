from models import Round, Match
from views import RoundsView, ErrorsViews
from .checks import Check
from . import selected_tournament, tournaments
from .matches import MatchesController
from . import crud_data

matches_self = MatchesController()


class RoundsController:

    def main(self, tournament):
        choice = RoundsView.rounds(tournament)

        if Check.int_input(choice):
            choice = int(choice)
        else:
            self.main(tournament)

        if choice == 1:
            self.add_round(tournament)
        elif choice == 2:
            self.delete_round(tournament)
        elif choice == 3:
            self.edit_round(tournament)
        elif choice == 4:
            self.end_round(tournament)
        elif choice == 5:
            selected_tournament_self = selected_tournament.SelectedTournamentController()
            selected_tournament.SelectedTournamentController.main(selected_tournament_self,
                                                                  tournament)
        else:
            ErrorsViews.unknown_choice()
            self.main(tournament)

    def end_round(self, tournament):
        if not tournament.rounds:
            RoundsView.no_rounds()
            self.main(tournament)
        else:
            round_to_end = tournament.rounds[-1]
            for match in round_to_end.matches:
                if match.in_progress:
                    RoundsView.end_round_fail()
                    self.main(tournament)
            round_to_end.ending()
            RoundsView.end_round_success(round_to_end)
            crud_data.Data.save(tournaments.all_tournaments.tournaments)
            self.main(tournament)

    @staticmethod
    def new_round_parameters(player, other_player, new_round, assigned_players, players_history):
        new_match = Match(player, other_player)
        new_round.matches.append(new_match)
        assigned_players.append(player)
        assigned_players.append(other_player)
        players_history[player.player_id].append(other_player)
        players_history[other_player.player_id].append(player)

    def add_round(self, tournament):
        if tournament.rounds:
            last_round = tournament.rounds[-1]
            if not last_round.end_time:
                RoundsView.round_not_ended()
                self.main(tournament)
        if len(tournament.players) != 8:
            RoundsView.not_enough_player()
            self.main(tournament)
        else:
            if len(tournament.rounds) >= tournament.number_of_rounds:
                RoundsView.tournament_is_over()
                selected_tournament_self = selected_tournament.SelectedTournamentController()
                selected_tournament.SelectedTournamentController.main(selected_tournament_self,
                                                                      tournament)

            new_round_number = len(tournament.rounds) + 1
            new_round_name = f"Tour {new_round_number}"
            new_round = Round(new_round_name)
            new_round.starting()
            tournament.add_round(new_round)

            if len(tournament.rounds) == 1:
                tournament.order_players_by_points_and_ranks()
                half = len(tournament.players) // 2
                first_half = tournament.players[:half]
                second_half = tournament.players[half:]

                i = 0
                for player_one in first_half:
                    player_two = second_half[i]
                    new_match = Match(player_one, player_two)
                    new_round.matches.append(new_match)
                    RoundsView.new_match_in_round(player_one, player_two, new_round)
                    i += 1

                crud_data.Data.save(tournaments.all_tournaments.tournaments)
                RoundsView.add_round_success(new_round)
                self.main(tournament)

            else:
                players_history = tournament.get_players_history()
                tournament.order_players_by_points_and_ranks()

                assigned_players = []
                for player in tournament.players:
                    if player not in assigned_players:
                        found_oponent = False
                        for other_player in tournament.players:
                            if (
                                    other_player != player
                                    and other_player not in assigned_players
                                    and other_player not in players_history[player.player_id]
                            ):
                                self.new_round_parameters(player, other_player, new_round,
                                                          assigned_players, players_history)
                                RoundsView.new_match_in_round(player, other_player, new_round)
                                found_oponent = True
                                break
                        if not found_oponent:
                            for other_player in tournament.players:
                                if (
                                        other_player != player
                                        and other_player not in assigned_players
                                ):
                                    self.new_round_parameters(player, other_player, new_round,
                                                              assigned_players, players_history)
                                    RoundsView.new_match_in_round_same_opponent(player,
                                                                                other_player,
                                                                                new_round)
                                    break

                crud_data.Data.save(tournaments.all_tournaments.tournaments)
                RoundsView.add_round_success(new_round)
                self.main(tournament)

    def delete_round(self, tournament):
        if not tournament.rounds:
            RoundsView.no_rounds()
            self.main(tournament)
        else:
            choice = RoundsView.delete_round(tournament)
            if not Check.int_input(choice):
                self.delete_round(tournament)
            else:
                choice = int(choice) - 1
                if choice == len(tournament.rounds):
                    self.main(tournament)
                elif choice > len(tournament.rounds):
                    ErrorsViews.unknown_choice()
                    self.delete_round(tournament)
                if Check.deletion():
                    round_to_delete = tournament.rounds[choice]
                    tournament.delete_round(round_to_delete)
                    crud_data.Data.save(tournaments.all_tournaments.tournaments)
                    RoundsView.delete_round_success(round_to_delete)
                    self.main(tournament)
                else:
                    self.main(tournament)

    def edit_round(self, tournament):
        if not tournament.rounds:
            RoundsView.no_rounds()
            self.main(tournament)
        else:
            MatchesController.main(matches_self, tournament.rounds[-1])
            crud_data.Data.save(tournaments.all_tournaments.tournaments)
            self.main(tournament)
