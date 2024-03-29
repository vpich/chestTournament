from datetime import date


class Player:
    def __init__(self, player_id, firstname, lastname,
                 date_of_birth: date, gender, rank: int = 0):
        self.player_id = player_id
        self.firstname = firstname
        self.lastname = lastname
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.rank = rank
        self.total_points = 0

    def __str__(self):
        return f"{self.firstname} {self.lastname}"
