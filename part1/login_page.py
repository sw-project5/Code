import tkinter as tk
from tkinter import messagebox

class LoginPage(tk.Frame):
    def __init__(self, parent, login_success_callback, show_signup_page_callback, user_manager):
        super().__init__(parent)

        self.user_manager = user_manager
        self.login_success_callback = login_success_callback
        self.show_signup_page_callback = show_signup_page_callback

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        # 레이블 및 입력 위젯 생성
        tk.Label(self, text="사용자 이름:").pack()
        self.username_entry = tk.Entry(self, textvariable=self.username_var)
        self.username_entry.pack()

        tk.Label(self, text="비밀번호:").pack()
        self.password_entry = tk.Entry(self, textvariable=self.password_var, show="*")
        self.password_entry.pack()

        tk.Button(self, text="로그인", command=self.login).pack()
        tk.Button(self, text="회원가입", command=self.show_signup_page_callback).pack()

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()

        if not username or not password:
            messagebox.showerror("오류", "사용자 이름과 비밀번호를 입력해주세요.")
            return

        if self.user_manager.check_user(username, password):
            self.login_success_callback(username)  # 로그인 성공 시 사용자 이름 전달
        else:
            messagebox.showerror("오류", "잘못된 사용자 이름 또는 비밀번호입니다.")
