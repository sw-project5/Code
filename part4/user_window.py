import tkinter
from tkinter import messagebox
import json
from word_window import open_wordlist_window
from test_main_window import open_test_window

# 현재 로그인된 사용자 정보를 저장할 전역 변수
current_user = None

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


def open_user_window(user):
    global current_user
    current_user = user

    window = tkinter.Tk()
    window.title("TOEICVOCAMACA - 단어장 목록")
    window.geometry("400x500+100+100")
    window.resizable(False, False)

    # 로그아웃 기능
    def logout():
        confirm = messagebox.askokcancel("로그아웃", "정말 로그아웃 하시겠습니까?")
        if confirm:
            window.destroy()  # 현재 창 닫기
            open_login_window(window)  # 로그인 창 열기

    # 회원 탈퇴 기능
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
                username = current_user['username']  # 현재 로그인된 사용자명
                user_data = load_user_data()

                for user in user_data:
                    if user['username'] == username and user['password'] == entered_password:
                        user_data.remove(user)
                        with open('users.json', 'w', encoding='utf-8') as file:
                            json.dump(user_data, file, ensure_ascii=False, indent=4)
                        messagebox.showinfo("회원 탈퇴", "회원 탈퇴되었습니다.")
                        password_window.destroy()  # 비밀번호 확인 창 닫기
                        window.destroy()  # 현재 창 닫기
                        open_login_window()  # 로그인 창 열기
                        return

                messagebox.showerror("회원 탈퇴", "아이디 또는 비밀번호가 일치하지 않습니다.")

            password_label = tkinter.Label(password_window, text="비밀번호:")
            password_label.pack()

            password_entry = tkinter.Entry(password_window, show="*")
            password_entry.pack()

            confirm_button = tkinter.Button(password_window, text="확인", command=check_password)
            confirm_button.pack()

    def open_word_page():
        window.destroy()
        open_wordlist_window()
    
    # 사용자 정보 표시 레이블 생성
    user_info_frame = tkinter.Frame(window)
    user_info_frame.pack(pady=20)

    username_label = tkinter.Label(user_info_frame, text=f"아이디: {current_user['username']}", font=("Arial", 12))
    username_label.pack()

    level_label = tkinter.Label(user_info_frame, text=f"레벨: {current_user.get('level', 'N/A')}", font=("Arial", 12))
    level_label.pack()

    word_list_button = tkinter.Button(window, text="단어장", width=8, height=10, command=open_wordlist_window)
    word_list_button.place(relx=0.3, rely=0.4, anchor=tkinter.CENTER)

    test_button = tkinter.Button(window, text="테스트", width=8, height=10, command=lambda:open_test_window(user))  # command="테스트 페이지"
    test_button.place(relx=0.7, rely=0.4, anchor=tkinter.CENTER)

    logout_button = tkinter.Button(window, text="로그아웃", command=logout)
    logout_button.place(relx=0.5, rely=0.75, anchor=tkinter.CENTER)

    withdraw_button = tkinter.Button(window, text="회원 탈퇴", command=withdraw)
    withdraw_button.place(relx=0.5, rely=0.82, anchor=tkinter.CENTER)

    window.mainloop()

