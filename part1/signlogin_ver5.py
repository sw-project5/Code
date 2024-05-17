import tkinter as tk
from tkinter import messagebox
from user_manager import UserManager  # UserManager는 사용자 관리를 위한 클래스로 가정
from word_description_window import open_description_window  # 분리된 함수 임포트

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
        tk.Button(self, text="단어장 설명", command=lambda: open_description_window(self)).pack()  # 단어장 설명 버튼 추가

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()

        if not username or not password:
            messagebox.showerror("오류", "사용자 이름과 비밀번호를 입력해주세요.")
            return

        if self.user_manager.check_user(username, password):
            self.login_success_callback()
        else:
            messagebox.showerror("오류", "잘못된 사용자 이름 또는 비밀번호입니다.")


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


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("단어장 앱")
        self.geometry("400x400")

        self.user_manager = UserManager("users.json")  # 사용자 정보를 저장할 파일

        self.current_user = None

        self.show_login_page()

    def show_login_page(self):
        self.clear_window()
        self.login_page = LoginPage(self, self.on_login_success, self.show_signup_page, self.user_manager)
        self.login_page.pack(fill="both", expand=True)

    def show_signup_page(self):
        self.clear_window()
        self.signup_page = SignupPage(self, self.show_login_page, self.user_manager)
        self.signup_page.pack(fill="both", expand=True)

    def on_login_success(self):
        self.show_word_list_page()

    def on_logout(self):
        self.current_user = None
        self.show_login_page()

    def show_word_list_page(self):
        self.clear_window()
        tk.Button(self, text="단어장 설명", command=lambda: open_word_description_window(self)).pack()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.pack_forget()

if __name__ == "__main__":
    app = App()
    app.mainloop()
