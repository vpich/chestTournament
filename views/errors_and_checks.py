class ErrorsViews:
    @staticmethod
    def number_required():
        print("Veuillez saisir un chiffre pour sélectionner votre choix.")

    @staticmethod
    def wrong_date_format():
        print("Format de date invalide. Format demandé: JJ/MM/AAAA")

    @staticmethod
    def unknown_choice():
        print("Je n'ai pas compris votre choix.")


class ChecksViews:
    @staticmethod
    def deletion():
        print("Toute suppression est irréversible.")
        choice = input("Souhaitez-vous vraiment effectuer la suppression ? (y/n)")
        return choice
