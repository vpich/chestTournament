class TimeControlView:
    @staticmethod
    def main(time_control_choices):
        print("Quel type de contrôle de temps souhaitez-vous ?")
        for i, choice in enumerate(time_control_choices):
            print(f"{i + 1}/ {choice}")

        user_choice = input("Entrez le numéro du choix à selectionner: ")
        return user_choice
