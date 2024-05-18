import tkinter
from tkinter import messagebox
import json
from join_window import open_join_window
from user_window import open_user_window

def load_user_data(filepath='users.json'):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def validate_login(username, password, user_data):
    for user in user_data:
        if user['username'] == username and user['password'] == password:
            return True
    return False

def open_login_window(window):
    login_window = tkinter.Tk()  # 새로운 Tk 객체를 생성하여 로그인 창을 만듭니다.
    login_window.title("로그인")
    login_window.geometry("400x300")

    username_label = tkinter.Label(login_window, text="사용자 이름:")
    username_label.pack()

    password_label = tkinter.Label(login_window, text="비밀번호:")
    password_label.pack()

    username_entry = tkinter.Entry(login_window)
    username_entry.pack()

    password_entry = tkinter.Entry(login_window, show="*")
    password_entry.pack()

    def login():
        username = username_entry.get()
        password = password_entry.get()

        user_data = load_user_data()

        if validate_login(username, password, user_data):
            messagebox.showinfo("로그인 성공", "로그인에 성공했습니다.")
            login_window.destroy()  # 기존 로그인 창을 파괴합니다.
            open_user_window()  # 새로운 로그인 창을 열어줍니다.
        else:
            messagebox.showerror("로그인 실패", "잘못된 사용자 이름 또는 비밀번호입니다.")

    login_button = tkinter.Button(login_window, text="로그인", command=login)
    login_button.pack()

    join_button = tkinter.Button(login_window, width=10, bd=2, text="회원가입", command=lambda: open_join_window(window))
    join_button.pack()

    # 비밀번호 찾기 버튼 및 기능 추가
    def open_password_reset_window():
        password_reset_window = tkinter.Toplevel(login_window)
        password_reset_window.title("비밀번호 찾기")
        password_reset_window.geometry("300x200")

        username_label = tkinter.Label(password_reset_window, text="사용자 이름:")
        username_label.pack()

        username_entry = tkinter.Entry(password_reset_window)
        username_entry.pack()

        birthday_label = tkinter.Label(password_reset_window, text="생년월일(YYMMDD):")
        birthday_label.pack()

        birthday_entry = tkinter.Entry(password_reset_window)
        birthday_entry.pack()

        def reset_password():
            username = username_entry.get()
            birthday = birthday_entry.get()

            user_data = load_user_data()

            for user in user_data:
                if user['username'] == username and user['birthday'] == birthday:
                    messagebox.showinfo("비밀번호 찾기", f"비밀번호: {user['password']}")
                    password_reset_window.destroy()
                    return

            messagebox.showerror("에러", "일치하는 정보를 찾을 수 없습니다.")

        reset_button = tkinter.Button(password_reset_window, text="비밀번호 찾기", command=reset_password)
        reset_button.pack()

    password_reset_button = tkinter.Button(login_window, text="비밀번호 찾기", command=open_password_reset_window)
    password_reset_button.pack()

    close_button = tkinter.Button(login_window, text="닫기", command=login_window.destroy)
    close_button.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

    login_window.mainloop()

# 코드 실행을 위한 테스트
if __name__ == "__main__":
    root = tkinter.Tk()
    open_login_window(root)