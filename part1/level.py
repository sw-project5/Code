def get_level_from_score(score):
    if 0 <= score <= 9:
        level = "Iron"
        print_score = score
    elif 10 <= score <= 19:
        level = "Bronze"
        print_score = score
    elif 20 <= score <= 29:
        level = "Silver"
        print_score = score
    elif 30 <= score <= 39:
        level = "Gold"
        print_score = score
    elif 40 <= score <= 49:
        level = "Platinum"
        print_score = score
    elif score == 50:
        # score-=1
        level = "Platinum"
        print_score = score
    return level, print_score