import tkinter
from tkinter import messagebox
import json
from datetime import datetime
# from login_window import open_login_window


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
        'firstlogin':True,
        'level':'iron'
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
    join_window = tkinter.Tk()
    join_window.title("회원가입")
    join_window.geometry("400x500")

    title_label = tkinter.Label(join_window, text="회원가입", width=20, height=2, font=("맑은 고딕", 24, "bold"))
    title_label.pack()

    username_label = tkinter.Label(join_window, text="사용자 이름:")
    username_label.pack()

    global username_entry
    username_entry = tkinter.Entry(join_window)
    username_entry.pack()

    # 중복 확인 버튼 추가
    check_button = tkinter.Button(join_window, text="중복 확인", command=lambda: check_duplicate(username_entry.get()))
    check_button.pack()

    password_label = tkinter.Label(join_window, text="비밀번호 입력:")
    password_label.pack()

    global password_entry
    password_entry = tkinter.Entry(join_window, show="*")
    password_entry.pack()

    confirm_password_label = tkinter.Label(join_window, text="비밀번호 재확인:")
    confirm_password_label.pack()

    global confirm_password_entry
    confirm_password_entry = tkinter.Entry(join_window, show="*")
    confirm_password_entry.pack()

    birthday_label = tkinter.Label(join_window, text="생년월일(YYMMDD):")
    birthday_label.pack()

    global birthday_entry
    birthday_entry = tkinter.Entry(join_window)
    birthday_entry.pack()

    join_button = tkinter.Button(join_window, text="회원가입", command=join)
    join_button.pack()

    close_button = tkinter.Button(join_window, text="닫기", command=join_window.destroy)
    close_button.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

    def check_duplicate(username):
        if check_duplicate_username(username)==True:
            tkinter.messagebox.showinfo("에러", "이미 사용 중인 사용자 이름입니다.")
        elif check_duplicate_username(username)==False:
            tkinter.messagebox.showerror("알림", "사용 가능한 사용자 이름입니다.")
        else:
            tkinter.messagebox.showerror("에러", "사용자 이름을 입력하시오.")