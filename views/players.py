class PlayersView:

    @staticmethod
    def main(tournament):
        print("--------------")
        print(f"Liste des {len(tournament.players)} participants du tournoi {tournament}: ")
        for player in tournament.players:
            print(player)
        print("--------------")
        print("Que souhaitez-vous faire ?")
        print("")
        print("1/ Rajouter un joueur")
        print("2/ Modifier les informations d'un joueur")
        print("3/ Supprimer un joueur")
        print("4/ Afficher le classement des joueurs")
        print("5/ Afficher les joueurs triés par noms de famille")
        print("6/ Retour en arrière")

        choice = input("Tapez le nombre du choix à sélectionner: ")
        return choice

    @staticmethod
    def add_player():
        firstname = input("Entrez le prénom du joueur: ")
        lastname = input("Entrez le nom de famille du joueur: ")
        date_of_birth = input("Entrez la date de naissance du joueur " "(format JJ/MM/AAAA): ")

        gender = input("Entrez le sexe du joueur: ")
        rank = input("Entrez le rang du joueur: ")

        return {
            "firstname": firstname,
            "lastname": lastname,
            "date_of_birth": date_of_birth,
            "gender": gender,
            "rank": rank
        }

    @staticmethod
    def add_player_success(player):
        print(f'Le joueur {player["firstname"]} {player["lastname"]} '
              f'a bien été ajouté au tournoi.')

    @staticmethod
    def no_player():
        print("--------------")
        print("Il n'y a aucun joueur d'enregistrés.")
        print("")

    @staticmethod
    def max_players():
        print("Vous avez atteint le nombre maximal de 8 joueurs.")

    @staticmethod
    def unknown_choice():
        print("Je n'ai pas compris votre choix")

    @staticmethod
    def edit_player_selection(tournament):
        print("--------------")
        print("Pour quel joueur souhaitez-vous modifier les informations ?")
        print("")
        for i, player in enumerate(tournament.players):
            print(f"{i + 1}/ Modifier le joueur {player}")
        choice = input("Tapez le numéro du joueur à modifier: ")
        return choice

    @staticmethod
    def edit_player_choices(player):
        print("--------------")
        print(f"Vous allez éditer les informations de {player}")
        print("Que souhaitez-vous modifier ?")
        print("")
        print("1/ Son prénom")
        print("2/ Son nom de famille")
        print("3/ Sa date de naissance")
        print("4/ Son sexe")
        print("5/ Son score")
        print("6/ Retour en arrière")
        choice = int(input("Tapez le numéro à modifier: "))
        return choice

    @staticmethod
    def edit_player(choice):
        if choice == 1:
            firstname = input("Entrez le prénom du joueur: ")
            return firstname
        elif choice == 2:
            lastname = input("Entrez le nom de famille du joueur: ")
            return lastname
        elif choice == 3:
            date_of_birth = input("Entrez la date de naissance du joueur: ")
            return date_of_birth
        elif choice == 4:
            gender = input("Entrez le sexe du joueur: ")
            return gender
        elif choice == 5:
            rank = input("Entrez le score du joueur: ")
            return rank

    @staticmethod
    def edit_player_success():
        print("La modification a été enregistrée.")

    @staticmethod
    def delete_player(tournament):
        print("--------------")
        print("Quel joueur souhaitez-vous supprimer du tournoi ?")
        print("")
        for i, player in enumerate(tournament.players):
            print(f"{i + 1}/ Supprimer {player} ?")
        print(f"{len(tournament.players) + 1}/ Retour en arrière")
        choice = input("Tapez le numéro du joueur à supprimer: ")
        return choice

    @staticmethod
    def delete_player_success(player):
        print(f"Le joueur {player} a bien été supprimé.")
