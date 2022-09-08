from datetime import datetime

from models import AllTournaments, Tournament
from views import tournaments_view
from .checks import check_int_input, check_date_format, check_deletion
from .ranking import ranking_controller
from . import crud_data
# from .crud_data import save_data, load_data, delete_data
from .selected_tournament import selected_tournament_controller
from .time_control import time_control_selection

all_tournaments = AllTournaments()


def tournaments_controller():
    tournaments_view()
    choice = input("Tapez le nombre du choix à sélectionner: ")

    if check_int_input(choice):
        choice = int(choice)
    else:
        tournaments_controller()

    if choice == 1:
        add_tournament_controller()
    elif choice == 2:
        show_tournaments_controller()
    elif choice == 3:
        manage_tournament_controller()
    elif choice == 4:
        delete_tournament_controller()
    elif choice == 5:
        crud_data.delete_data()
    elif choice == 6:
        print("Vous quittez le programme.")
        exit()
    elif choice == 7:
        crud_data.save_data(all_tournaments.tournaments)
    elif choice == 8:
        crud_data.load_data()
    else:
        print("Je n'ai pas compris votre choix.")
        tournaments_controller()
    print("-----------------")


def manage_tournament_controller():
    if not all_tournaments.tournaments:
        print("Il n'y a aucun tounoi en cours")
        tournaments_controller()
    else:
        print("Quel tournoi souhaitez-vous modifier ?")
        for i, tournament in enumerate(all_tournaments.tournaments):
            print(f"{i + 1}/ Le tournoi {tournament}")
        print(f"{len(all_tournaments.tournaments) + 1}/ Retour en arrière")
        selected_tournament = input("Tapez le numéro du tournoi à modifier: ")
        if check_int_input(selected_tournament):
            selected_tournament = int(selected_tournament) - 1
        else:
            manage_tournament_controller()

        if selected_tournament < 0:
            print("Je n'ai pas compris votre choix.")
            print(
                f"Veuillez saisir un chiffre "
                f"entre 1 et {len(all_tournaments.tournaments) + 1}."
            )
            manage_tournament_controller()
        elif selected_tournament == len(all_tournaments.tournaments):
            tournaments_controller()
        elif selected_tournament > len(all_tournaments.tournaments):
            print("Je n'ai pas compris votre choix.")
            print(
                f"Veuillez saisir un chiffre "
                f"entre 1 et {len(all_tournaments.tournaments) + 1}."
            )
            manage_tournament_controller()

        selected_tournament_controller(all_tournaments.tournaments[selected_tournament])


def show_tournaments_controller():
    print("---------------")
    print(
        f"Il y a actuellement "
        f"{len(all_tournaments.tournaments)} tournoi(s) enregistré(s)."
    )
    print("---------------")
    for tournament in all_tournaments.tournaments:
        ranking_controller(tournament)
    tournaments_controller()


def add_tournament_controller():
    print("****************************")
    print("Un nouveau tournoi va commencer aujourd'hui")
    name = input("Entrez le nom du tournoi: ")
    place = input("Entrez le lieu où se déroule le tournoi: ")

    if not all_tournaments.tournaments:
        tournament_id = 1
    else:
        tournament_id = len(all_tournaments.tournaments)

    end_date = check_date_format(input("Entrez la date de fin de tournoi: "))
    today = datetime.date(datetime.now())
    if not end_date:
        add_tournament_controller()
    if end_date < today:
        print("La date ne peut pas être antérieure à aujourd'hui.")
        add_tournament_controller()
    else:
        date = f"Du {today.strftime('%d/%m/%Y')} " f"au {end_date.strftime('%d/%m/%Y')}"

    time_control = time_control_selection()
    number_of_rounds = input("Entrez le nombre de tours: ")

    if number_of_rounds == "":
        number_of_rounds = 4
    elif number_of_rounds == "0":
        print("Le nombre de tour ne peut pas être nul.")
        add_tournament_controller()
    elif not check_int_input(number_of_rounds):
        add_tournament_controller()
    else:
        number_of_rounds = int(number_of_rounds)

    new_tournament = Tournament(
        tournament_id, name, place, date, time_control, number_of_rounds
    )
    description = input("Entrez la description du tournoi: ")
    new_tournament.description = description
    print(f"{date}")
    print("Tournoi bien créé")
    all_tournaments.add_tournament(new_tournament)
    # save_data(all_tournaments.tournaments)
    print("*****************************")
    tournaments_controller()


def delete_tournament_controller():
    if len(all_tournaments.tournaments) == 0:
        print("Il n'y a aucun tounoi en cours")
        tournaments_controller()
    else:
        for i, tournament in enumerate(all_tournaments.tournaments):
            print(f"{i + 1}/ Supprimer {tournament.name} ?")
        print(f"{len(all_tournaments.tournaments) + 1}/ Retour en arrière")
        choice = input("Tapez le numéro du tournoi à supprimer: ")

        if check_int_input(choice):
            choice = int(choice) - 1
        else:
            delete_tournament_controller()

        if choice > len(all_tournaments.tournaments):
            print("Je n'ai pas compris votre choix.")
            print(
                f"Veuillez saisir un chiffre compris "
                f"entre 1 et {len(all_tournaments.tournaments)}"
            )
            delete_tournament_controller()

        if choice == len(all_tournaments.tournaments):
            tournaments_controller()

        tournament_to_delete = all_tournaments.tournaments[choice]
        if check_deletion():
            all_tournaments.delete_tournament(tournament_to_delete)
            # save_data(all_tournaments.tournaments)
            print(f"Le tournoi {tournament_to_delete.name} a bien été supprimé.")
            tournaments_controller()
        else:
            tournaments_controller()
