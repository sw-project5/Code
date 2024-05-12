import tkinter

def open_join_window(window):
    join_window = tkinter.Toplevel(window)
    join_window.title("회원가입")
    join_window.geometry("400x300")




# 로그인 버튼 눌렀을 시 로그인, 회원가입 둘 다 뜨는 문제 발생
# -> 아직 해결X