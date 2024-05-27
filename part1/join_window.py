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

def join():
    # entry.get() : 기입창의 텍스트를 문자열로 반환
    username = username_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()
    birthday = birthday_entry.get()
    

    # 필수 필드가 비어 있는지 확인
    if not (username and password and confirm_password and birthday):
        tkinter.messagebox.showerror("에러", "모든 회원 정보를 입력하세요.")
        return

    # 사용자 이름 중복 확인
    if check_duplicate_username(username):
        tkinter.messagebox.showerror("에러", "이미 사용 중인 사용자 이름입니다.")
        return

    # 비밀번호 일치 여부 확인
    if password != confirm_password:
        tkinter.messagebox.showerror("에러", "비밀번호가 일치하지 않습니다.")
        return

    # 생년월일 형식 확인
    try:
        datetime.strptime(birthday, '%y%m%d')
    except ValueError:
        tkinter.messagebox.showerror("에러", "올바른 생년월일 형식이 아닙니다. (YYMMDD)")
        return

    # JSON 파일 불러오기
    try:
        with open("users.json", "r") as file:
            users = json.load(file)
    except FileNotFoundError:
        users = []

    # 새로운 사용자 데이터 생성
    user_data = {
        "username": username,
        "password": password,
        "birthday": birthday,
        "firstlogin": True,
        "level":"iron",
        "score" : 0
    }

    # 사용자 데이터 추가
    users.append(user_data)

    # JSON 파일에 데이터 저장
    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)

    # 회원가입 성공 메시지
    tkinter.messagebox.showinfo("성공", "회원가입이 완료되었습니다.")
    

# 사용자 이름 중복 체크
def check_duplicate_username(username):
    # 중복확인하는데 사용자 이름을 입력하지 않은 경우
    if username=='':
        return 5
    # 예외처리
    try:
        with open("users.json", "r") as file:
            users = json.load(file)
            for user in users:
                # 중복된 이름 존재
                if user["username"] == username:
                    return True
    # 시스템 에러           
    except FileNotFoundError:
        return False
    # 중복된 이름 없음
    return False

def open_join_window(window):
    join_window = customtkinter.CTkToplevel()
    join_window.title("회원가입")
    join_window.geometry("400x500")
    join_window.config(background=bgColor)
    signUpTextImg=customtkinter.CTkImage(light_image=Image.open("signup.png"),
                               dark_image=Image.open("signup.png"),
                               size=(250,250))
    # title_label = tkinter.Label(join_window, text="회원가입", background=bgColor,width=20, height=2, font=("맑은 고딕", 24, "bold"))
    # title_label.pack()
    title_label = customtkinter.CTkLabel(join_window,text="", bg_color=bgColor,image=signUpTextImg)
    title_label.place(relx=0.5,rely=0.2,anchor="center")
    username_label = tkinter.Label(join_window, text="사용자 이름:",background=bgColor)
    username_label.place(relx=0.5,rely=0.35,anchor="center")

    global username_entry
    username_entry = customtkinter.CTkEntry(join_window, placeholder_text="영어로 입력하세요",fg_color=bgColor,border_color=fgColor)
    username_entry.place(relx=0.5,rely=0.4,anchor="center")

    # 중복 확인 버튼 추가
    check_button = customtkinter.CTkButton(join_window,width=20, height=2,text="중복 확인",bg_color=bgColor,fg_color=fgColor,hover_color=hoverColor, command=lambda: check_duplicate(username_entry.get()))
    check_button.place(relx=0.85, rely=0.4, anchor=tkinter.E)

    password_label = tkinter.Label(join_window, text="비밀번호 입력:",background=bgColor)
    password_label.place(relx=0.5,rely=0.45,anchor="center")

    global password_entry
    password_entry = customtkinter.CTkEntry(join_window, fg_color=bgColor,border_color=fgColor,show="*")
    password_entry.place(relx=0.5,rely=0.5,anchor="center")

    confirm_password_label = tkinter.Label(join_window, text="비밀번호 재확인:",background=bgColor)
    confirm_password_label.place(relx=0.5,rely=0.55,anchor="center")

    global confirm_password_entry
    confirm_password_entry = customtkinter.CTkEntry(join_window,fg_color=bgColor,border_color=fgColor, show="*")
    confirm_password_entry.place(relx=0.5,rely=0.6,anchor="center")

    birthday_label = tkinter.Label(join_window, text="생년월일(YYMMDD):",background=bgColor)
    birthday_label.place(relx=0.5,rely=0.65,anchor="center")

    global birthday_entry
    birthday_entry = customtkinter.CTkEntry(join_window,fg_color=bgColor,border_color=fgColor)
    birthday_entry.place(relx=0.5,rely=0.7,anchor="center")

    join_button = customtkinter.CTkButton(join_window, text="회원가입", bg_color=bgColor,fg_color=fgColor,hover_color=hoverColor,command=join)
    join_button.place(relx=0.5,rely=0.8,anchor="center")

    close_button = customtkinter.CTkButton(join_window, text="닫기", width=20,height=10,bg_color=bgColor,fg_color=fgColor,hover_color=hoverColor,command=join_window.destroy)
    close_button.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

    def check_duplicate(username):
        if check_duplicate_username(username)==True:
            tkinter.messagebox.showinfo("에러", "이미 사용 중인 사용자 이름입니다.")
        elif check_duplicate_username(username)==False:
            tkinter.messagebox.showerror("알림", "사용 가능한 사용자 이름입니다.")
        else:
            tkinter.messagebox.showerror("에러", "사용자 이름을 입력하시오.")

    join_window.mainloop()
