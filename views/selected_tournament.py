class SelectedTournamentView:
    @staticmethod
    def main(tournament_name):
        print("--------------")
        print(f"Menu de gestion du tournoi {tournament_name}")
        print("Que souhaitez-vous faire ?")
        print("")
        print("1/ Modifier les informations du tournoi")
        print("2/ Gérer les joueurs")
        print("3/ Gérer les rounds")
        print("4/ Retour en arrière")

        choice = input("Tapez le numéro du choix à sélectionner: ")
        return choice

    @staticmethod
    def edit(tournament):
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
        return choice

    @staticmethod
    def edit_choice(choice):
        if choice == 1:
            name = input("Entrez le nom du tournoi: ")
            return name
        elif choice == 2:
            place = input("Entrez le lieu: ")
            return place
        elif choice == 3:
            start_date = input("Entrez la date de début de tournoi: ")
            return start_date
        elif choice == 5:
            user_input = input("Entrez le nombre de tours: ")
            return user_input

    @staticmethod
    def edit_success(tournament):
        print(f"Le tournoi {tournament} a bien été modifié.")
