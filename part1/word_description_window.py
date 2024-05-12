# description_window.py

import tkinter

def open_description_window(window):
    # 새로운 창 생성
    description_window = tkinter.Toplevel(window)
    description_window.title("단어장 설명")
    description_window.geometry("400x300")
    description_window.resizable(0,0)

    # 단어장 설명 창 내용 추가
    description_label = tkinter.Label(description_window, text="단어장 설명 페이지입니다.")
    description_label.pack()
