from views import PlayersView
from models import Player
from .checks import Checks
from .ranking import ranking_controller, filter_players_by_name
from . import selected_tournament, crud_data, tournaments


class PlayersController:

    def players_controller(self, tournament):

        choice = PlayersView.players_view(self, tournament)

        if Checks.check_int_input(self, choice):
            choice = int(choice)
        else:
            self.players_controller(tournament)

        if choice == 1:
            self.add_player(tournament)
        elif choice == 2:
            self.edit_player(self, tournament)
        elif choice == 3:
            self.delete_player(self, tournament)
        elif choice == 4:
            ranking_controller(tournament)
            self.players_controller(tournament)
        elif choice == 5:
            filter_players_by_name(tournament)
            self.players_controller(tournament)
        elif choice == 6:
            selected_tournament.selected_tournament_controller(tournament)
        else:
            PlayersView.unknown_choice(self)
            self.players_controller(tournament)

    def add_player(self, tournament):

        if len(tournament.players) >= 8:
            print("Vous avez atteint le nombre maximal de 8 joueurs.")
            self.players_controller(tournament)
        else:
            if not tournament.players:
                player_id = 1
            else:
                player_id = len(tournament.players) + 1
            new_player_info = PlayersView.add_player_view(self)
            if not Checks.check_date_format(self, new_player_info["date_of_birth"]):
                print(
                    "La date de naissance est invalide, "
                    "veuillez taper une date au format JJ/MM/AAAA"
                )
                self.add_player(tournament)

            if new_player_info["rank"] == "":
                rank = 0
            else:
                if not Checks.check_int_input(self, new_player_info["rank"]):
                    print("La rang doit être un nombre entier.")
                    print("")
                    self.add_player(tournament)
                else:
                    rank = int(new_player_info["rank"])
            new_player = Player(
                player_id,
                new_player_info["firstname"],
                new_player_info["lastname"],
                new_player_info["date_of_birth"],
                new_player_info["gender"],
                rank
            )
            tournament.players.append(new_player)
            crud_data.save_data(tournaments.all_tournaments.tournaments)
            print(f'Le joueur {new_player_info["firstname"]} {new_player_info["lastname"]} '
                  f'a bien été ajouté au tournoi.')
            self.players_controller(tournament)

    @staticmethod
    def edit_player(self, tournament):
        if not tournament.players:
            print("--------------")
            print("Il n'y a aucun joueur d'enregistrés.")
            print("")
            self.players_controller(tournament)
        else:
            print("--------------")
            print("Pour quel joueur souhaitez-vous modifier les informations ?")
            print("")
            for i, player in enumerate(tournament.players):
                print(f"{i + 1}/ Modifier le joueur {player}")
            choice = input("Tapez le numéro du joueur à modifier: ")

            if Checks.check_int_input(self, choice):
                choice = int(choice) - 1
            else:
                self.edit_player(tournament)

            if choice > len(tournament.players):
                print("Je n'ai pas compris votre choix.")
                print(
                    f"Veuillez saisir un chiffre compris "
                    f"entre 1 et {len(tournament.players)}"
                )
                self.edit_player(tournament)

            player_to_modify = tournament.players[choice]
            print("--------------")
            print(f"Vous allez éditer les informations de {player_to_modify}")
            print("Que souhaitez-vous modifier ?")
            print("")
            print("1/ Son prénom")
            print("2/ Son nom de famille")
            print("3/ Sa date de naissance")
            print("4/ Son sexe")
            print("5/ Son score")
            print("6/ Retour en arrière")
            choice = int(input("Tapez le numéro à modifier: "))
            if choice == 1:
                firstname = input("Entrez le prénom du joueur: ")
                player_to_modify.firstname = firstname
            elif choice == 2:
                lastname = input("Entrez le nom de famille du joueur: ")
                player_to_modify.lastname = lastname
            elif choice == 3:
                date_of_birth = Checks.check_date_format(
                    self,
                    input("Entrez la date de naissance du joueur: ")
                )
                if not date_of_birth:
                    print(
                        "La date de naissance est invalide, "
                        "veuillez taper une date au format JJ/MM/AAAA"
                    )
                    self.edit_player(tournament)
                player_to_modify.date_of_birth = date_of_birth
            elif choice == 4:
                gender = input("Entrez le sexe du joueur: ")
                player_to_modify.gender = gender
            elif choice == 5:
                rank = input("Entrez le score du joueur: ")
                if Checks.check_int_input(self, rank):
                    rank = int(rank)
                else:
                    self.edit_player(tournament)
                player_to_modify.rank = rank
            elif choice == 6:
                self.players_controller(tournament)
            else:
                print("Je n'ai pas compris votre choix.")
                self.edit_player(tournament)
            crud_data.save_data(tournaments.all_tournaments.tournaments)
            print("La modification a été enregistrée.")
            self.players_controller(tournament)

    @staticmethod
    def delete_player(self, tournament):
        if not tournament.players:
            print("--------------")
            print("Il n'y a aucun joueur d'enregistré.")
            print("")
            self.players_controller(tournament)
        else:
            print("--------------")
            print("Quel joueur souhaitez-vous supprimer du tournoi ?")
            print("")
            for i, player in enumerate(tournament.players):
                print(f"{i + 1}/ Supprimer {player} ?")
            print(f"{len(tournament.players) + 1}/ Retour en arrière")
            choice = input("Tapez le numéro du joueur à supprimer: ")

            if Checks.check_int_input(self, choice):
                choice = int(choice) - 1
            else:
                self.delete_player(tournament)

            if choice == len(tournament.players):
                self.players_controller(tournament)

            if choice > len(tournament.players):
                print("Je n'ai pas compris votre choix.")
                print(
                    f"Veuillez saisir un chiffre compris "
                    f"entre 1 et {len(tournament.players) + 1}"
                )
                self.delete_player(tournament)

            player_to_delete = tournament.players[choice]
            if Checks.check_deletion(self):
                tournament.delete_player(player_to_delete)
                crud_data.save_data(tournaments.all_tournaments.tournaments)
                print(f"Le joueur {player_to_delete} a bien été supprimé.")
                self.players_controller(tournament)
            else:
                self.players_controller(tournament)
