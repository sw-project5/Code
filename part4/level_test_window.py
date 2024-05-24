import tkinter as tk
from tkinter import messagebox
from wordDB import words
import random
from user_window import open_user_window
import json

# 사용자 데이터 로드 함수
def load_user_data(filepath='users.json'):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

# 로그인 검증 함수
def validate_login(username, password, user_data):
    for user in user_data:
        if user['username'] == username and user['password'] == password:
            return user
    return False

# 각 딕셔너리의 key와 value 이름 설정
new_key_name = "english_word"
new_value_name = "korean_meaning"

# 새로운 형식의 딕셔너리 리스트 생성
new_questions = [{new_key_name: key, new_value_name: value} for item in words for key, value in item.items()]

# 색깔 상수들 정의
BGCOLOR = "#FFFFFF"     # 배경색
BTN_COLOR = "#F0F0F0"          # 버튼 배경색
PROGRESS_COLOR = "#2ECC71"     # 진행 바 색

# 정답 번호를 담을 변수 초기화
answer = 0
total_questions = 20  # 총 문제 수
correct_count = 0  # 맞은 문제 수
wrong_count = 0  # 틀린 문제 수

# 전역 변수로 사용자 이름 저장
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

def open_level_test_window(user):
    global answer, current_question, correct_count, wrong_count, current_user
    

    # 변수 초기화
    current_user = user
    correct_count = 0
    wrong_count = 0
    current_question = 0

    level_test_window = tk.Tk()
    level_test_window.title("영어 퀴즈")
    level_test_window.config(padx=30, pady=10, bg="#FFFFFF")

    # 테스트 결과 맨 위로 올라오게 하기
    level_test_window.attributes("-topmost", True)
    level_test_window.update()

    # 사용자의 수준을 알아보기 위한 텍스트
    level_text = tk.Label(level_test_window, text="사용자의 수준을 알아보기 위해 레벨 테스트를 진행하겠습니다.",
                    font=("맑은 고딕", 13), bg=BGCOLOR)
    level_text.pack()

    # 문제 표시 레이블 생성
    question_label = tk.Label(level_test_window, width=30, height=4, text="test", font=("맑은 고딕", 20, "bold"), bg="#FFFFFF", fg="black")
    question_label.pack()

    # 진행 상황 표시 레이블 생성
    current_question = 0
    progress_label = tk.Label(level_test_window, text=f"{current_question}/{total_questions}", font=("맑은 고딕", 12), bg="#FFFFFF")
    progress_label.pack()

    # 진행 상황 바 생성
    progress_canvas = tk.Canvas(level_test_window, width=300, height=20, bg="#FFFFFF", highlightthickness=0)
    progress_canvas.pack()

    # 초기 문제 생성
    next_question(level_test_window, question_label, progress_label, progress_canvas) 



    


def next_question(window, question_label, progress_label, progress_canvas):
    global answer, current_question, correct_count, wrong_count ,score, current_user, level

    # 모든 문제를 다 풀었으면 종료
    if current_question == total_questions:
        for widget in window.winfo_children():
            widget.destroy()
        
        if correct_count >= 0 and correct_count <= 4:
            level = "Iron"
            score = 0
        elif correct_count >= 5 and correct_count <= 14:
            level = "Bronze"
            score = 10
        elif correct_count >= 15 and correct_count <= 20:
            level = "Silver"
            score = 20
        
        current_user['level'] = level
        current_user['score'] = score

        level_text = f"맞은 문제 수: {correct_count}\n틀린 문제 수: {wrong_count}\n당신의 레벨은 '{level}'입니다.\n지금부터 우리와 함께 단어 학습을 시작하세요."
        level_label = tk.Label(window, text=level_text, font=("맑은 고딕", 13), bg="#FFFFFF")
        level_label.pack()
        
            # 유저 데이터 업데이트
        users = load_user_data()
        update_user_data(users, current_user, level, score)
        
        save_user_data(users)
        

        
            
        

        #open_user_window(user)
        return
        
    # 홀수 번째 문제는 4지선다형, 짝수 번째 문제는 단답형으로 생성
    if current_question % 2 != 0:
        # 4지선다형 문제 생성
        multi_choice_question(window, question_label, progress_label, progress_canvas)
    else:
        # 단답형 문제 생성
        short_answer_question(window, question_label, progress_label, progress_canvas)

    # 진행 상황 업데이트
    current_question += 1
    progress_label.config(text=f"{current_question}/{total_questions}")
    update_progress(progress_canvas)

def multi_choice_question(window, question_label, progress_label, progress_canvas):
    global answer, buttons
    
    # 버튼 생성
    buttons = []
    for i in range(4):
        btn = tk.Button(window, text=f"{i+1}번", width=35, height=2, command=lambda idx=i: check_answer(idx, window, question_label, progress_label, progress_canvas), font=("맑은 고딕", 15, "bold"), bg="#F0F0F0")
        btn.pack()
        buttons.append(btn)
    # 문제 및 보기를 랜덤으로 선택
    multi_choice = random.sample(new_questions, 4)
    answer = random.randint(0, 3)
    cur_question = multi_choice[answer][new_key_name]
    question_label.config(text=cur_question)
    
    # 버튼에 보기 할당
    for i in range(4):
        buttons[i].config(text=multi_choice[i][new_value_name], command=lambda idx=i: check_answer(idx, window, question_label, progress_label, progress_canvas))

def short_answer_question(window, question_label, progress_label, progress_canvas):
    global answer, entry, check_btn

    # 문제 및 보기를 랜덤으로 선택
    random_question = random.choice(new_questions)
    cur_question = random_question[new_value_name]  # 영어 단어
    answer = random_question[new_key_name]        # 한글 뜻
    question_label.config(text=cur_question)

    # 입력 창 생성
    entry = tk.Entry(window, font=("맑은 고딕", 12), width=30)
    entry.pack()

    # 확인 버튼 생성
    check_btn = tk.Button(window, text="확인", width=15, height=2, command=lambda: check_short_answer(window, question_label, progress_label, progress_canvas), font=("맑은 고딕", 15, "bold"), bg="#F0F0F0")
    check_btn.pack()

def check_short_answer(window, question_label, progress_label, progress_canvas):
    global correct_count, wrong_count
    user_answer = entry.get().strip().lower()
    if user_answer == answer.lower():
        correct_count += 1
    else:
        wrong_count += 1
    entry.destroy()
    check_btn.destroy()
    window.after(1, next_question, window, question_label, progress_label, progress_canvas)

def check_answer(idx, window, question_label, progress_label, progress_canvas):
    global correct_count, wrong_count
    
    if idx == answer:
        correct_count += 1
    else:
        wrong_count += 1
    if buttons:
        for btn in buttons:
            btn.destroy()
    window.after(1, next_question, window, question_label, progress_label, progress_canvas)

def update_progress(progress_canvas):
    progress_canvas.delete("all")
    progress_canvas.create_rectangle(0, 0, current_question / total_questions * 300, 20, fill="#2ECC71", outline="")

