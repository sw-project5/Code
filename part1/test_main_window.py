
#테스트 누르면 나오는 화면
import tkinter
from tkinter import *
from word_test import open_wordtest_window
from level_test import open_wordleveltest_window
import json
import customtkinter 
from customtkinter import *
from PIL import Image

# 기본 색상
bgColor = "#FFDFB9"
fgColor = "#A4193D"
hoverColor = "#C850C0"

def load_user_data(filepath='users.json'):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []
    
    


def open_test_window(user):
    test_window = customtkinter.CTkToplevel()
    test_window.title("테스트")
    test_window.geometry("400x500+100+100")
    test_window.resizable(False, False)
    test_window.config(background=bgColor)

    test_label=tkinter.Label(test_window, text="진행할 테스트를 골라주세요!",background=bgColor,font=("맑은 고딕",14))
    test_label.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

    wordtest_button = customtkinter.CTkButton(test_window, text="단어테스트", width=80, height=200, command=open_wordtest_window,bg_color=fgColor,fg_color=fgColor,hover_color=hoverColor)
    wordtest_button.place(relx=0.3, rely=0.4, anchor=tkinter.CENTER)

    wordleveltest_button = customtkinter.CTkButton(test_window, text="레벨테스트", width=80, height=200, command=lambda: open_wordleveltest_window(user),bg_color=fgColor,fg_color=fgColor,hover_color=hoverColor)
    wordleveltest_button.place(relx=0.7, rely=0.4, anchor=tkinter.CENTER)

    close_button = customtkinter.CTkButton(test_window, text="닫기",width=20,height=10, command=test_window.destroy,bg_color=fgColor,fg_color=fgColor,hover_color=hoverColor)
    close_button.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

    test_window.attributes("-topmost", True)
    test_window.after(100, lambda: test_window.attributes("-topmost", False))
    test_window.mainloop()
