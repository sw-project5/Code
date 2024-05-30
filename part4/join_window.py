import tkinter
from tkinter import messagebox
import json
from datetime import datetime
import customtkinter 
from customtkinter import *
from PIL import Image

# 기본 색상
bgColor="#FFDFB9"
fgColor="#A4193D"
hoverColor="#C850C0"

# 플래그 변수 추가
username_checked = False
# password_verified = False

def join():
    global username_checked, password_verified

    if not username_checked:
        tkinter.messagebox.showerror("에러", "사용자 이름 중복 확인을 진행하세요.")
        return

    # if not password_verified:
    #     tkinter.messagebox.showerror("에러", "비밀번호 검증을 진행하세요.")
    #     return

    username = username_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()
    birthday = birthday_entry.get()
    
    if not (username and password and confirm_password and birthday):
        tkinter.messagebox.showerror("에러", "모든 회원 정보를 입력하세요.")
        return

    if check_duplicate_username(username):
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
        "level":"iron",
        "score" : 0
    }

    users.append(user_data)
    
    #시스템 에러 처리 코드
    try:
        with open("users.json", "w") as file:
            json.dump(users, file, indent=4)
    except Exception as e:
        tkinter.messagebox.showerror("에러", "일시적인 오류가 발생했습니다. 나중에 다시 시도해주세요.")
        return

    tkinter.messagebox.showinfo("성공", "회원가입이 완료되었습니다.")
    join_window.destroy()
    

def check_duplicate_username(username):
    if username == '':
        return 5
    try:
        with open("users.json", "r") as file:
            users = json.load(file)
            for user in users:
                if user["username"] == username:
                    return True
    except FileNotFoundError:
        return False
    return False

def open_join_window(window):
    global join_window, username_checked, password_verified
    username_checked = False
    password_verified = False

    join_window = customtkinter.CTkToplevel()
    join_window.title("회원가입")
    join_window.geometry("400x500")
    join_window.config(background=bgColor)
    signUpTextImg=customtkinter.CTkImage(light_image=Image.open("signup.png"),
                               dark_image=Image.open("signup.png"),
                               size=(250,250))
    title_label = customtkinter.CTkLabel(join_window, text="", bg_color=bgColor, image=signUpTextImg)
    title_label.place(relx=0.5, rely=0.2, anchor="center")
    
    username_label = tkinter.Label(join_window, text="사용자 이름:", background=bgColor)
    username_label.place(relx=0.5, rely=0.35, anchor="center")

    global username_entry
    username_entry = customtkinter.CTkEntry(join_window, placeholder_text="영어로 입력하세요", corner_radius=0, placeholder_text_color="#964B64", text_color="black", fg_color=bgColor, border_color=fgColor)
    username_entry.place(relx=0.5, rely=0.4, anchor="center")

    check_button = customtkinter.CTkButton(join_window, width=20, height=2, text="중복 확인", bg_color=bgColor, fg_color=fgColor, hover_color=hoverColor, command=lambda: check_duplicate(username_entry.get()))
    check_button.place(relx=0.85, rely=0.4, anchor=tkinter.E)

    password_label = tkinter.Label(join_window, text="비밀번호 입력:", background=bgColor)
    password_label.place(relx=0.5, rely=0.45, anchor="center")

    global password_entry
    password_entry = customtkinter.CTkEntry(join_window, corner_radius=0, text_color="black", fg_color=bgColor, border_color=fgColor, show="*")
    password_entry.place(relx=0.5, rely=0.5, anchor="center")

    confirm_password_label = tkinter.Label(join_window, text="비밀번호 재확인:", background=bgColor)
    confirm_password_label.place(relx=0.5, rely=0.55, anchor="center")

    global confirm_password_entry
    confirm_password_entry = customtkinter.CTkEntry(join_window, text_color="black", corner_radius=0, fg_color=bgColor, border_color=fgColor, show="*")
    confirm_password_entry.place(relx=0.5, rely=0.6, anchor="center")

    # verify_button = customtkinter.CTkButton(join_window, width=20, height=2, text="검증 확인", bg_color=bgColor, fg_color=fgColor, hover_color=hoverColor, command=lambda: verify_password(password_entry.get(), confirm_password_entry.get()))
    # verify_button.place(relx=0.85, rely=0.6, anchor=tkinter.E)

    birthday_label = tkinter.Label(join_window, text="생년월일(YYMMDD):", background=bgColor)
    birthday_label.place(relx=0.5, rely=0.65, anchor="center")

    global birthday_entry
    birthday_entry = customtkinter.CTkEntry(join_window, text_color="black", corner_radius=0, fg_color=bgColor, border_color=fgColor)
    birthday_entry.place(relx=0.5, rely=0.7, anchor="center")

    join_button = customtkinter.CTkButton(join_window, text="회원가입", bg_color=bgColor, fg_color=fgColor, hover_color=hoverColor, command=join)
    join_button.place(relx=0.5, rely=0.8, anchor="center")

    close_button = customtkinter.CTkButton(join_window, text="닫기", width=20, height=10, bg_color=bgColor, fg_color=fgColor, hover_color=hoverColor, command=join_window.destroy)
    close_button.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

    def check_duplicate(username):
        global username_checked
        if check_duplicate_username(username) == True:
            tkinter.messagebox.showinfo("에러", "이미 사용 중인 사용자 이름입니다.")
        elif check_duplicate_username(username) == False:
            tkinter.messagebox.showinfo("알림", "사용 가능한 사용자 이름입니다.")
            username_checked = True
        else:
            tkinter.messagebox.showerror("에러", "사용자 이름을 입력하시오.")
            username_checked = False

    # def verify_password(password, confirm_password):
    #     global password_verified
    #     if not password or not confirm_password:
    #         tkinter.messagebox.showerror("에러", "비밀번호를 입력하세요.")
    #         password_verified = False
    #     elif password == confirm_password:
    #         tkinter.messagebox.showinfo("알림", "비밀번호가 일치합니다.")
    #         password_verified = True
    #     else:
    #         tkinter.messagebox.showerror("에러", "비밀번호가 일치하지 않습니다.")
    #         password_verified = False

    join_window.attributes("-topmost", True)
    join_window.after(100, lambda: join_window.attributes("-topmost", False))
    join_window.mainloop()


