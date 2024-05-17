import tkinter as tk
from tkinter import messagebox

class SignupPage(tk.Frame):
    def __init__(self, parent, show_login_page_callback, user_manager):
        super().__init__(parent)

        self.user_manager = user_manager
        self.show_login_page_callback = show_login_page_callback

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.confirm_password_var = tk.StringVar()
        self.birthdate_var = tk.StringVar()  # 생년월일을 YYMMDD 형식으로 저장할 변수

        # 레이블 및 입력 위젯 생성
        tk.Label(self, text="사용자 이름:").pack()
        self.username_entry = tk.Entry(self, textvariable=self.username_var)
        self.username_entry.pack()

        tk.Label(self, text="비밀번호:").pack()
        self.password_entry = tk.Entry(self, textvariable=self.password_var, show="*")
        self.password_entry.pack()

        tk.Label(self, text="비밀번호 재확인:").pack()
        self.confirm_password_entry = tk.Entry(self, textvariable=self.confirm_password_var, show="*")
        self.confirm_password_entry.pack()

        tk.Label(self, text="생년월일 (YYMMDD):").pack()  # 생년월일 레이블 추가
        self.birthdate_entry = tk.Entry(self, textvariable=self.birthdate_var)
        self.birthdate_entry.pack()

        tk.Button(self, text="회원가입", command=self.signup).pack()

    def signup(self):
        username = self.username_var.get()
        password = self.password_var.get()
        confirm_password = self.confirm_password_var.get()
        birthdate = self.birthdate_var.get()  # 입력받은 생년월일 YYMMDD 형식으로 가져오기

        if not username or not password or not birthdate:
            messagebox.showerror("오류", "사용자 이름, 비밀번호, 생년월일을 모두 입력해주세요.")
            return

        if password != confirm_password:
            messagebox.showerror("오류", "비밀번호가 일치하지 않습니다.")
            return

        # 사용자 등록
        success = self.user_manager.add_user(username, password, birthdate)
        if success:
            messagebox.showinfo("성공", "회원가입이 완료되었습니다!")
            self.show_login_page_callback()
        else:
            messagebox.showerror("오류", "이미 존재하는 사용자 이름입니다.")
