from models import AllTournaments, Tournament
from views import TournamentsView, QuitView
from .checks import Check
from .ranking import SortPlayers
from . import crud_data
from .selected_tournament import SelectedTournamentController
from .time_control import TimeControl

all_tournaments = AllTournaments()
selected_tournament_self = SelectedTournamentController()


class TournamentsController:
    def main(self):
        TournamentsView.tournaments()
        choice = input("Tapez le nombre du choix à sélectionner: ")

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
            print("Je n'ai pas compris votre choix.")
            self.main()
        print("")

    def manage_tournament(self):
        if not all_tournaments.tournaments:
            print("-----------")
            print("Il n'y a aucun tounoi en cours")
            print("")
            self.main()
        else:
            print("-----------")
            print("Quel tournoi souhaitez-vous modifier ?")
            print("")
            for i, tournament in enumerate(all_tournaments.tournaments):
                print(f"{i + 1}/ Le tournoi {tournament}")
            print(f"{len(all_tournaments.tournaments) + 1}/ Retour en arrière")
            selected_tournament = input("Tapez le numéro du tournoi à modifier: ")
            if Check.int_input(selected_tournament):
                selected_tournament = int(selected_tournament) - 1
            else:
                self.manage_tournament()

            if selected_tournament < 0:
                print("Je n'ai pas compris votre choix.")
                print(
                    f"Veuillez saisir un chiffre "
                    f"entre 1 et {len(all_tournaments.tournaments) + 1}."
                )
                self.manage_tournament()
            elif selected_tournament == len(all_tournaments.tournaments):
                self.main()
            elif selected_tournament > len(all_tournaments.tournaments):
                print("Je n'ai pas compris votre choix.")
                print(
                    f"Veuillez saisir un chiffre "
                    f"entre 1 et {len(all_tournaments.tournaments) + 1}."
                )
                self.manage_tournament()

            SelectedTournamentController.main(selected_tournament_self,
                                              all_tournaments.tournaments[selected_tournament])

    def show_tournaments(self):
        print("---------------")
        print(
            f"Il y a actuellement "
            f"{len(all_tournaments.tournaments)} tournoi(s) enregistré(s)."
        )
        for tournament in all_tournaments.tournaments:
            print("---------------")
            print(
                f"Nom: {tournament.name}, Lieu: {tournament.place}, "
                f"Date: {tournament.date}, "
                f"Contrôle du temps: {tournament.time_control}, "
                f"Nombre de tours: {tournament.number_of_rounds}"
            )
            print(
                f"Il y a actuellement {len(tournament.rounds)} tour(s) "
                "dans ce tournoi."
            )
            print("")
            SortPlayers.by_ranking(tournament)
        self.main()

    def add_tournament(self):
        name = input("Entrez le nom du tournoi: ")
        place = input("Entrez le lieu où se déroule le tournoi: ")

        if not all_tournaments.tournaments:
            tournament_id = 1
        else:
            tournament_id = len(all_tournaments.tournaments) + 1

        start_date = Check.date_format(input("Entrez la date de début de tournoi (format JJ/MM/AAAA): "))
        if not start_date:
            self.add_tournament()
        else:
            start_date = start_date.strftime("%d/%m/%Y")

        time_control_signature = TimeControl()
        time_control = TimeControl.selection(time_control_signature)
        number_of_rounds = input("Entrez le nombre de tours: ")

        if number_of_rounds == "":
            number_of_rounds = 4
        elif number_of_rounds == "0":
            print("Le nombre de tour ne peut pas être nul.")
            self.add_tournament()
        elif not Check.int_input(number_of_rounds):
            self.add_tournament()
        else:
            number_of_rounds = int(number_of_rounds)

        new_tournament = Tournament(
            tournament_id, name, place, start_date, time_control, number_of_rounds
        )
        description = input("Entrez la description du tournoi: ")
        new_tournament.description = description
        print("Tournoi bien créé")
        all_tournaments.add_tournament(new_tournament)
        crud_data.Data.save(all_tournaments.tournaments)
        self.main()

    def delete_tournament(self):
        if len(all_tournaments.tournaments) == 0:
            print("Il n'y a aucun tounoi en cours")
            self.main()
        else:
            for i, tournament in enumerate(all_tournaments.tournaments):
                print(f"{i + 1}/ Supprimer {tournament.name} ?")
            print(f"{len(all_tournaments.tournaments) + 1}/ Retour en arrière")
            choice = input("Tapez le numéro du tournoi à supprimer: ")

            if Check.int_input(choice):
                choice = int(choice) - 1
            else:
                self.delete_tournament()

            if choice >= len(all_tournaments.tournaments):
                print("Je n'ai pas compris votre choix.")
                print(
                    f"Veuillez saisir un chiffre compris "
                    f"entre 1 et {len(all_tournaments.tournaments) + 1}"
                )
                self.delete_tournament()

            tournament_to_delete = all_tournaments.tournaments[choice]
            if Check.deletion():
                all_tournaments.delete_tournament(tournament_to_delete)
                crud_data.Data.delete_tournament(tournament_to_delete.tournament_id)
                print(f"Le tournoi {tournament_to_delete.name} a bien été supprimé.")
                self.main()
            else:
                self.main()
