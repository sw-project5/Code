import tkinter as tk
from tkinter import messagebox
import wordDB  # wordDB.py 파일을 가져옵니다.
import json
import os

class ManagerWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Word Manager")
        self.window.geometry("450x500+100+100")
        self.window.resizable(False, False)

        self.words = wordDB.words

        self.create_widgets()

    def update_word_listbox(self):
        try:
            self.word_listbox.delete(0, tk.END)
            for word in self.words:
                for eng, kor in word.items():
                    self.word_listbox.insert(tk.END, f"{eng}: {kor}")
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
                    self.word_entry.delete(0, tk.END)
                    self.meaning_entry.delete(0, tk.END)
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
                    self.word_entry.delete(0, tk.END)
                    self.meaning_entry.delete(0, tk.END)
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
                    self.word_entry.delete(0, tk.END)
                    self.meaning_entry.delete(0, tk.END)
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
                    self.word_entry.delete(0, tk.END)
                    self.meaning_entry.delete(0, tk.END)
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
                    self.word_entry.delete(0, tk.END)
                    self.meaning_entry.delete(0, tk.END)
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

        tk.Label(self.window, text="Word:").grid(row=1, column=0)
        self.word_entry = tk.Entry(self.window)
        self.word_entry.grid(row=1, column=1, columnspan=2)

        tk.Label(self.window, text="Meaning:").grid(row=2, column=0)
        self.meaning_entry = tk.Entry(self.window)
        self.meaning_entry.grid(row=2, column=1, columnspan=2)

        button_frame = tk.Frame(self.window)
        button_frame.grid(row=3, column=0, columnspan=3)

        add_button = tk.Button(button_frame, text="Add", command=self.add_word)
        add_button.grid(row=0, column=0)

        update_button = tk.Button(button_frame, text="Update", command=self.update_word)
        update_button.grid(row=0, column=1)

        delete_button = tk.Button(button_frame, text="Delete", command=self.delete_word)
        delete_button.grid(row=0, column=2)

        logout_button = tk.Button(button_frame, text="Logout", command=self.logout)
        logout_button.grid(row=0, column=3)

        complete_button = tk.Button(self.window, text="Complete", command=self.save_words_to_file)
        complete_button.grid(row=4, column=0, columnspan=3)
        self.window.mainloop()
