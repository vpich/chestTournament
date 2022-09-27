class MatchesView:
    @staticmethod
    def matches(round_of_matches):
        print("Quel match souhaitez-vous gérer ?")
        for i, match in enumerate(round_of_matches.matches):
            print(f"{i + 1}/ {match}")
        print(f"{len(round_of_matches.matches) + 1}/ Retour en arrière")
        print("--------------")
