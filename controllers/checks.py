from datetime import datetime


def check_int_input(user_input):
    if user_input.isdigit():
        return True
    else:
        print("Je n'ai pas compris votre choix.")
        print("Veuillez saisir un chiffre pour sélectionner votre choix.")
        return False


def check_date_format(user_input):
    try:
        date_to_check = datetime.strptime(user_input, "%d/%m/%Y")
        return datetime.date(date_to_check)
    except ValueError:
        print("Format de date invalide.")
        return False


def check_deletion():
    print("Toute suppression est irréversible.")
    choice = input("Souhaitez-vous vraiment effectuer la suppression ? (y/n)")
    if choice == "y":
        return True
    elif choice == "n":
        return False
    else:
        print("Je n'ai pas compris votre choix.")
        check_deletion()
