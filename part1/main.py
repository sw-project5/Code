import tkinter as tk
from user_manager import UserManager  # UserManager는 사용자 관리를 위한 클래스로 가정
from word_description_window import open_description_window  # 분리된 함수 임포트
from main_page import MainPage
from login_page import LoginPage
from signup_page import SignupPage

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("단어장 앱")
        self.geometry("400x400")

        self.user_manager = UserManager("users.json")  # 사용자 정보를 저장할 파일

        self.current_user = None

        self.show_main_page()

    def show_main_page(self):
        self.clear_window()
        self.main_page = MainPage(self, self.show_login_page, lambda: open_description_window(self))
        self.main_page.pack(fill="both", expand=True)

    def show_login_page(self):
        self.clear_window()
        self.login_page = LoginPage(self, self.on_login_success, self.show_signup_page, self.user_manager)
        self.login_page.pack(fill="both", expand=True)

    def show_signup_page(self):
        self.clear_window()
        self.signup_page = SignupPage(self, self.show_login_page, self.user_manager)
        self.signup_page.pack(fill="both", expand=True)

    def on_login_success(self, username):
        self.current_user = username
        self.show_word_list_page()

    def on_logout(self):
        self.current_user = None
        self.show_login_page()

    def show_word_list_page(self):
        self.clear_window()
        tk.Label(self, text=f"환영합니다, {self.current_user}님!").pack()  # 로그인 후 사용자 이름 표시
        tk.Button(self, text="단어장 설명", command=lambda: open_description_window(self)).pack()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.pack_forget()

if __name__ == "__main__":
    app = App()
    app.mainloop()
