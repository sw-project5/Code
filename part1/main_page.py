import tkinter as tk

class MainPage(tk.Frame):
    def __init__(self, parent, show_login_page_callback, show_description_callback):
        super().__init__(parent)

        self.show_login_page_callback = show_login_page_callback
        self.show_description_callback = show_description_callback

        tk.Button(self, text="로그인", command=self.show_login_page_callback).pack()
        tk.Button(self, text="단어장 설명", command=self.show_description_callback).pack()
