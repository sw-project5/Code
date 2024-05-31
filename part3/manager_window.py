import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import wordDB  # wordDB.py 파일을 가져옵니다.
import json
import os
import customtkinter 
from customtkinter import *
from user_window import UserWindow


class ManagerWindow:
    def __init__(self):
        self.bgColor="#FFDFB9"
        self.fgColor="#A4193D"
        self.hoverColor="#C850C0"
        self.window = customtkinter.CTkToplevel()
        self.window.title("Word Manager")
        self.window.geometry("600x700+100")
        self.window.resizable(False, False)
        self.window.config(background=self.bgColor)

        self.words = wordDB.words

        self.window.attributes("-topmost", True)
        self.window.update()  # Update the window to apply the topmost attribute
        self.window.attributes("-topmost", False)

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
        

        self.word_listbox = tk.Listbox(self.window,height=15, width=60)
        self.word_listbox.pack(pady=10)
        self.word_listbox.config(background=self.bgColor)

        self.start_index =  0
        self.end_index = len(self.words)

        self.canvas = tk.Canvas(self.word_listbox)
        self.canvas.config(background=self.bgColor)
        self.scrollbar = ttk.Scrollbar(self.word_listbox, orient="vertical", command=self.canvas.yview)

        self.word_frame = tk.Frame(self.canvas)
        self.word_frame.config(background=self.bgColor)
        self.word_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
                )
        )    
        
        self.canvas.create_window((0, 0), window=self.word_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set,background=self.bgColor)
        self.canvas.config(background=self.bgColor,width=350,height=300)
        
        for i, self.word in enumerate(self.words[self.start_index:self.end_index], start=self.start_index):
            for english_word, meaning in self.word.items():
                self.word_label = tk.Label(self.word_frame, text=f"{english_word}: {meaning}", anchor='w', justify='left', wraplength=360,background=self.bgColor,font=('맑은 고딕',14))
                self.word_label.pack(anchor="w", padx=10, pady=5)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.update_word_listbox()

        # 단어 추가/수정/삭제를 위한 엔트리와 버튼
        self.word_frame=customtkinter.CTkFrame(self.window,bg_color=self.bgColor,fg_color=self.bgColor)
        self.word_frame.pack(pady=10)
        self.word_label=customtkinter.CTkLabel(self.word_frame, text="Word:",text_color="black",bg_color=self.bgColor)
        self.word_label.pack(side="left",padx=14)
        self.word_entry = customtkinter.CTkEntry(self.word_frame,bg_color=self.bgColor)
        self.word_entry.pack(side="left",padx=14)

        self.meaning_frame=customtkinter.CTkFrame(self.window,bg_color=self.bgColor,fg_color=self.bgColor)
        self.meaning_frame.pack(pady=10)
        self.meaning_label=customtkinter.CTkLabel(self.meaning_frame, text="Meaning:",text_color="black",bg_color=self.bgColor)
        self.meaning_label.pack(side="left",padx=5)
        self.meaning_entry = customtkinter.CTkEntry(self.meaning_frame,bg_color=self.bgColor)
        self.meaning_entry.pack(side="left",padx=5)

        self.button_frame = customtkinter.CTkFrame(self.window,bg_color=self.bgColor,fg_color=self.bgColor)
        self.button_frame.pack(pady=10)
        self.add_button = customtkinter.CTkButton(self.button_frame, text="추가",text_color="white",bg_color=self.bgColor,fg_color=self.fgColor, corner_radius=32,command=lambda: self.add_word())
        self.add_button.pack(side="left")
        self.update_button = customtkinter.CTkButton(self.button_frame, text="수정", text_color="white",bg_color=self.bgColor,fg_color=self.fgColor,corner_radius=32,command=lambda: self.update_word())
        self.update_button.pack(side="left",padx=7)
        self.delete_button = customtkinter.CTkButton(self.button_frame, text="삭제",text_color="white",bg_color=self.bgColor,fg_color=self.fgColor ,corner_radius=32,command=lambda: self.delete_word())
        self.delete_button.pack()
        # 완료 버튼을 추가합니다
        self.complete_button = customtkinter.CTkButton(self.window, text="저장", text_color="white",bg_color=self.bgColor,fg_color=self.fgColor,hover_color=self.hoverColor,corner_radius=32,command=lambda: self.save_words_to_file())
        self.complete_button.pack()

        self.logout_button = customtkinter.CTkButton(self.window, text="로그아웃", text_color="white",bg_color=self.bgColor, fg_color=self.fgColor, hover_color=self.hoverColor, corner_radius=32, command=self.logout)
        self.logout_button.pack(pady=10)

        self.window.attributes("-topmost", True)
        self.window.lift()
        self.window.after(100, lambda: self.window.attributes("-topmost", False))



        self.window.mainloop()
