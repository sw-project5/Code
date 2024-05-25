import tkinter as tk
import random
from wordDB import words

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
current_question = 0  # 현재 진행 중인 문제 수

# Tkinter 창과 위젯 전역 변수 선언
window = None
question_label = None
progress_label = None
progress_canvas = None
buttons = []
entry = None
check_btn = None

def wrap_text(text, line_length):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line) + len(word) + 1 <= line_length:
            current_line += (word + " ")
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    if current_line:
        lines.append(current_line.strip())
    return "\n".join(lines)

def next_question():
    global answer, current_question, correct_count, wrong_count

    # 모든 문제를 다 풀었으면 종료
    if current_question == total_questions:
        print("맞은 문제 수:", correct_count)
        print("틀린 문제 수:", wrong_count)
        for widget in window.winfo_children():
            widget.destroy()
        level_text = f"맞은 문제의 수: {correct_count} 입니다."
        level_label = tk.Label(window, text=level_text, font=("맑은 고딕", 20))
        level_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        reset_counts()  # 맞은 문제 수와 틀린 문제 수 초기화

        close_button = tk.Button(window, text="닫기", command=window.destroy)
        close_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

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

def multi_choice_question():
    global answer, buttons

    # 버튼 생성
    buttons = []
    for i in range(4):
        btn = tk.Button(window, text=f"{i+1}번", width=35, height=3,
                        command=lambda idx=i: check_answer(idx),
                        font=("맑은 고딕", 10, "bold"), bg=BTN_COLOR)
        btn.pack()
        buttons.append(btn)

    # 문제 및 보기를 랜덤으로 선택
    multi_choice = random.sample(new_questions, 4)
    answer = random.randint(0, 3)
    cur_question = multi_choice[answer][new_key_name]
    question_label.config(text=cur_question)

    # 버튼에 보기 할당
    for i in range(4):
        wrapped_text = wrap_text(multi_choice[i][new_value_name], 20)  # 텍스트를 20자로 줄바꿈
        buttons[i].config(text=wrapped_text, command=lambda idx=i: check_answer(idx))

def short_answer_question():
    global answer, entry, check_btn

    # 문제 및 보기를 랜덤으로 선택
    random_question = random.choice(new_questions)
    cur_question = random_question[new_value_name]  # 영어 단어
    answer = random_question[new_key_name]          # 한글 뜻
    question_label.config(text=cur_question)

    # 입력 창 생성
    entry = tk.Entry(window, font=("맑은 고딕", 12), width=30)
    entry.pack()

    # 확인 버튼 생성
    check_btn = tk.Button(window, text="확인", width=15, height=2,
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

def increase_wrong_count():
    global wrong_count
    wrong_count += 1

def reset_counts():
    global correct_count, wrong_count, current_question
    correct_count = 0
    wrong_count = 0
    current_question = 0

def open_wordtest_window():
    global window, question_label, progress_label, progress_canvas, current_question

    # Tkinter 창 생성
    window = tk.Tk()
    window.title("영어 퀴즈")
    window.geometry("600x500+100+100")
    window.resizable(False, False)

    # 사용자의 수준을 알아보기 위한 텍스트
    level_text = tk.Label(window, text="사용자의 수준을 알아보기 위해 단어 테스트를 진행하겠습니다.",
                          font=("맑은 고딕", 13))
    level_text.pack()

    # 문제 표시 레이블 생성
    question_label = tk.Label(window, width=30, height=4,
                              text="test", font=("맑은 고딕", 20, "bold"), fg="black")
    question_label.pack()

    # 진행 상황 표시 레이블 생성
    current_question = 0
    progress_label = tk.Label(window, text=f"{current_question}/{total_questions}",
                              font=("맑은 고딕", 12))
    progress_label.pack()

    # 진행 상황 바 생성
    progress_canvas = tk.Canvas(window, width=300, height=15, highlightthickness=0)
    progress_canvas.pack()

    # 초기 문제 생성
    next_question()

    # Tkinter 창 실행
    window.mainloop()


