class TournamentsView:
    @staticmethod
    def main():
        print("--------------")
        print("Que souhaitez-vous faire ?")
        print("")
        print("1/ Créer un nouveau tournoi")
        print("2/ Afficher la liste des tournois")
        print("3/ Modifier un tournoi")
        print("4/ Supprimer un tournoi")
        print("5/ Réinitialiser le programme")
        print("6/ Quitter")

        choice = input("Tapez le nombre du choix à sélectionner: ")
        return choice

    @staticmethod
    def no_tournaments():
        print("-----------")
        print("Il n'y a aucun tournoi en cours")
        print("")

    @staticmethod
    def manage(all_tournaments):
        print("-----------")
        print("Quel tournoi souhaitez-vous modifier ?")
        print("")
        for i, tournament in enumerate(all_tournaments.tournaments):
            print(f"{i + 1}/ Le tournoi {tournament}")
        print(f"{len(all_tournaments.tournaments) + 1}/ Retour en arrière")
        selected_tournament = input("Tapez le numéro du tournoi à modifier: ")
        return selected_tournament

    @staticmethod
    def show(all_tournaments):
        print("---------------")
        print(
            f"Il y a actuellement "
            f"{len(all_tournaments.tournaments)} tournoi(s) enregistré(s)."
        )

    @staticmethod
    def show_each_tournament(tournament):
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

    @staticmethod
    def add():
        name = input("Entrez le nom du tournoi: ")
        place = input("Entrez le lieu où se déroule le tournoi: ")
        start_date = input("Entrez la date de début de tournoi (format JJ/MM/AAAA): ")
        number_of_rounds = input("Entrez le nombre de tours: ")
        description = input("Entrez la description du tournoi: ")

        return {
            "name": name,
            "place": place,
            "start_date": start_date,
            "number_of_rounds": number_of_rounds,
            "description": description
        }

    @staticmethod
    def number_of_round_not_null():
        print("Le nombre de tour ne peut pas être nul.")

    @staticmethod
    def add_success():
        print("Tournoi bien créé")

    @staticmethod
    def delete(all_tournaments):
        for i, tournament in enumerate(all_tournaments.tournaments):
            print(f"{i + 1}/ Supprimer {tournament.name} ?")
        print(f"{len(all_tournaments.tournaments) + 1}/ Retour en arrière")
        choice = input("Tapez le numéro du tournoi à supprimer: ")
        return choice

    @staticmethod
    def delete_success(tournament_to_delete):
        print(f"Le tournoi {tournament_to_delete.name} a bien été supprimé.")

