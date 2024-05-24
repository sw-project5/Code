#테스트 누르면 나오는 화면
import tkinter
from tkinter import *
from word_test import open_wordtest_window
from level_test import open_wordleveltest_window


def open_test_window(user):
    test_window = tkinter.Tk()
    test_window.title("테스트")
    test_window.geometry("400x500+100+100")
    test_window.resizable(False, False)

    test_label=tkinter.Label(test_window, text="진행할 테스트를 골라주세요!")
    test_label.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

    wordtest_button = tkinter.Button(test_window, text="단어테스트", width=8, height=10, command=open_wordtest_window)
    wordtest_button.place(relx=0.3, rely=0.5, anchor=tkinter.CENTER)

    wordleveltest_button = tkinter.Button(test_window, text="레벨테스트", width=8, height=10, command=lambda:open_wordleveltest_window(user))
    wordleveltest_button.place(relx=0.7, rely=0.5, anchor=tkinter.CENTER)

    close_button = tkinter.Button(test_window, text="닫기", command=test_window.destroy)
    close_button.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

    test_window.mainloop()