from datetime import date


class Player:
    def __init__(self, firstname, lastname, date_of_birth: date, gender, rank: int = 0):
        self.firstname = firstname
        self.lastname = lastname
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.rank = rank
        self.points_gagnes = 0
        # a la fin de chaque match,

    def __str__(self):
        return f"Joueur {self.firstname} {self.lastname}, classement: {self.rank}"
