from datetime import datetime

from models import AllTournaments, Tournament
from views import tournaments_view, selected_tournament_view
from controllers import check_int_input, check_date_format, ranking_controller, players_controller

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
        edit_tournament_controller()
    elif choice == 4:
        delete_tournament_controller()
    elif choice == 5:
        print("Vous quittez le programme.")
        exit()
    else:
        print("Je n'ai pas compris votre choix.")
        tournaments_controller()
    print("-----------------")


def edit_tournament_controller():
    #     print la liste des tournois avec chacun un numéro
    if len(all_tournaments.tournaments) == 0:
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
            edit_tournament_controller()

        if selected_tournament < 0:
            print("Je n'ai pas compris votre choix.")
            print(f"Veuillez saisir un chiffre entre 1 et {len(all_tournaments.tournaments)}.")
            edit_tournament_controller()
        elif selected_tournament >= len(all_tournaments.tournaments):
            print("Je n'ai pas compris votre choix.")
            print(f"Veuillez saisir un chiffre entre 1 et {len(all_tournaments.tournaments)}.")
            edit_tournament_controller()

        selected_tournament_controller(all_tournaments.tournaments[selected_tournament])


def show_tournaments_controller():
    #     faire comme les joueurs: print la liste des tournois
    #     avec chacun un numéro et pour celui sélectionné print toutes les infos du tournoi
    print(f"Il y a actuellement {len(all_tournaments.tournaments)} tournoi(s) enregistré(s).")
    for tournament in all_tournaments.tournaments:
        ranking_controller(tournament)
    # print("Pour quel tournoi souhaitez-vous éditer un rapport ?")
    # for i, tournament in enumerate(all_tournaments.tournaments):
    #     print(f"{i + 1}/ Le {tournament} ?")
    # selected_tournament = int(input("Tapez le numéro du tournoi choisi: ")) - 1
    # print(f"Vous avez choisi le tournoi {all_tournaments.tournaments[selected_tournament].name}")
    # ranking_view(all_tournaments.tournaments[selected_tournament])
    tournaments_controller()


def add_tournament_controller():
    print("****************************")
    print("Un nouveau tournoi va commencer !")
    # name = input("Entrez le nom du tournoi: ")
    # place = input("Entrez le lieu où se déroule le tournoi: ")
    end_date = check_date_format(input("Entrez la date de fin de tournoi: "))
    # time_control = input("Entrez le type de contrôle de temps (bullet, blitz ou coup rapide): ")
    # number_of_rounds = int(input("Entrez le nombre de tours: "))
    # new_tournament = Tournament(name, place, date, time_control, number_of_rounds)
    today = datetime.date(datetime.now())
    if end_date < today:
        raise print("La date ne peut pas être antérieure à aujourd'hui.")
    else:
        date = f"Du {today.strftime('%d/%m/%Y')} au {end_date.strftime('%d/%m/%Y')}"
    new_tournament = Tournament("name", "place", date, "time_control", 4)
    # description = input("Entrez la description du tournoi: ")
    # new_tournament.description = description
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
            print(f"Veuillez saisir un chiffre compris entre 1 et {len(all_tournaments.tournaments)}")
            delete_tournament_controller()

        tournament_to_delete = all_tournaments.tournaments[choice]
        all_tournaments.delete_tournament(tournament_to_delete)
        print(
            f"Le tournoi {tournament_to_delete.name} a bien été supprimé."
        )
        tournaments_controller()


def selected_tournament_controller(tournament):
    selected_tournament_view()
    choice = input("Tapez 1, 2 ou 3: ")

    if check_int_input(choice):
        choice = int(choice)
    else:
        selected_tournament_controller(tournament)

    if choice == 1:
        players_controller(tournament)
    elif choice == 2:
        rounds_controller(tournament)
    elif choice == 3:
        ranking_controller(tournament)
        selected_tournament_controller(tournament)
    elif choice == 4:
        tournaments_controller()
    else:
        print("Je n'ai pas compris votre choix.")
        selected_tournament_controller(tournament)
    print("-----------------")
