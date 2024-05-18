import tkinter
from tkinter import messagebox
import json
import customtkinter 
from customtkinter import *
def load_user_data(filepath='users.json'):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def open_password_reset_window():
    password_reset_window = customtkinter.CTk()
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

    password_reset_window.mainloop()

open_password_reset_window()