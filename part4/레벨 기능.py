def get_level_from_score(score,print_score):
    if 0 <= score <= 9:
        level = "Iron"
        print_score = score
    elif 10 <= score <= 19:
        level = "Bronze"
        print_score = score-10
    elif 20 <= score <= 29:
        level = "Silver"
        print_score = score-20
    elif 30 <= score <= 39:
        level = "Gold"
        print_score = score-30
    elif 40 <= score <= 49:
        level = "Platinum"
        print_score = score-40
    elif score == 50:
        score-=1
        level = "Platinum"
        print_score = score-40



    level_text = f"맞은 문제의 수: {correct_count} \n당신의 레벨은\n'{level}'입니다.\n점수는 '{print_score}'입니다."
    level_label = Label(window, text=level_text, font=("HanSans", 13), bg=BGCOLOR)
    level_label.pack()

