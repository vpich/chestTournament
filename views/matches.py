class MatchesView:
    @staticmethod
    def main(round_of_matches):
        print("Quel match souhaitez-vous gérer ?")
        for i, match in enumerate(round_of_matches.matches):
            print(f"{i + 1}/ {match}")
        print(f"{len(round_of_matches.matches) + 1}/ Retour en arrière")
        print("--------------")

        match_selected = input("Tapez le numéro du match à mettre à gérer: ")
        print("")
        return match_selected

    @staticmethod
    def match_selected(match):
        print("Que souhaitez-vous faire ?")
        print("")
        print(f"1/ Lancer un choix aléatoire pour définir "
              f"la couleur à jouer pour le joueur {match.contestants[0]}")
        print("2/ Mettre à jour le vainqueur de cette partie")
        print("3/ Retour en arrière")
        print("--------------")
        choice = input("Tapez le numéro souhaité pour sélectionner votre choix: ")
        print("")
        return choice

    @staticmethod
    def update_winner(match):
        print("Quel joueur a gagné ?")
        print("")
        print(f"1/ Le joueur {match.contestants[0]}")
        print(f"2/ Le joueur {match.contestants[1]}")
        print("3/ Il y a eu égalité.")
        print("4/ Retour en arrière")
        print("--------------")
        winner = input("Tapez le nombre du choix à sélectionner: ")
        print("")
        return winner

    @staticmethod
    def player_one_wins(match):
        print(
            f"{match.scores[0]} point ajouté "
            f"au joueur {match.contestants[0]}"
        )

    @staticmethod
    def player_two_wins(match):
        print(
            f"{match.scores[1]} point ajouté "
            f"au joueur {match.contestants[1]}"
        )

    @staticmethod
    def draw(match):
        print(f"{match.scores[0]} point ajouté aux 2 joueurs")

    @staticmethod
    def random_color(player, color):
        print(f"Le joueur {player} jouera le côté {color}")
