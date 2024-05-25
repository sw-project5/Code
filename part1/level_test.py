from tkinter import *
import tkinter
import random
import json
from wordDB import words  # 단어 데이터베이스 임포트
from level import get_level_from_score

# 각 딕셔너리의 key와 value 이름 설정
new_key_name = "english_word"
new_value_name = "korean_meaning"

# 새로운 형식의 딕셔너리 리스트 생성
new_questions = [{new_key_name: key, new_value_name: value} for item in words for key, value in item.items()]

# 색깔 상수들 정의
BTN_COLOR = "#F0F0F0"   # 버튼 배경색
PROGRESS_COLOR = "#2ECC71"  # 진행 바 색

# 정답 번호를 담을 변수 초기화
answer = 0
total_questions = 20  # 총 문제 수
correct_count = 0  # 맞은 문제 수
wrong_count = 0  # 틀린 문제 수
level = ""
score = 0
current_question = 0  # 현재 진행 중인 문제 수

# Tkinter 창과 위젯 전역 변수 선언
window = None
question_label = None
progress_label = None
progress_canvas = None
buttons = []
entry = None
check_btn = None
current_user = None

# 사용자 데이터 로드 및 업데이트
def load_user_data(filepath='users.json'):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []
    
def save_user_data(users, filepath='users.json'):
    if not isinstance(users, list):
        raise ValueError("The data to be saved must be a list.")
    
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(users, file, ensure_ascii=False, indent=4)

def update_user_data(users, current_user, level, score):
    for user in users:
        if user["username"] == current_user["username"]:
            user["level"] = level
            user["score"] = score
            break

def open_wordleveltest_window(user):
    global window, question_label, progress_label, progress_canvas, current_user
    
    current_user = user
    
    # Tkinter 창 생성
    window = Tk()
    window.title("영어 퀴즈")
    window.geometry("450x500+100+100")
    window.resizable(False, False)

    # 사용자의 수준을 알아보기 위한 텍스트
    level_text = Label(window, text="사용자의 수준을 알아보기 위해 레벨 테스트를 진행하겠습니다.",
                       font=("맑은 고딕", 13))
    level_text.pack()

    # 문제 표시 레이블 생성
    question_label = Label(window, width=30, height=4,
                           text="test", font=("맑은 고딕", 20, "bold"), fg="black")
    question_label.pack()

    # 진행 상황 표시 레이블 생성
    progress_label = Label(window, text=f"{current_question}/{total_questions}",
                           font=("맑은 고딕", 12))
    progress_label.pack()

    # 진행 상황 바 생성
    progress_canvas = Canvas(window, width=300, height=15, highlightthickness=0)
    progress_canvas.pack()

    # 초기 문제 생성
    next_question()

    # Tkinter 창 실행
    window.mainloop()

def next_question():
    global answer, current_question, correct_count, wrong_count, score, level
    
    # 모든 문제를 다 풀었으면 종료
    if current_question == total_questions:
        print("맞은 문제 수:", correct_count)
        print("틀린 문제 수:", wrong_count)
        for widget in window.winfo_children():
            widget.destroy()
        
        if correct_count >= 1:
            result_text = "통과하였습니다."
            score = current_user.get("score", 0)
            score += 1
        else:
            result_text = "통과하지 못했습니다."
            score = current_user.get('score', 0)

        # 레벨 계산 및 업데이트
        level, print_score = get_level_from_score(score)
        current_user["level"] = level
        current_user["score"] = score

        level_text = f"맞은 문제의 수: {correct_count} 입니다.\n레벨은 {level}입니다.\n점수는 {print_score}점입니다."
        level_label = Label(window, text=level_text, font=("맑은 고딕", 20))
        level_label.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

        result_label = Label(window, text=result_text, font=("맑은 고딕", 20))
        result_label.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

        close_button = tkinter.Button(window, text="닫기", command=window.destroy)
        close_button.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

        
        # 유저 데이터 업데이트
        users = load_user_data()
        update_user_data(users, current_user, level, score)
        save_user_data(users)
        
        restart_test()
        return

    if current_question % 2 != 0:
        multi_choice_question()
    else:
        short_answer_question()

    current_question += 1
    progress_label.config(text=f"{current_question}/{total_questions}")
    update_progress()

def multi_choice_question():
    global answer, buttons

    buttons = []
    for i in range(4):
        btn = Button(window, text=f"{i+1}번", width=35, height=3,
                     command=lambda idx=i: check_answer(idx),
                     font=("맑은 고딕", 13, "bold"), bg=BTN_COLOR)
        btn.pack()
        buttons.append(btn)

    multi_choice = random.sample(new_questions, 4)
    answer = random.randint(0, 3)
    cur_question = multi_choice[answer][new_key_name]
    question_label.config(text=cur_question)

    for i in range(4):
        buttons[i].config(text=multi_choice[i][new_value_name], command=lambda idx=i: check_answer(idx))

def short_answer_question():
    global answer, entry, check_btn

    random_question = random.choice(new_questions)
    cur_question = random_question[new_value_name]
    answer = random_question[new_key_name]
    question_label.config(text=cur_question)

    entry = Entry(window, font=("맑은 고딕", 12), width=30)
    entry.pack()

    check_btn = Button(window, text="확인", width=15, height=2,
                       command=check_short_answer, font=("맑은 고딕", 15, "bold"), bg=BTN_COLOR)
    check_btn.pack()

def check_short_answer():
    global correct_count, wrong_count
    user_answer = entry.get().strip().lower()
    if user_answer == answer.lower():
        correct_count += 1
    else:
        wrong_count += 1
    entry.destroy()
    check_btn.destroy()
    window.after(1, next_question)

def check_answer(idx):
    global correct_count, wrong_count
    if idx == answer:
        correct_count += 1
    else:
        wrong_count += 1
    if buttons:    
        for btn in buttons:
            btn.destroy()
        window.after(1, next_question)

def update_progress():
    progress_canvas.delete("all")
    progress_canvas.create_rectangle(0, 0, current_question / total_questions * 300, 20, fill=PROGRESS_COLOR, outline="")

def restart_test():
    global correct_count, wrong_count, current_question, score, print_score

    correct_count = 0
    wrong_count = 0
    current_question = 0
    print_score = 0