from controllers import check_int_input


def time_control_selection():
    time_control_choices = ["Bullet", "Blitz", "Coup rapide"]
    print("Quel type de contrôle de temps souhaitez-vous ?")
    for i, choice in enumerate(time_control_choices):
        print(f"{i + 1}/ {choice}")

    user_choice = input("Entrez le numéro du choix à selectionner: ")

    if not check_int_input(user_choice):
        time_control_selection()
    else:
        user_choice = int(user_choice)
        if user_choice > 3:
            print("Je n'ai pas compris votre choix.")
            time_control_selection()
        elif user_choice == 1:
            return time_control_choices[0]
        elif user_choice == 2:
            return time_control_choices[1]
        elif user_choice == 3:
            return time_control_choices[2]
        else:
            print(
                "Je n'ai pas compris votre choix. "
                "Veuillez taper un nombre entre 1 et 3."
            )
            time_control_selection()
