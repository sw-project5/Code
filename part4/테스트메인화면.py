#테스트 누르면 나오는 화면
import tkinter
from tkinter import *
from 단어테스트 import open_wordtest_window
from 단어레벨테스트 import open_wordleveltest_window


def open_test_window():
  

  window = Tk()
  window.title("테스트")
  window.config(padx=30, pady=10)

  wordtest_button = tkinter.Button(window, text="단어테스트", command=open_wordtest_window)
  wordtest_button.pack(pady=(0, 10))

  wordleveltest_button = tkinter.Button(window, text="레벨테스트", command=open_wordleveltest_window)
  wordleveltest_button.pack()

  window.mainloop()
