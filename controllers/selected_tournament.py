from datetime import datetime

from views import selected_tournament_view
from .checks import Check
from . import players
from .rounds import RoundsController
from .time_control import time_control_selection
from . import tournaments
from crud_data import Data


class SelectedTournamentController:
    def main(self, tournament):
        selected_tournament_view(tournament)
        choice = input("Tapez le numéro du choix à sélectionner: ")

        if Check.int_input(choice):
            choice = int(choice)
        else:
            self.main(tournament)

        if choice == 1:
            self.edit_selected_tournament(tournament)
        elif choice == 2:
            players.PlayersController.main(tournament)
        elif choice == 3:
            RoundsController.main(tournament)
        elif choice == 4:
            tournaments.tournaments_controller()
        else:
            print("Je n'ai pas compris votre choix.")
            self.main(tournament)
        print("-")

    def edit_selected_tournament(self, tournament):
        print("--------------")
        print("Voici les informations actuelles du tournoi:")
        print(
            f"Nom: {tournament.name}, Lieu: {tournament.place}, "
            f"Date: {tournament.date}, "
            f"Contrôle du temps: {tournament.time_control}, "
            f"Nombre de tours: {tournament.number_of_rounds}"
        )
        print("--------------")
        print("Que souhaitez-vous modifier ?")
        print("")
        print("1/ Le nom")
        print("2/ Le lieu")
        print("3/ La date")
        print("4/ Le contrôle du temps")
        print("5/ Le nombre de tours")
        print("6/ Retour en arrière")
        choice = input("Taper un chiffre entre 1 et 6: ")
        if not Check.int_input(choice):
            self.edit_selected_tournament(tournament)
        else:
            choice = int(choice)
            if choice == 1:
                name = input("Entrez le nom du tournoi: ")
                tournament.name = name
            elif choice == 2:
                place = input("Entrez le lieu: ")
                tournament.place = place
            elif choice == 3:
                start_date = Check.date_format(input("Entrez la date de début de tournoi: "))
                if not start_date:
                    self.edit_selected_tournament(tournament)
                else:
                    start_date = datetime.strptime(start_date, "%d/%m/%Y")
                tournament.date = start_date
            elif choice == 4:
                time_control = time_control_selection()
                tournament.time_control = time_control
            elif choice == 5:
                user_input = input("Entrez le nombre de tours: ")
                if Check.int_input(user_input):
                    number_of_rounds = int(user_input)
                    tournament.number_of_rounds = number_of_rounds
                else:
                    print("Saisie invalide. Veuillez rentrer un chiffre entier.")
                    self.edit_selected_tournament(tournament)
            elif choice == 6:
                self.main(tournament)
            else:
                print("Je n'ai pas compris votre choix.")
                self.edit_selected_tournament(tournament)
            Data.save(tournaments.all_tournaments.tournaments)
            print(f"Le tournoi {tournament} a bien été modifié.")
            self.main(tournament)
