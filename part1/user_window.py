import tkinter as tk
from tkinter import messagebox
import json
from tier_leaderboard import tier_board  # tier_board_page 모듈에서 tier_board 함수를 import
from word_window import open_wordlist_window
from test_main_window import open_test_window
import customtkinter 
from customtkinter import *
from PIL import Image

# 기본 색상
bgColor = "#FFDFB9"
fgColor = "#A4193D"
hoverColor = "#C850C0"
rankImg=customtkinter.CTkImage(light_image=Image.open("ranking.png"),dark_image=Image.open("ranking.png"),size=(25,25))
refreshImg=customtkinter.CTkImage(light_image=Image.open("refresh2.png"),dark_image=Image.open("refresh2.png"),size=(30,30))
# 현재 로그인된 사용자 정보를 저장할 전역 변수
current_user = None

# 사용자 데이터 로드 함수
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
    global current_user, username_label, level_label
    current_user = user

    window = customtkinter.CTkToplevel()
    window.title("TOEICVOCAMACA - 단어장 목록")
    window.geometry("400x500+100+100")
    window.resizable(False, False)
    window.config(background=bgColor)

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
            password_window = customtkinter.CTkToplevel(window)
            password_window.title("회원 탈퇴 - 비밀번호 확인")
            password_window.geometry("300x150")
            password_window.resizable(False, False)
            password_window.config(background=bgColor)

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

            password_label = tk.Label(password_window, text="비밀번호:",background=bgColor)
            password_label.pack()

            password_entry = customtkinter.CTkEntry(password_window, show="*",bg_color=bgColor,border_color=fgColor)
            password_entry.pack()

            confirm_button = customtkinter.CTkButton(password_window, text="확인", command=check_password,bg_color=bgColor,fg_color=fgColor,hover_color=hoverColor)
            confirm_button.pack()

    def open_word_page():
        window.destroy()
        open_wordlist_window()

    def refresh_user_info():
        user_data = load_user_data()
        for user in user_data:
            if user['username'] == current_user['username']:
                current_user.update(user)
                username_label.config(text=f"ID: {current_user['username']}")
                level_label.config(text=f"Level: {current_user.get('level', 'N/A')}")
                break

    # 사용자 정보 표시 레이블 생성
    user_info_frame = tk.Frame(window)
    user_info_frame.pack(pady=20)
    user_info_frame.config(background=bgColor)

    username_label = tk.Label(user_info_frame, text=f"ID: {current_user['username']}", font=("Arial", 12), background=bgColor)
    username_label.pack()

    level_frame = tk.Frame(user_info_frame, background=bgColor)
    level_frame.pack()

    level_label = tk.Label(level_frame, text=f"Level: {current_user.get('level', 'N/A')}", font=("Arial", 12), background=bgColor)
    level_label.pack(side=tk.LEFT)

    tier_board_button = customtkinter.CTkButton(level_frame,text="",image=rankImg, bg_color=bgColor,fg_color=bgColor,border_color=fgColor, hover_color=hoverColor,command=tier_board,width=25,height=25,border_width=2)
    tier_board_button.pack(side=customtkinter.LEFT, padx=5)
    

    word_list_button = customtkinter.CTkButton(window, text="단어장", width=80, height=200, command=open_wordlist_window, bg_color=fgColor,fg_color=fgColor,hover_color=hoverColor)
    word_list_button.place(relx=0.3, rely=0.4, anchor=tk.CENTER)

    test_button = customtkinter.CTkButton(window, text="테스트", width=80, height=200, command=lambda: open_test_window(user), bg_color=fgColor,fg_color=fgColor,hover_color=hoverColor)  # command="테스트 페이지"
    test_button.place(relx=0.7, rely=0.4, anchor=tk.CENTER)

    logout_button = customtkinter.CTkButton(window, text="로그아웃", bg_color=bgColor, fg_color=fgColor, hover_color=hoverColor, corner_radius=32, command=logout)
    logout_button.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

    withdraw_button = customtkinter.CTkButton(window, text="회원 탈퇴", bg_color=bgColor, fg_color=fgColor, hover_color=hoverColor, corner_radius=32, command=withdraw)
    withdraw_button.place(relx=0.5, rely=0.82, anchor=tk.CENTER)
    #새로고침 버튼
    refresh_button = customtkinter.CTkButton(window, text="", width=20,height=20,image=refreshImg,bg_color=bgColor,fg_color=bgColor,border_color=bgColor,hover_color=hoverColor, command=refresh_user_info)
    refresh_button.place(relx=0.001, rely=0.01, anchor=tk.NW)  # 맨 왼쪽 상단에 배치

    window.mainloop()
