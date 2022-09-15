import random


def random_black_or_white(player):
    choices = ["noir", "blanc"]
    color = random.choice(choices)
    print(f"Le joueur {player} jouera le côté {color}")
