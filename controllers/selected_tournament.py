from views import selected_tournament_view
from .checks import check_int_input
from .ranking import ranking_controller
from .players import players_controller
from .rounds import rounds_controller
from .tournaments import edit_tournament_controller, tournaments_controller


def selected_tournament_controller(tournament):
    selected_tournament_view()
    choice = input("Tapez 1, 2 ou 3: ")

    if check_int_input(choice):
        choice = int(choice)
    else:
        selected_tournament_controller(tournament)

    if choice == 1:
        edit_tournament_controller(tournament)
    elif choice == 2:
        players_controller(tournament)
    elif choice == 3:
        rounds_controller(tournament)
    elif choice == 4:
        ranking_controller(tournament)
        selected_tournament_controller(tournament)
    elif choice == 5:
        tournaments_controller()
    else:
        print("Je n'ai pas compris votre choix.")
        selected_tournament_controller(tournament)
    print("-----------------")
