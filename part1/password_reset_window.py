import tkinter
from tkinter import messagebox
import json
import customtkinter 
from customtkinter import *
from PIL import Image

class PasswordResetWindow:
    def __init__(self, master):
        self.master = master
        self.password_reset_window = None

    def load_user_data(self, filepath='users.json'):
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def open_password_reset_window(self):
        try:
            self.password_reset_window = customtkinter.CTkToplevel()
            self.password_reset_window.title("비밀번호 찾기")
            self.password_reset_window.geometry("400x500")
            self.password_reset_window.config(background="#FFDFB9")
            
            findPasswordImg = customtkinter.CTkImage(light_image=Image.open("password_find.png"),
                                                     dark_image=Image.open("password_find.png"),
                                                     size=(300, 300))
            title_label = customtkinter.CTkLabel(self.password_reset_window, text="", bg_color="#FFDFB9", image=findPasswordImg)
            title_label.place(relx=0.5, rely=0.2, anchor="center")

            username_label = tkinter.Label(self.password_reset_window, text="사용자 이름:", background="#FFDFB9")
            username_label.place(relx=0.5, rely=0.3, anchor="center")

            self.username_entry = customtkinter.CTkEntry(self.password_reset_window, corner_radius=0, text_color="black", fg_color="#FFDFB9", border_color="#A4193D")
            self.username_entry.place(relx=0.5, rely=0.35, anchor="center")

            birthday_label = tkinter.Label(self.password_reset_window, text="생년월일(YYMMDD):", background="#FFDFB9")
            birthday_label.place(relx=0.5, rely=0.4, anchor="center")

            self.birthday_entry = customtkinter.CTkEntry(self.password_reset_window, corner_radius=0, text_color="black", fg_color="#FFDFB9", border_color="#A4193D")
            self.birthday_entry.place(relx=0.5, rely=0.45, anchor="center")

            reset_button = customtkinter.CTkButton(self.password_reset_window, text="비밀번호 찾기", bg_color="#FFDFB9", fg_color="#A4193D", hover_color="#C850C0", corner_radius=32, command=self.reset_password)
            reset_button.place(relx=0.5, rely=0.8, anchor="center")

            # 창 순서 조정 코드 추가
            self.password_reset_window.attributes("-topmost", True)
            self.password_reset_window.after(100, lambda: self.password_reset_window.attributes("-topmost", False))

            self.password_reset_window.mainloop()
        # 예외 처리 코드 추가
        except Exception as e:
            messagebox.showerror("에러", "일시적인 오류가 발생했습니다. 나중에 다시 시도해주세요.")

    def reset_password(self):
        username = self.username_entry.get()
        birthday = self.birthday_entry.get()

        user_data = self.load_user_data()

        for user in user_data:
            if user['username'] == username and user['birthday'] == birthday:
                messagebox.showinfo("비밀번호 찾기", f"비밀번호: {user['password']}")
                self.password_reset_window.destroy()
                return

        messagebox.showerror("에러", "일치하는 정보를 찾을 수 없습니다.")

