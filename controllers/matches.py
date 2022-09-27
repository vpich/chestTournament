from views import MatchesView
from .checks import Check
from .rand_black_or_white import RandomizeColor


class MatchesController:

    def main(self, tournament_round):
        MatchesView.matches(tournament_round)
        match_selected = input("Tapez le numéro du match à mettre à gérer: ")
        print("")
        if not Check.int_input(match_selected):
            print("Je n'ai pas compris votre choix.")
            self.main(tournament_round)
        else:
            match_selected = int(match_selected) - 1
            if match_selected < len(tournament_round.matches):
                self.match_selected(tournament_round.matches[match_selected])
                self.main(tournament_round)
            elif match_selected == len(tournament_round.matches):
                pass
            else:
                print("Je n'ai pas compris votre choix.")
                self.main(tournament_round)

    def match_selected(self, match):
        print("Que souhaitez-vous faire ?")
        print("")
        print(f"1/ Lancer un choix aléatoire pour définir "
              f"la couleur à jouer pour le joueur {match.contestants[0]}")
        print("2/ Mettre à jour le vainqueur de cette partie")
        print("3/ Retour en arrière")
        print("--------------")
        choice = input("Tapez le numéro souhaité pour sélectionner votre choix: ")
        print("")
        if not Check.int_input(choice):
            self.match_selected(match)
        else:
            choice = int(choice)
            if choice == 1:
                RandomizeColor.black_or_white(match.contestants[0])
                self.match_selected(match)
            elif choice == 2:
                self.update_winner(match)
            elif choice == 3:
                pass
            else:
                print("Je n'ai pas compris votre choix")
                self.match_selected(match)

    def update_winner(self, match):
        print("Quel joueur a gagné ?")
        print("")
        print(f"1/ Le joueur {match.contestants[0]}")
        print(f"2/ Le joueur {match.contestants[1]}")
        print("3/ Il y a eu égalité.")
        print("4/ Retour en arrière")
        print("--------------")
        winner = input("Tapez le nombre du choix à sélectionner: ")
        print("")
        if not Check.int_input(winner):
            print("Je n'ai pas comprix votre choix.")
            self.update_winner(match)
        else:
            winner = int(winner)
            if winner == 1:
                match.add_score_to_winner(match.contestants[0])
                print(
                    f"{match.scores[0]} point ajouté "
                    f"au joueur {match.contestants[0]}"
                )
            elif winner == 2:
                match.add_score_to_winner(match.contestants[1])
                print(
                    f"{match.scores[1]} point ajouté "
                    f"au joueur {match.contestants[1]}"
                )
            elif winner == 3:
                match.add_score_to_winner(None)
                print(f"{match.scores[0]} point ajouté aux 2 joueurs")
            elif winner == 4:
                pass
            else:
                print("Je n'ai pas compris votre choix.")
                self.update_winner(match)
