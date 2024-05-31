import tkinter as tk
from tkinter import messagebox
import json
from tier_leaderboard import TierLeaderboard
from word_window import WordWindow
from test_main_window import TestWindow
import customtkinter 
from customtkinter import *
from PIL import Image

class UserWindow:
    def __init__(self):
        self.bgColor = "#FFDFB9"
        self.fgColor = "#A4193D"
        self.hoverColor = "#C850C0"
        self.rankImg = customtkinter.CTkImage(light_image=Image.open("ranking.png"), dark_image=Image.open("ranking.png"), size=(25, 25))
        self.refreshImg = customtkinter.CTkImage(light_image=Image.open("refresh2.png"), dark_image=Image.open("refresh2.png"), size=(30, 30))
        self.current_user = None
        self.window = None
        self.username_label = None
        self.level_label = None

    def load_user_data(self, filepath='users.json'):
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def open_login_window(self):
        import login_window
        login_window.open_login_window(self.window)

    def logout(self):
        confirm = messagebox.askokcancel("로그아웃", "정말 로그아웃 하시겠습니까?")
        if confirm:
            self.window.destroy()
            self.open_login_window()

    def withdraw(self):
        password_window = customtkinter.CTkToplevel(self.window)
        password_window.title("회원 탈퇴 - 정보 확인")
        password_window.geometry("400x500")
        password_window.resizable(False, False)
        password_window.config(background=self.bgColor)
        withdrawImg = customtkinter.CTkImage(light_image=Image.open("withdraw.png"), dark_image=Image.open("withdraw.png"), size=(300, 300))
        title_label = customtkinter.CTkLabel(password_window, text="", bg_color=self.bgColor, image=withdrawImg)
        title_label.pack()

        def check_credentials():
            entered_username = username_entry.get()
            entered_password = password_entry.get()
            user_data = self.load_user_data()

            for user in user_data:
                if user['username'] == entered_username and user['password'] == entered_password:
                    if entered_username == self.current_user['username']:
                        confirm = messagebox.askokcancel("회원 탈퇴", "정말 탈퇴하시겠습니까?")
                        if confirm:
                            user_data.remove(user)
                            with open('users.json', 'w', encoding='utf-8') as file:
                                json.dump(user_data, file, ensure_ascii=False, indent=4)
                            messagebox.showinfo("회원 탈퇴", "회원 탈퇴되었습니다.")
                            password_window.destroy()
                            self.window.destroy()
                            self.open_login_window()
                        return
                    else:
                        messagebox.showerror("회원 탈퇴", "로그인된 아이디와 입력된 아이디가 일치하지 않습니다.")
                        return

            messagebox.showerror("회원 탈퇴", "아이디 또는 비밀번호가 일치하지 않습니다.")

        username_label = tk.Label(password_window, text="아이디:", background=self.bgColor)
        username_label.pack()

        username_entry = customtkinter.CTkEntry(password_window, bg_color=self.bgColor, border_color=self.fgColor)
        username_entry.pack()

        password_label = tk.Label(password_window, text="비밀번호:", background=self.bgColor)
        password_label.pack()

        password_entry = customtkinter.CTkEntry(password_window, show="*", bg_color=self.bgColor, border_color=self.fgColor)
        password_entry.pack()

        confirm_button = customtkinter.CTkButton(password_window, text="확인", command=check_credentials, bg_color=self.bgColor, fg_color=self.fgColor, hover_color=self.hoverColor)
        confirm_button.pack()

    def open_user_window(self, user):
        self.current_user = user

        self.window = customtkinter.CTkToplevel()
        self.window.title("TOEICVOCAMACA - 단어장 목록")
        self.window.geometry("400x500+100+100")
        self.window.resizable(False, False)
        self.window.config(background=self.bgColor)

        def refresh_user_info():
            user_data = self.load_user_data()
            for user in user_data:
                if user['username'] == self.current_user['username']:
                    self.current_user.update(user)
                    self.username_label.config(text=f"ID: {self.current_user['username']}")
                    self.level_label.config(text=f"Level: {self.current_user.get('level', 'N/A')}")
                    break

        user_info_frame = tk.Frame(self.window)
        user_info_frame.pack(pady=20)
        user_info_frame.config(background=self.bgColor)

        self.username_label = tk.Label(user_info_frame, text=f"ID: {self.current_user['username']}", font=("맑은 고딕", 14), background=self.bgColor)
        self.username_label.pack()

        level_frame = tk.Frame(user_info_frame, background=self.bgColor)
        level_frame.pack()

        self.level_label = tk.Label(level_frame, text=f"Level: {self.current_user.get('level', 'N/A')}", font=("맑은 고딕", 14), background=self.bgColor)
        self.level_label.pack(side=tk.LEFT)

        def open_tier_board():
            # tier_leaderboard.py 파일에서 TierLeaderboard 클래스를 인스턴스화하여 티어 리더보드를 보여줍니다.
            tier_leaderboard_window = customtkinter.CTkToplevel()
            tier_leaderboard_window.title("TOEIC Vocabulary Tier Leaderboard")
            TierLeaderboard(tier_leaderboard_window)

        tier_board_button = customtkinter.CTkButton(level_frame, text="", image=self.rankImg, bg_color=self.bgColor, fg_color=self.bgColor, border_color=self.fgColor, hover_color=self.hoverColor, command=open_tier_board, width=25, height=25, border_width=2)
        tier_board_button.pack(side=customtkinter.LEFT, padx=5)

        word_list_button = customtkinter.CTkButton(self.window, text="단어장", width=80, height=200, command=self.open_wordlist_window, bg_color=self.fgColor, fg_color=self.fgColor, hover_color=self.hoverColor)
        word_list_button.place(relx=0.3, rely=0.4, anchor=tk.CENTER)

        test_button = customtkinter.CTkButton(self.window, text="테스트", width=80, height=200, command=lambda:self.open_test_page(user), bg_color=self.fgColor, fg_color=self.fgColor, hover_color=self.hoverColor)
        test_button.place(relx=0.7, rely=0.4, anchor=tk.CENTER)

        logout_button = customtkinter.CTkButton(self.window, text="로그아웃", bg_color=self.bgColor, fg_color=self.fgColor, hover_color=self.hoverColor, corner_radius=32, command=self.logout)
        logout_button.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

        withdraw_button = customtkinter.CTkButton(self.window, text="회원 탈퇴", bg_color=self.bgColor, fg_color=self.fgColor, hover_color=self.hoverColor, corner_radius=32, command=self.withdraw)
        withdraw_button.place(relx=0.5, rely=0.82, anchor=tk.CENTER)

        refresh_button = customtkinter.CTkButton(self.window, text="", width=20, height=20, image=self.refreshImg, bg_color=self.bgColor, fg_color=self.bgColor, border_color=self.bgColor, hover_color=self.hoverColor, command=refresh_user_info)
        refresh_button.place(relx=0.001, rely=0.01, anchor=tk.NW)

        self.window.attributes("-topmost", True)
        self.window.after(100, lambda: self.window.attributes("-topmost", False))
        self.window.mainloop()
    
    def open_test_page(self, user):
            test_window=TestWindow()
            test_window.open_test_window(user)

    def open_wordlist_window(self):
        word_window = WordWindow()
        word_window.open_wordlist_window()

