from datetime import datetime


class Checks:

    @staticmethod
    def check_int_input(self, user_input):
        if user_input.isdigit():
            return True
        else:
            print("Je n'ai pas compris votre choix.")
            print("Veuillez saisir un chiffre pour sélectionner votre choix.")
            return False

    @staticmethod
    def check_date_format(self, user_input):
        try:
            date_to_check = datetime.strptime(user_input, "%d/%m/%Y")
            return datetime.date(date_to_check)
        except ValueError:
            print("Format de date invalide. Format demandé: JJ/MM/AAAA")
            return False

    @staticmethod
    def check_deletion(self):
        print("Toute suppression est irréversible.")
        choice = input("Souhaitez-vous vraiment effectuer la suppression ? (y/n)")
        if choice == "y":
            return True
        elif choice == "n":
            return False
        else:
            print("Je n'ai pas compris votre choix.")
            self.check_deletion()
