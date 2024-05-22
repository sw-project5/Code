#유저 화면

import tkinter
from tkinter import *
from 테스트메인화면 import open_test_window

window = Tk()
window.title("유저 화면")
window.config(padx=30, pady=10)

test_button = tkinter.Button(window, text="테스트", command=open_test_window)
test_button.place(relx=0.5, rely=0.85, anchor=tkinter.CENTER)

window.mainloop()
