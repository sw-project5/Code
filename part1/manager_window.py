import customtkinter as ctk
from tkinter import messagebox
import wordDB  # wordDB.py 파일을 가져옵니다.
import json
import os
import tkinter as tk
# 색상 설정
bgColor = "#FFDFB9"
fgColor = "#A4193D"
hoverColor = "#C850C0"

class ManagerWindow:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Word Manager")
        self.window.geometry("450x500+100+100")
        self.window.resizable(False, False)
        self.window.config(background=bgColor)

        self.words = wordDB.words

        self.create_widgets()

    def update_word_listbox(self):
        try:
            self.word_listbox.delete(0, ctk.END)
            for word in self.words:
                for eng, kor in word.items():
                    self.word_listbox.insert(ctk.END, f"{eng}: {kor}")
        except Exception as e:
            messagebox.showerror("에러", "일시적인 오류가 발생했습니다. 나중에 다시 시도해주세요.")

    def add_word(self):
        try:
            eng = self.word_entry.get().strip()
            kor = self.meaning_entry.get().strip()
            if eng and kor:
                if any(eng in word for word in self.words):
                    messagebox.showwarning("Duplicate Error", "이미 존재하는 단어입니다.")
                else:
                    self.words.append({eng: kor})
                    self.update_word_listbox()
                    self.word_entry.delete(0, ctk.END)
                    self.meaning_entry.delete(0, ctk.END)
            else:
                messagebox.showwarning("Input Error", "단어와 뜻 모두 입력해주세요.")
        except Exception as e:
            messagebox.showerror("에러", "일시적인 오류가 발생했습니다. 나중에 다시 시도해주세요.")

    def update_word(self):
        try:
            selected = self.word_listbox.curselection()
            if selected:
                index = selected[0]
                eng = self.word_entry.get().strip()
                kor = self.meaning_entry.get().strip()
                if eng and kor:
                    self.words[index] = {eng: kor}
                    self.update_word_listbox()
                    self.word_entry.delete(0, ctk.END)
                    self.meaning_entry.delete(0, ctk.END)
                else:
                    messagebox.showwarning("Input Error", "단어와 뜻 모두 입력해주세요.")
            else:
                eng = self.word_entry.get().strip()
                kor = self.meaning_entry.get().strip()
                found = False
                for i, word in enumerate(self.words):
                    if eng in word:
                        self.words[i][eng] = kor
                        found = True
                        break
                if found:
                    self.update_word_listbox()
                    self.word_entry.delete(0, ctk.END)
                    self.meaning_entry.delete(0, ctk.END)
                else:
                    messagebox.showwarning("Word Not Found", "해당 단어는 존재하지 않습니다.")
        except Exception as e:
            messagebox.showerror("에러", "일시적인 오류가 발생했습니다. 나중에 다시 시도해주세요.")

    def delete_word(self):
        try:
            eng = self.word_entry.get().strip()
            kor = self.meaning_entry.get().strip()
            selected = self.word_listbox.curselection()
            if selected:
                index = selected[0]
                word = list(self.words[index].keys())[0]
                meaning = self.words[index][word]
                if word == eng and meaning == kor:
                    del self.words[index]
                    self.update_word_listbox()
                    self.word_entry.delete(0, ctk.END)
                    self.meaning_entry.delete(0, ctk.END)
                else:
                    messagebox.showwarning("Mismatch Error", "해당 단어와 뜻이 일치하지 않습니다.")
            else:
                found = False
                for i, word in enumerate(self.words):
                    if eng in word and word[eng] == kor:
                        del self.words[i]
                        found = True
                        break
                if found:
                    self.update_word_listbox()
                    self.word_entry.delete(0, ctk.END)
                    self.meaning_entry.delete(0, ctk.END)
                else:
                    messagebox.showwarning("Word Not Found", "해당 단어와 뜻이 일치하지 않습니다.")
        except Exception as e:
            messagebox.showerror("에러", "일시적인 오류가 발생했습니다. 나중에 다시 시도해주세요.")

    def save_words_to_file(self):
        try:
            words_data = {"words": self.words}
            with open('wordDB.py', 'w', encoding='utf-8') as file:
                file.write("words = ")
                json.dump(words_data["words"], file, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("에러", "일시적인 오류가 발생했습니다. 나중에 다시 시도해주세요.")

    def open_login_window(self):
        import login_window
        login_window.open_login_window(self.window)

    def logout(self):
        confirm = messagebox.askokcancel("로그아웃", "정말 로그아웃 하시겠습니까?")
        if confirm:
            logout=messagebox.askokcancel("로그아웃", "로그아웃 되었습니다.\n다시 로그인해주세요.")
            if logout:
                self.window.destroy()

    def create_widgets(self):
        self.word_listbox = tk.Listbox(self.window, height=10, width=50)
        self.word_listbox.grid(row=0, column=0, columnspan=3)
        self.update_word_listbox()

        ctk.CTkLabel(self.window, text="Word:", bg_color=bgColor).grid(row=1, column=0)
        self.word_entry = ctk.CTkEntry(self.window, width=250)
        self.word_entry.grid(row=1, column=1, columnspan=2)

        ctk.CTkLabel(self.window, text="Meaning:", bg_color=bgColor).grid(row=2, column=0)
        self.meaning_entry = ctk.CTkEntry(self.window, width=250)
        self.meaning_entry.grid(row=2, column=1, columnspan=2)

        button_frame = ctk.CTkFrame(self.window, bg_color=bgColor)
        button_frame.grid(row=3, column=0, columnspan=3, pady=10)

        add_button = ctk.CTkButton(button_frame, text="Add", command=self.add_word, 
                                   bg_color=bgColor, fg_color=fgColor, hover_color=hoverColor)
        add_button.grid(row=0, column=0, padx=5)

        update_button = ctk.CTkButton(button_frame, text="Update", command=self.update_word, 
                                      bg_color=bgColor, fg_color=fgColor, hover_color=hoverColor)
        update_button.grid(row=0, column=1, padx=5)

        delete_button = ctk.CTkButton(button_frame, text="Delete", command=self.delete_word, 
                                      bg_color=bgColor, fg_color=fgColor, hover_color=hoverColor)
        delete_button.grid(row=0, column=2, padx=5)

        complete_button = ctk.CTkButton(self.window, text="Complete", command=self.save_words_to_file, 
                                        bg_color=bgColor, fg_color=fgColor, hover_color=hoverColor)
        complete_button.grid(row=4, column=0, columnspan=3, pady=10)

        logout_button = ctk.CTkButton(self.window, text="Logout", command=self.logout, 
                                      bg_color=bgColor, fg_color=fgColor, hover_color=hoverColor)
        logout_button.grid(row=5, column=0, columnspan=3, pady=(10, 0))

        self.window.mainloop()


