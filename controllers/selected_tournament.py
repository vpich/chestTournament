from datetime import datetime

from views import selected_tournament_view
from .checks import check_int_input, check_date_format
from .ranking import ranking_controller
from . import players
# from .players import players_controller
from .rounds import rounds_controller
from .time_control import time_control_selection
from . import tournaments


# from .tournaments import tournaments_controller


def selected_tournament_controller(tournament):
    selected_tournament_view()
    choice = input("Tapez le numéro du choix à sélectionner: ")

    if check_int_input(choice):
        choice = int(choice)
    else:
        selected_tournament_controller(tournament)

    if choice == 1:
        edit_selected_tournament_controller(tournament)
    elif choice == 2:
        players.players_controller(tournament)
    elif choice == 3:
        rounds_controller(tournament)
    elif choice == 4:
        ranking_controller(tournament)
        selected_tournament_controller(tournament)
    elif choice == 5:
        tournaments.tournaments_controller()
    else:
        print("Je n'ai pas compris votre choix.")
        selected_tournament_controller(tournament)
    print("-----------------")


def edit_selected_tournament_controller(tournament):
    print(
        f"Nom: {tournament.name}, Lieu: {tournament.place}, "
        f"Date(s): {tournament.date}, "
        f"Contrôle du temps: {tournament.time_control}, "
        f"Nombre de tours: {tournament.number_of_rounds}"
    )
    print("Que souhaitez-vous modifier ?")
    print("1/ Le nom")
    print("2/ Le lieu")
    print("3/ Les dates")
    print("4/ Le contrôle du temps")
    print("5/ Le nombre de tours")
    print("6/ Retour en arrière")
    choice = input("Taper un chiffre entre 1 et 6: ")
    if check_int_input(choice):
        choice = int(choice)
        if choice == 1:
            name = input("Entrez le nom du tournoi: ")
            tournament.name = name
        elif choice == 2:
            place = input("Entrez le lieu: ")
            tournament.place = place
        elif choice == 3:
            end_date = check_date_format(input("Entrez la date de fin de tournoi: "))
            today = datetime.date(datetime.now())
            if not end_date:
                edit_selected_tournament_controller(tournament)
            if end_date < today:
                print("La date ne peut pas être antérieure à aujourd'hui.")
                edit_selected_tournament_controller(tournament)
            else:
                date = (
                    f"Du {today.strftime('%d/%m/%Y')} "
                    f"au {end_date.strftime('%d/%m/%Y')}"
                )
            tournament.date = date
        elif choice == 4:
            time_control = time_control_selection()
            tournament.time_control = time_control
        elif choice == 5:
            user_input = input("Entrez le nombre de tours: ")
            if check_int_input(user_input):
                number_of_rounds = int(user_input)
                tournament.number_of_rounds = number_of_rounds
            else:
                print("Saisie invalide. Veuillez rentrer un chiffre entier.")
                edit_selected_tournament_controller(tournament)
        elif choice == 6:
            selected_tournament_controller(tournament)
        else:
            print("Je n'ai pas compris votre choix.")
            edit_selected_tournament_controller(tournament)
        # save_data(all_tournaments.tournaments)
        selected_tournament_controller(tournament)
