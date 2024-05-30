import tkinter as tk
from tkinter import messagebox
import json
from word_test import WordTestWindow
from level_test import LevelTestWindow
import customtkinter 
from customtkinter import *
from PIL import Image

# class TestWindow:
#     def __init__(self):
#         self.bgColor = "#FFDFB9"
#         self.fgColor = "#A4193D"
#         self.hoverColor = "#C850C0"

#     def open_test_window(self, user):
#         self.test_window = customtkinter.CTkToplevel()
#         self.test_window.title("테스트")
#         self.test_window.geometry("400x500+100+100")
#         self.test_window.resizable(False, False)
#         self.test_window.config(background=self.bgColor)

#         test_label = tk.Label(self.test_window, text="진행할 테스트를 골라주세요!", background=self.bgColor, font=("맑은 고딕", 14))
#         test_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

#         wordtest_button = customtkinter.CTkButton(self.test_window, text="단어테스트", width=80, height=200, command=self.start_word_test, bg_color=self.fgColor, fg_color=self.fgColor, hover_color=self.hoverColor)
#         wordtest_button.place(relx=0.3, rely=0.4, anchor=tk.CENTER)

#         wordleveltest_button = customtkinter.CTkButton(self.test_window, text="레벨테스트", width=80, height=200, command=lambda: self.start_level_test(user), bg_color=self.fgColor, fg_color=self.fgColor, hover_color=self.hoverColor)
#         wordleveltest_button.place(relx=0.7, rely=0.4, anchor=tk.CENTER)

#         close_button = customtkinter.CTkButton(self.test_window, text="닫기", width=20, height=10, command=self.test_window.destroy, bg_color=self.fgColor, fg_color=self.fgColor, hover_color=self.hoverColor)
#         close_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

#         self.test_window.attributes("-topmost", True)
#         self.test_window.after(100, lambda: self.test_window.attributes("-topmost", False))
#         self.test_window.mainloop()

#     def start_word_test(self):
#         word_test = WordTestWindow()
#         word_test.open_wordtest_window()
    
#     def start_level_test(self, user):
#         level_test = LevelTestWindow()
#         level_test.open_wordleveltest_window(user)



class TestWindow:
    def __init__(self):
        self.bgColor = "#FFDFB9"
        self.fgColor = "#A4193D"
        self.hoverColor = "#C850C0"

    def open_test_window(self, user):
        self.test_window = customtkinter.CTkToplevel()
        self.test_window.title("테스트")
        self.test_window.geometry("400x500+100+100")
        self.test_window.resizable(False, False)
        self.test_window.config(background=self.bgColor)

        test_label = tk.Label(self.test_window, text="진행할 테스트를 골라주세요!", background=self.bgColor, font=("맑은 고딕", 14))
        test_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        wordtest_button = customtkinter.CTkButton(self.test_window, text="단어테스트", width=80, height=200, command=self.start_word_test, bg_color=self.fgColor, fg_color=self.fgColor, hover_color=self.hoverColor)
        wordtest_button.place(relx=0.3, rely=0.4, anchor=tk.CENTER)

        wordleveltest_button = customtkinter.CTkButton(self.test_window, text="레벨테스트", width=80, height=200, command=lambda:self.start_level_test(user), bg_color=self.fgColor, fg_color=self.fgColor, hover_color=self.hoverColor)
        wordleveltest_button.place(relx=0.7, rely=0.4, anchor=tk.CENTER)

        close_button = customtkinter.CTkButton(self.test_window, text="닫기", width=20, height=10, command=self.test_window.destroy, bg_color=self.fgColor, fg_color=self.fgColor, hover_color=self.hoverColor)
        close_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

        self.test_window.attributes("-topmost", True)
        self.test_window.after(100, lambda: self.test_window.attributes("-topmost", False))
        self.test_window.mainloop()

    def start_word_test(self):
        word_test = WordTestWindow()
        word_test.open_wordtest_window()

    def start_level_test(self, user):
        level_test = LevelTestWindow()
        level_test.open_wordleveltest_window(user)


