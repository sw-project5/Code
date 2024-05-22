import tkinter
from tkinter import messagebox
import json

def load_user_data(filepath='users.json'):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def open_login_window(window):
    import login_window
    login_window.open_login_window(window)  # 기존 인자를 그대로 전달

def open_word_list_window():
    window = tkinter.Tk()
    window.title("TOEICVOCAMACA - 단어장 목록")
    window.geometry("400x500+100+100")
    window.resizable(False, False)

    def logout():
        confirm = messagebox.askokcancel("로그아웃", "정말 로그아웃 하시겠습니까?")
        if confirm:
            window.destroy()  # 현재 창 닫기
            open_login_window(window)  # 로그인 창 열기

    def withdraw():
        confirm = messagebox.askokcancel("회원 탈퇴", "정말 회원 탈퇴하시겠습니까?")
        if confirm:
            # 비밀번호 입력 창 생성
            password_window = tkinter.Toplevel(window)
            password_window.title("회원 탈퇴 - 비밀번호 확인")
            password_window.geometry("300x150")
            password_window.resizable(False, False)

            def check_password():
                entered_password = password_entry.get()
                username = username_entry.get()
                user_data = load_user_data()

                for user in user_data:
                    if user['username'] == username and user['password'] == entered_password:
                        user_data.remove(user)
                        with open('users.json', 'w', encoding='utf-8') as file:
                            json.dump(user_data, file, ensure_ascii=False, indent=4)
                        messagebox.showinfo("회원 탈퇴", "회원 탈퇴되었습니다.")
                        password_window.destroy()  # 비밀번호 확인 창 닫기
                        window.destroy()  # 현재 창 닫기
                        open_login_window(window)  # 로그인 창 열기
                        return

                messagebox.showerror("회원 탈퇴", "아이디 또는 비밀번호가 일치하지 않습니다.")

            username_label = tkinter.Label(password_window, text="아이디:")
            username_label.pack()

            username_entry = tkinter.Entry(password_window)
            username_entry.pack()

            password_label = tkinter.Label(password_window, text="비밀번호:")
            password_label.pack()

            password_entry = tkinter.Entry(password_window, show="*")
            password_entry.pack()

            confirm_button = tkinter.Button(password_window, text="확인", command=check_password)
            confirm_button.pack()

    logout_button = tkinter.Button(window, text="로그아웃", command=logout)
    logout_button.pack()

    withdraw_button = tkinter.Button(window, text="회원 탈퇴", command=withdraw)
    withdraw_button.pack()

    window.mainloop()
