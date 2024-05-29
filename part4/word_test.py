import tkinter as tk
import random
from wordDB import words
import customtkinter 
from customtkinter import *
from PIL import Image

# 각 딕셔너리의 key와 value 이름 설정
new_key_name = "english_word"
new_value_name = "korean_meaning"

# 새로운 형식의 딕셔너리 리스트 생성
new_questions = [{new_key_name: key, new_value_name: value} for item in words for key, value in item.items()]

# 기본 색상
bgColor = "#FFDFB9"
fgColor = "#A4193D"
hoverColor = "#C850C0"
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
        level_label = customtkinter.CTkLabel(window, text=level_text,text_color="black",bg_color=bgColor, font=("맑은 고딕", 20))
        level_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        reset_counts()  # 맞은 문제 수와 틀린 문제 수 초기화

        close_button = customtkinter.CTkButton(window, text="닫기", width=30,height=20,command=window.destroy,bg_color=bgColor,fg_color=fgColor,hover_color=hoverColor)
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
    progress_label.configure(text=f"{current_question}/{total_questions}")
    update_progress()

def multi_choice_question():
    global answer, buttons

    # 기존 버튼들을 모두 제거
    if buttons:
        for btn in buttons:
            btn.destroy()

    buttons = []
    for i in range(4):
        btn = customtkinter.CTkButton(window, width=200, height=50,  # 버튼 크기를 동일하게 설정
                     text=f"{i+1}번", command=lambda idx=i: check_answer(idx), 
                     bg_color=bgColor, fg_color=fgColor, hover_color=hoverColor, 
                     corner_radius=32, text_color="white")
        btn.pack(pady=5)  # 버튼 간의 간격을 위해 패딩 추가
        buttons.append(btn)

    multi_choice = random.sample(new_questions, 4)
    answer = random.randint(0, 3)
    cur_question = multi_choice[answer][new_key_name]
    question_label.configure(text=cur_question)

    for i in range(4):
        wrapped_text = wrap_text(multi_choice[i][new_value_name], 20)  # 텍스트를 20자로 줄바꿈
        buttons[i].configure(text=wrapped_text, command=lambda idx=i: check_answer(idx))

def short_answer_question():
    global answer, entry, check_btn

    random_question = random.choice(new_questions)
    cur_question = random_question[new_value_name]
    answer = random_question[new_key_name]
    question_label.configure(text=cur_question)

    entry = customtkinter.CTkEntry(window,  width=200,fg_color=bgColor,border_color=fgColor,text_color="black"
                                   ,corner_radius=0)
    entry.pack(pady=7)

    check_btn = customtkinter.CTkButton(window, text="확인", width=150, height=50,bg_color=bgColor,fg_color=fgColor,hover_color=hoverColor,corner_radius=32,
                                        text_color="white",font=("맑은 고딕",16 ,"bold"),command=check_short_answer)
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
    # 테두리를 그리는 사각형
    progress_canvas.create_rectangle(0, 0, 300, 20, outline=fgColor, width=2)
    # 배경색을 채우는 사각형
    progress_canvas.create_rectangle(1, 1, 299, 19, fill=bgColor, outline="")
    # 진행률을 나타내는 사각형
    progress_canvas.create_rectangle(1, 1, current_question / total_questions * 299, 19, fill=fgColor, outline="")


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
    window = customtkinter.CTkToplevel()
    window.title("영어 퀴즈")
    window.geometry("600x500+100+100")
    window.resizable(False, False)
    window.config(background=bgColor)

    # 사용자의 수준을 알아보기 위한 텍스트
    level_text = customtkinter.CTkLabel(window, text="사용자의 수준을 알아보기 위해 단어 테스트를 진행하겠습니다.",
                          text_color="black",bg_color=bgColor,font=("맑은 고딕", 13))
    level_text.pack(pady=30)
    
    # 문제 표시 레이블 생성
    question_label = customtkinter.CTkLabel(window, width=30, height=4,
                           text="test",text_color="black", font=("맑은 고딕", 20, "bold"),bg_color=bgColor)
    question_label.pack(pady=10)

    # 진행 상황 표시 레이블 생성
    progress_label = customtkinter.CTkLabel(window,text=f"{current_question}/{total_questions}",
                           font=("맑은 고딕", 12), text_color="black",bg_color=bgColor)
    progress_label.pack()

    # 진행 상황 바 생성
    progress_canvas = customtkinter.CTkCanvas(window, width=300, height=20, highlightthickness=0,highlightbackground=fgColor)
    progress_canvas.pack(pady=30)

    # 초기 문제 생성
    next_question()

    # Tkinter 창 실행
    window.attributes("-topmost", True)
    window.after(100, lambda: window.attributes("-topmost", False))
    window.mainloop()

