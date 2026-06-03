# Simulated weekly recovery scores
weekly_scores = [82, 65, 71, 45, 88, 55, 78]

for score in weekly_scores:
    if score >= 80:
        print(score, "→ Green day")
    elif score >= 60:
        print(score, "→ Yellow day")
    else:
        print(score, "→ Red day")