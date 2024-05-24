from tkinter import *
import random
from wordDB import words
from level import get_level_from_score

# 각 딕셔너리의 key와 value 이름 설정
new_key_name = "english_word"
new_value_name = "korean_meaning"

# 새로운 형식의 딕셔너리 리스트 생성
new_questions = [{new_key_name: key, new_value_name: value} for item in words for key, value in item.items()]

# 색깔 상수들 정의
BGCOLOR = "#FFFFFF"     # 배경색
BTN_COLOR = "#F0F0F0"   # 버튼 배경색
PROGRESS_COLOR = "#2ECC71"  # 진행 바 색

# 정답 번호를 담을 변수 초기화
answer = 0
total_questions = 20  # 총 문제 수
correct_count = 0  # 맞은 문제 수
wrong_count = 0  # 틀린 문제 수
level = 0
score = 0
print_score = 0
current_question = 0  # 현재 진행 중인 문제 수

# Tkinter 창과 위젯 전역 변수 선언
window = None
question_label = None
progress_label = None
progress_canvas = None
buttons = []
entry = None
check_btn = None

def open_wordleveltest_window():
    global window, question_label, progress_label, progress_canvas

    # Tkinter 창 생성
    window = Tk()
    window.title("영어 퀴즈")
    window.config(padx=30, pady=10, bg=BGCOLOR)

    # 사용자의 수준을 알아보기 위한 텍스트
    level_text = Label(window, text="레벨 테스트입니다.",
                       font=("HanSans", 13), bg=BGCOLOR)
    level_text.pack()

    # 문제 표시 레이블 생성
    question_label = Label(window, width=30, height=4,
                           text="test", font=("HanSans", 20, "bold"), bg=BGCOLOR, fg="black")
    question_label.pack()

    # 진행 상황 표시 레이블 생성
    progress_label = Label(window, text=f"{current_question}/{total_questions}",
                           font=("HanSans", 12), bg=BGCOLOR)
    progress_label.pack()

    # 진행 상황 바 생성
    progress_canvas = Canvas(window, width=300, height=20, bg=BGCOLOR, highlightthickness=0)
    progress_canvas.pack()

    # 초기 문제 생성
    next_question()

    # Tkinter 창 실행
    window.mainloop()

# 다음 문제를 생성하는 함수
def next_question():
    global answer, current_question, correct_count, wrong_count , score ,print_score

    # 모든 문제를 다 풀었으면 종료
    if current_question == total_questions:
        print("맞은 문제 수:", correct_count)
        print("틀린 문제 수:", wrong_count)
        for widget in window.winfo_children():
            widget.destroy()
        get_level_from_score(score)
        level_text = f"맞은 문제의 수: {correct_count} 입니다.\n레벨은 {level}입니다.\n점수는 {print_score}점입니다."
        if correct_count >= 15:
            result_text = "통과하였습니다."
            score += 1
        else:
            result_text = "통과하지 못했습니다."

        level_label = Label(window, text=level_text, font=("HanSans", 13), bg=BGCOLOR)
        level_label.pack()
        result_label = Label(window, text=result_text, font=("HanSans", 13), bg=BGCOLOR)
        result_label.pack()
        return

    # 홀수 번째 문제는 4지선다형, 짝수 번째 문제는 단답형으로 생성
    if current_question % 2 != 0:
        # 4지선다형 문제 생성
        multi_choice_question()
    else:
        # 단답형 문제 생성
        short_answer_question()

    # 진행 상황 업데이트
    current_question += 1
    progress_label.config(text=f"{current_question}/{total_questions}")
    update_progress()

# 4지선다형 문제 생성 함수
def multi_choice_question():
    global answer, buttons
    
    # 버튼 생성
    buttons = []
    for i in range(4):
        btn = Button(window, text=f"{i+1}번", width=35, height=2,
                     command=lambda idx=i: check_answer(idx),
                     font=("HanSans", 15, "bold"), bg=BTN_COLOR)
        btn.pack()
        buttons.append(btn)
    
    # 문제 및 보기를 랜덤으로 선택
    multi_choice = random.sample(new_questions, 4)
    answer = random.randint(0, 3)
    cur_question = multi_choice[answer][new_key_name]
    question_label.config(text=cur_question)
    
    # 버튼에 보기 할당
    for i in range(4):
        buttons[i].config(text=multi_choice[i][new_value_name], command=lambda idx=i: check_answer(idx))

# 단답형 문제 생성 함수
def short_answer_question():
    global answer, entry, check_btn

    # 문제 및 보기를 랜덤으로 선택
    random_question = random.choice(new_questions)
    cur_question = random_question[new_value_name]  # 영어 단어
    answer = random_question[new_key_name]          # 한글 뜻
    question_label.config(text=cur_question)

    # 입력 창 생성
    entry = Entry(window, font=("HanSans", 12), width=30)
    entry.pack()

    # 확인 버튼 생성
    check_btn = Button(window, text="확인", width=15, height=2,
                       command=check_short_answer, font=("HanSans", 15, "bold"), bg=BTN_COLOR)
    check_btn.pack()

# 정답을 체크하는 함수(단답형)
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

# 정답을 체크하는 함수(4지선다형)
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

# 진행 상황 바 업데이트 함수
def update_progress():
    progress_canvas.delete("all")
    progress_canvas.create_rectangle(0, 0, current_question / total_questions * 300, 20, fill=PROGRESS_COLOR, outline="")

# Next 버튼을 누르면 wrong_count를 1 증가시키는 함수
def increase_wrong_count():
    global wrong_count
    wrong_count += 1


