# login_window.py

import tkinter
from join_window import open_join_window

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

        # 더미로 설정된 사용자 이름과 비밀번호와 비교하여 로그인을 시도합니다.
        if username == "user" and password == "password":
            tkinter.messagebox.showinfo("로그인 성공", "로그인에 성공했습니다.")
            login_window.destroy()
            # 여기에 로그인 성공 시 수행할 동작을 추가할 수 있습니다.
        else:
            tkinter.messagebox.showerror("로그인 실패", "잘못된 사용자 이름 또는 비밀번호입니다.")

    # 로그인 버튼을 만들고 윈도우에 추가합니다.
    login_button = tkinter.Button(login_window, text="로그인", command=login)
    login_button.pack()


    join_button=tkinter.Button(login_window, width=10, bd=2, text="회원가입",command=lambda:open_join_window(window))
    join_button.pack()

