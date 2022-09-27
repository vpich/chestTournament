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
    def unknown_choice():
        print("Je n'ai pas compris votre choix")
