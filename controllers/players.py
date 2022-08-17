from controllers import check_int_input, check_date_format
from views import players_view
from models import Player


def players_controller(tournament):
    print("---Début player controller")
    players_view(tournament)
    choice = input("Tapez 1, 2, 3 ou 4: ")

    if check_int_input(choice):
        choice = int(choice)
    else:
        players_controller(tournament)

    if choice == 1:
        # il faut 8 joueurs
        add_player_controller(tournament)
    elif choice == 2:
        edit_player_controller(tournament)
    elif choice == 3:
        delete_player_controller(tournament)
    elif choice == 4:
        selected_tournament_controller(tournament)
    else:
        print("Je n'ai pas compris votre choix")
        players_controller(tournament)


def add_player_controller(tournament):
    firstname = input("Entrez le prénom du joueur: ")
    lastname = input("Entrez le nom de famille du joueur: ")
    date_of_birth = check_date_format(
        input("Entrez la date de naissance du joueur (format JJ/MM/AAAA): ")
    )
    gender = input("Entrez le sexe du joueur: ")
    new_player = Player(firstname, lastname, date_of_birth, gender)
    tournament.players.append(new_player)
    print(f"Le joueur {firstname} {lastname} a bien été ajouté au tournoi.")
    players_controller(tournament)


def edit_player_controller(tournament):
    for i, player in enumerate(tournament.players):
        print(f"{i + 1}/ Modifier {player}")
    choice = input("Tapez le numéro du joueur à modifier: ")

    if check_int_input(choice):
        choice = int(choice) - 1
    else:
        edit_player_controller(tournament)

    if choice > len(tournament.players):
        print("Je n'ai pas compris votre choix.")
        print(f"Veuillez saisir un chiffre compris entre 1 et {len(tournament.players)}")
        edit_player_controller(tournament)

    player_to_modify = tournament.players[choice]
    print("Que souhaitez-vous modifier ?")
    print("1/ Son prénom ?")
    print("2/ Son nom de famille ?")
    print("3/ Sa date de naissance ?")
    print("4/ Son sexe ?")
    print("5/ Son score ?")
    choice = int(input("Tapez le numéro à modifier: "))
    if choice == 1:
        firstname = input("Entrez le prénom du joueur: ")
        player_to_modify.firstname = firstname
    elif choice == 2:
        lastname = input("Entrez le nom de famille du joueur: ")
        player_to_modify.lastname = lastname
    elif choice == 3:
        date_of_birth = check_date_format(
            input("Entrez la date de naissance du joueur: ")
        )
        player_to_modify.date_of_birth = date_of_birth
    elif choice == 4:
        gender = input("Entrez le sexe du joueur: ")
        player_to_modify.gender = gender
    elif choice == 5:
        rank = int(input("Entrez le score du joueur: "))
        player_to_modify.rank = rank
    else:
        return
    print("La modification a été enregistrée.")
    players_controller(tournament)


def delete_player_controller(tournament):
    for i, player in enumerate(tournament.players):
        print(f"{i + 1}/ Supprimer {player} ?")
    choice = input("Tapez le numéro du joueur à supprimer: ")

    if check_int_input(choice):
        choice = int(choice) - 1
    else:
        delete_player_controller(tournament)

    if choice > tournament.players:
        print("Je n'ai pas compris votre choix.")
        print(f"Veuillez saisir un chiffre compris entre 1 et {len(tournament.players)}")
        delete_player_controller(tournament)

    player_to_delete = tournament.players[choice]
    tournament.delete_player(player_to_delete)
    print(
        f"Le joueur {player_to_delete.firstname} {player_to_delete.lastname} a bien été supprimé."
    )
    players_controller(tournament)
