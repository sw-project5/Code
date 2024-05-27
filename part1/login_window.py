import tkinter
from tkinter import messagebox
import json
from join_window import open_join_window
from level_test_window import open_level_test_window
from user_window import open_user_window
from manager_window import open_manager_window
from password_reset_window import open_password_reset_window  # 비밀번호 찾기 기능을 가져옴
import customtkinter 
from customtkinter import *
from PIL import Image
#기본 색상
bgColor="#FFDFB9"
fgColor="#A4193D"
hoverColor="#C850C0"

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
            return user
    return False

def open_login_window(window):
    login_window = customtkinter.CTkToplevel()
    login_window.title("로그인")
    login_window.geometry("400x500")
    login_window.config(background=bgColor)
    loginTextImg=customtkinter.CTkImage(light_image=Image.open("Login.png"),
                               dark_image=Image.open("Login.png"),
                               size=(250,250))
    login_window.grid_columnconfigure(0, weight=1)
    login_window.grid_columnconfigure(1, weight=1)

    # title_label = tkinter.Label(login_window, text="LOGIN", width=20, height=2, font=("맑은 고딕", 24, "bold"), background=bgColor)
    # title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
    title_label = customtkinter.CTkLabel(login_window,text="", bg_color=bgColor,image=loginTextImg)
    title_label.place(relx=0.5,rely=0.2,anchor="center")
    img = customtkinter.CTkImage(light_image=Image.open("id_wine.png"), dark_image=Image.open("id_wine.png"), size=(50, 50))
    username_label = customtkinter.CTkLabel(login_window, text="", bg_color=bgColor, image=img)
    username_label.place(relx=0.25,rely=0.35,anchor="center")

    username_entry = customtkinter.CTkEntry(login_window, placeholder_text="사용자 이름 입력..", fg_color=bgColor,border_color=fgColor)
    username_entry.place(relx=0.5,rely=0.35,anchor="center")

    my_img = customtkinter.CTkImage(light_image=Image.open("password2.png"), dark_image=Image.open("password2.png"), size=(50, 50))
    password_label = customtkinter.CTkLabel(login_window, text="", bg_color=bgColor, image=my_img)
    password_label.place(relx=0.25,rely=0.45,anchor="center")

    password_entry = customtkinter.CTkEntry(login_window, placeholder_text="비밀번호 입력..", fg_color=bgColor, border_color=fgColor,show="*")
    password_entry.place(relx=0.5,rely=0.45,anchor="center")

    def login():
        username = username_entry.get()
        password = password_entry.get()

        user_data = load_user_data()

        user = validate_login(username, password, user_data)

        if user:
            
            login_window.destroy()

            if user.get('firstlogin', True):
                user['firstlogin'] = False
                # 변경된 사용자 정보를 파일에 저장
                with open('users.json', 'w') as file:
                    json.dump(user_data, file, indent=4)
                messagebox.showinfo("첫 로그인 성공", "레벨 확인 테스트로 이동합니다.")
                open_level_test_window(username)  # 레벨 확인 테스트 함수 호출  

            elif user.get('level')=="admin":
                messagebox.showinfo("관리자 로그인 성공","관리자님 환영합니다.")
                open_manager_window()
            
            else:
                messagebox.showinfo("로그인 성공", "로그인에 성공했습니다.")
                open_user_window(user)
        else:
            messagebox.showerror("로그인 실패", "잘못된 사용자 이름 또는 비밀번호입니다.")

    login_button = customtkinter.CTkButton(login_window, text="로그인", bg_color=bgColor, corner_radius=32, fg_color=fgColor, hover_color=hoverColor, command=login)
    login_button.place(relx=0.5,rely=0.6,anchor="center")

    join_button = customtkinter.CTkButton(login_window, text="회원가입", bg_color=bgColor,fg_color=fgColor,hover_color=hoverColor,corner_radius=32, command=lambda: open_join_window(window))
    join_button.place(relx=0.5,rely=0.7,anchor="center")

    password_reset_button = customtkinter.CTkButton(login_window, text="비밀번호 찾기", bg_color=bgColor,fg_color=fgColor,hover_color=hoverColor,corner_radius=32, command=open_password_reset_window)
    password_reset_button.place(relx=0.5,rely=0.8,anchor="center")

    close_button = customtkinter.CTkButton(login_window, text="닫기", width=20,height=10,bg_color=bgColor,fg_color=fgColor,hover_color=hoverColor,command=login_window.destroy)
    close_button.place(relx=0.5,rely=0.9,anchor="center")

    login_window.mainloop()
