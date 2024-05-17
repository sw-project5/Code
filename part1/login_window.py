import tkinter
from tkinter import messagebox
import json
from join_window import open_join_window
from user_window import open_user_window

# JSON 파일에서 사용자 데이터를 로드하는 함수
def load_user_data(filepath='users.json'):
    # 예외 처리
    try:
        # 파일 불러와 'r'모드로 file에 저장
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    # 파일 없을 때
    except FileNotFoundError:
        return []
    # 시스템 에러
    except json.JSONDecodeError:
        return []

# 사용자 이름과 비밀번호를 검증하는 함수
def validate_login(username, password, user_data):
    # user_data : 
    for user in user_data:
        if user['username'] == username and user['password'] == password:
            return True
    return False

# 로그인 창을 열기 위한 함수를 정의합니다.
def open_login_window(window):
    # 새로운 윈도우를 만듭니다.
    login_window = tkinter.Toplevel(window)
    login_window.title("로그인")
    login_window.geometry("400x300")

    # 사용자 이름과 비밀번호 레이블을 추가합니다.
    username_label = tkinter.Label(login_window, text="사용자 이름:")
    username_label.pack()

    password_label = tkinter.Label(login_window, text="비밀번호:")
    password_label.pack()

    # 사용자 이름과 비밀번호를 입력할 수 있는 필드를 추가합니다.
    username_entry = tkinter.Entry(login_window)
    username_entry.pack()

    password_entry = tkinter.Entry(login_window, show="*")
    password_entry.pack()

    # 로그인 버튼을 누를 때 실행될 함수를 정의합니다.
    def login():
        # 입력한 사용자 이름과 비밀번호를 가져옵니다.
        username = username_entry.get()
        password = password_entry.get()

        # JSON 파일에서 사용자 데이터를 로드합니다.
        user_data = load_user_data()

        # 사용자 이름과 비밀번호를 검증합니다.
        if validate_login(username, password, user_data):
            messagebox.showinfo("로그인 성공", "로그인에 성공했습니다.")
            login_window.destroy()
            
            open_user_window()
        else:
            messagebox.showerror("로그인 실패", "잘못된 사용자 이름 또는 비밀번호입니다.")

    # 로그인 버튼을 만들고 윈도우에 추가합니다.
    login_button = tkinter.Button(login_window, text="로그인", command=login)
    login_button.pack()

    join_button = tkinter.Button(login_window, width=10, bd=2, text="회원가입", command=lambda: open_join_window(window))
    join_button.pack()

    close_button = tkinter.Button(login_window, text="닫기", command=login_window.destroy)
    close_button.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

    login_window.mainloop()
