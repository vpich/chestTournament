from datetime import datetime


class Round:
    def __init__(self, name):
        self.name = name
        self.matches = []

        self.start_time = None
        self.end_time = None

    def __str__(self):
        return f"{self.name}"

    def add_match(self, match):
        self.matches.append(match)

    def starting(self):
        self.start_time = datetime.now()

    def ending(self):
        self.end_time = datetime.now()
