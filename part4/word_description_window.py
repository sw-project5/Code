
import tkinter
from tkinter import font as tkfont 
import customtkinter 
from customtkinter import *
from PIL import Image
#기본 색상
bgColor="#FFDFB9"
fgColor="#A4193D"
hoverColor="#C850C0"

def open_description_window(window):
    # 새로운 창 생성
    description_window = customtkinter.CTkToplevel(window)
    
    description_window.title("단어장 설명")
    description_window.geometry("400x500")
    description_window.resizable(0, 0)
    description_window.config(background=bgColor)

    title_label = customtkinter.CTkLabel(description_window, text="TOEICVOCAMACA", text_color=fgColor, width=20, height=2, font=("맑은 고딕", 24, "bold"), bg_color=bgColor)
    title_label.pack()

    messages = [
        ("토익단어장", "안녕하세요! TOEICVOCAMACA 입니다!"),
        ("사용자", "안녕하세요!\n어떤 토익단어장인가요?"),
        ("토익단어장", "주 사용자인 대학생을 위해 토익 영단어를 쉽게 외울 수 있도록 토익 단어 및 학습 기능을 제공합니다!"),
        ("사용자", "다른 영단어장과의 차이점이 있나요?"),
        ("토익단어장", "각종 테스트 및 레벨 시스템을 도입한 재밌는 영단어장입니다."),
        ("사용자", "레벨은 어떻게 구성되어있나요?"),
        ("토익단어장", "처음 회원가입 시 레벨은 '아이언'이고, '브론즈'~'플레티넘'레벨이 있습니다.")
    ]

    # 각 메시지에 대한 라벨 생성 및 배치
    for i, (sender, message) in enumerate(messages):
        if sender == "사용자":
            label = customtkinter.CTkLabel(description_window, text=message, text_color=fgColor, font=("맑은 고딕", 12,"bold"), anchor="w", wraplength=300,
                                           justify="right", bg_color="white",   corner_radius=32)
            label.place(relx=0.9, rely=0.2 + i * 0.1, anchor=tkinter.E)
        else:
            label = customtkinter.CTkLabel(description_window, text=message, text_color=fgColor, font=("맑은 고딕", 12,"bold"), anchor="e", wraplength=300,
                                           justify="left", bg_color="white",   corner_radius=32)
            label.place(relx=0.1, rely=0.2 + i * 0.1, anchor=tkinter.W)

    close_button = customtkinter.CTkButton(description_window, text="닫기", command=description_window.destroy,
                                           bg_color=bgColor, fg_color=fgColor, hover_color=hoverColor)
    close_button.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

    description_window.attributes("-topmost", True)
    description_window.after(100, lambda: description_window.attributes("-topmost", False))
    description_window.mainloop()
