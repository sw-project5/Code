import tkinter
from tkinter import messagebox
import json
from datetime import datetime
import customtkinter
from customtkinter import *
from PIL import Image

# 기본 색상
bgColor = "#FFDFB9"
fgColor = "#A4193D"
hoverColor = "#C850C0"

class JoinWindow:
    def __init__(self, master):
        self.master = master
        self.join_window = None
        self.username_checked = False
        self.password_verified = False

    def open_join_window(self):
        self.join_window = customtkinter.CTkToplevel(self.master)
        self.join_window.title("회원가입")
        self.join_window.geometry("400x500")
        self.join_window.config(background=bgColor)

        signUpTextImg = customtkinter.CTkImage(light_image=Image.open("signup.png"),
                                               dark_image=Image.open("signup.png"),
                                               size=(250, 250))
        title_label = customtkinter.CTkLabel(self.join_window, text="", bg_color=bgColor, image=signUpTextImg)
        title_label.place(relx=0.5, rely=0.2, anchor="center")

        username_label = tkinter.Label(self.join_window, text="사용자 이름:", background=bgColor)
        username_label.place(relx=0.5, rely=0.35, anchor="center")

        self.username_entry = customtkinter.CTkEntry(self.join_window, placeholder_text="영어로 입력하세요", corner_radius=0, placeholder_text_color="#964B64", text_color="black", fg_color=bgColor, border_color=fgColor)
        self.username_entry.place(relx=0.5, rely=0.4, anchor="center")

        check_button = customtkinter.CTkButton(self.join_window, width=20, height=2, text="중복 확인", bg_color=bgColor, fg_color=fgColor, hover_color=hoverColor, command=self.check_duplicate)
        check_button.place(relx=0.85, rely=0.4, anchor=tkinter.E)

        password_label = tkinter.Label(self.join_window, text="비밀번호 입력:", background=bgColor)
        password_label.place(relx=0.5, rely=0.45, anchor="center")

        self.password_entry = customtkinter.CTkEntry(self.join_window, corner_radius=0, text_color="black", fg_color=bgColor, border_color=fgColor, show="*")
        self.password_entry.place(relx=0.5, rely=0.5, anchor="center")

        confirm_password_label = tkinter.Label(self.join_window, text="비밀번호 재확인:", background=bgColor)
        confirm_password_label.place(relx=0.5, rely=0.55, anchor="center")

        self.confirm_password_entry = customtkinter.CTkEntry(self.join_window, text_color="black", corner_radius=0, fg_color=bgColor, border_color=fgColor, show="*")
        self.confirm_password_entry.place(relx=0.5, rely=0.6, anchor="center")

        birthday_label = tkinter.Label(self.join_window, text="생년월일(YYMMDD):", background=bgColor)
        birthday_label.place(relx=0.5, rely=0.65, anchor="center")

        self.birthday_entry = customtkinter.CTkEntry(self.join_window, text_color="black", corner_radius=0, fg_color=bgColor, border_color=fgColor)
        self.birthday_entry.place(relx=0.5, rely=0.7, anchor="center")

        join_button = customtkinter.CTkButton(self.join_window, text="회원가입", bg_color=bgColor, fg_color=fgColor, hover_color=hoverColor, command=self.join)
        join_button.place(relx=0.5, rely=0.8, anchor="center")

        close_button = customtkinter.CTkButton(self.join_window, text="닫기", width=20, height=10, bg_color=bgColor, fg_color=fgColor, hover_color=hoverColor, command=self.join_window.destroy)
        close_button.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

        self.join_window.attributes("-topmost", True)
        self.join_window.after(100, lambda: self.join_window.attributes("-topmost", False))
        self.join_window.mainloop()

    def check_duplicate(self):
        username = self.username_entry.get()
        if username == '':
            tkinter.messagebox.showerror("에러", "사용자 이름을 입력하시오.")
            self.username_checked = False
            return

        if self.check_duplicate_username(username):
            tkinter.messagebox.showinfo("에러", "이미 사용 중인 사용자 이름입니다.")
            self.username_checked = False
        else:
            tkinter.messagebox.showinfo("알림", "사용 가능한 사용자 이름입니다.")
            self.username_checked = True

    def check_duplicate_username(self, username):
        try:
            with open("users.json", "r") as file:
                users = json.load(file)
                for user in users:
                    if user["username"] == username:
                        return True
        except FileNotFoundError:
            return False
        return False

    def join(self):
        if not self.username_checked:
            tkinter.messagebox.showerror("에러", "사용자 이름 중복 확인을 진행하세요.")
            return

        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        birthday = self.birthday_entry.get()

        if not (username and password and confirm_password and birthday):
            tkinter.messagebox.showerror("에러", "모든 회원 정보를 입력하세요.")
            return

        if self.check_duplicate_username(username):
            tkinter.messagebox.showerror("에러", "이미 사용 중인 사용자 이름입니다.")
            return

        if password != confirm_password:
            tkinter.messagebox.showerror("에러", "비밀번호가 일치하지 않습니다.")
            return

        try:
            datetime.strptime(birthday, '%y%m%d')
        except ValueError:
            tkinter.messagebox.showerror("에러", "올바른 생년월일 형식이 아닙니다. (YYMMDD)")
            return

        try:
            with open("users.json", "r") as file:
                users = json.load(file)
        except FileNotFoundError:
            users = []

        user_data = {
            "username": username,
            "password": password,
            "birthday": birthday,
            "firstlogin": True,
            "level": "iron",
            "score": 0
        }

        users.append(user_data)

        try:
            with open("users.json", "w") as file:
                json.dump(users, file, indent=4)
        except Exception as e:
            tkinter.messagebox.showerror("에러", "일시적인 오류가 발생했습니다. 나중에 다시 시도해주세요.")
            return

        tkinter.messagebox.showinfo("성공", "회원가입이 완료되었습니다.")
        self.join_window.destroy()



