from datetime import datetime

from models import AllTournaments, Tournament
from views import tournaments_view
from .checks import check_int_input, check_date_format
from .ranking import ranking_controller
from .crud_data import save_data, load_data, delete_data

all_tournaments = AllTournaments()


def tournaments_controller():
    tournaments_view()
    choice = input("Tapez 1, 2, 3, 4 ou 5: ")

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
        save_data(all_tournaments.tournaments)
    elif choice == 6:
        load_data()
    elif choice == 7:
        delete_data()
    elif choice == 8:
        print("Vous quittez le programme.")
        exit()
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
            print(f"{i + 1}/ Le {tournament} ?")
        selected_tournament = input("Tapez le numéro du tournoi à modifier: ")
        if check_int_input(selected_tournament):
            selected_tournament = int(selected_tournament) - 1
        else:
            manage_tournament_controller()

        if selected_tournament < 0:
            print("Je n'ai pas compris votre choix.")
            print(
                f"Veuillez saisir un chiffre "
                f"entre 1 et {len(all_tournaments.tournaments)}."
            )
            manage_tournament_controller()
        elif selected_tournament >= len(all_tournaments.tournaments):
            print("Je n'ai pas compris votre choix.")
            print(
                f"Veuillez saisir un chiffre "
                f"entre 1 et {len(all_tournaments.tournaments)}."
            )
            manage_tournament_controller()

        selected_tournament_controller(all_tournaments.tournaments[selected_tournament])


def show_tournaments_controller():
    print(
        f"Il y a actuellement "
        f"{len(all_tournaments.tournaments)} tournoi(s) enregistré(s)."
    )
    for tournament in all_tournaments.tournaments:
        ranking_controller(tournament)
    tournaments_controller()


def time_control_selection():
    time_control_choices = ["Bullet", "Blitz", "Coup rapide"]
    print("Quel type de contrôle de temps souhaitez-vous ?")
    for i, choice in enumerate(time_control_choices):
        print(f"{i + 1}/ {choice}")

    user_choice = input("Entrez le numéro du choix à selectionner: ")

    if not check_int_input(user_choice):
        time_control_selection()
    else:
        user_choice = int(user_choice)
        if user_choice > 3:
            print("Je n'ai pas compris votre choix.")
            time_control_selection()
        elif user_choice == 1:
            return time_control_choices[0]
        elif user_choice == 2:
            return time_control_choices[1]
        elif user_choice == 3:
            return time_control_choices[2]
        else:
            print(
                "Je n'ai pas compris votre choix. "
                "Veuillez taper un nombre entre 1 et 3."
            )
            time_control_selection()


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
    print("*****************************")
    tournaments_controller()


def delete_tournament_controller():
    if len(all_tournaments.tournaments) == 0:
        print("Il n'y a aucun tounoi en cours")
        tournaments_controller()
    else:
        for i, tournament in enumerate(all_tournaments.tournaments):
            print(f"{i + 1}/ Supprimer {tournament.name} ?")
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

        tournament_to_delete = all_tournaments.tournaments[choice]
        all_tournaments.delete_tournament(tournament_to_delete)
        print(f"Le tournoi {tournament_to_delete.name} a bien été supprimé.")
        tournaments_controller()


def edit_tournament_controller(tournament):
    print(
        f"Nom: {tournament.name}, Lieu: {tournament.place}, "
        f"Date(s): {tournament.date}, "
        f"Contrôle du temps: {tournament.time_control}, "
        f"Nombre de tours: {tournament.number_of_rounds}"
    )
    print("Que souhaitez-vous modifier ?")
    print("1/ Le nom ?")
    print("2/ Le lieu ?")
    print("3/ Les dates ?")
    print("4/ Le contrôle du temps ?")
    print("5/ Le nombre de tours ?")
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
                edit_tournament_controller(tournament)
            if end_date < today:
                print("La date ne peut pas être antérieure à aujourd'hui.")
                edit_tournament_controller(tournament)
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
                edit_tournament_controller(tournament)
        elif choice == 6:
            selected_tournament_controller(tournament)
        else:
            print("Je n'ai pas compris votre choix.")
            edit_tournament_controller(tournament)
        selected_tournament_controller(tournament)
    else:
        print("Je n'ai pas compris votre choix.")
        edit_tournament_controller(tournament)
