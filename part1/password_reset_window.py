import tkinter
from tkinter import messagebox
import json
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

def open_password_reset_window():
    password_reset_window = customtkinter.CTkToplevel()
    password_reset_window.title("비밀번호 찾기")
    password_reset_window.geometry("400x500")
    password_reset_window.config(background=bgColor)
    findPasswordImg=customtkinter.CTkImage(light_image=Image.open("password_find.png"),
                               dark_image=Image.open("password_find.png"),
                               size=(300,300))
    title_label = customtkinter.CTkLabel(password_reset_window,text="", bg_color=bgColor,image=findPasswordImg)
    title_label.place(relx=0.5,rely=0.2,anchor="center")

    username_label = tkinter.Label(password_reset_window, text="사용자 이름:",background=bgColor)
    username_label.place(relx=0.5,rely=0.3,anchor="center")

    username_entry = customtkinter.CTkEntry(password_reset_window,fg_color=bgColor,border_color=fgColor)
    username_entry.place(relx=0.5,rely=0.35,anchor="center")

    birthday_label = tkinter.Label(password_reset_window, text="생년월일(YYMMDD):",background=bgColor)
    birthday_label.place(relx=0.5,rely=0.4,anchor="center")

    birthday_entry = customtkinter.CTkEntry(password_reset_window,fg_color=bgColor,border_color=fgColor)
    birthday_entry.place(relx=0.5,rely=0.45,anchor="center")

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

       

    reset_button = customtkinter.CTkButton(password_reset_window, text="비밀번호 찾기", bg_color=bgColor,fg_color=fgColor,hover_color=hoverColor,corner_radius=32,command=reset_password)
    reset_button.place(relx=0.5,rely=0.8,anchor="center")

    password_reset_window.mainloop()


