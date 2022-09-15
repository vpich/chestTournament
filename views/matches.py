def matches_view(round):
    print("Quel match souhaitez-vous gérer ?")
    for i, match in enumerate(round.matches):
        print(f"{i + 1}/ {match}")
    print("--------------")
