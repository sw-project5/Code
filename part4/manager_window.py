import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import wordDB  # wordDB.py 파일을 가져옵니다.
import json
import os
import customtkinter 
from customtkinter import *
from user_window import open_login_window
# 기본 색상
bgColor="#FFDFB9"
fgColor="#A4193D"
hoverColor="#C850C0"

def update_word_listbox(words, word_listbox):
    try:
        word_listbox.delete(0, tk.END)
        for word in words:
            for eng, kor in word.items():
                word_listbox.insert(tk.END, f"{eng}: {kor}")
    except Exception as e:
        messagebox.showerror("에러", "일시적인 오류가 발생했습니다. 나중에 다시 시도해주세요.")

def add_word(words, word_entry, meaning_entry, word_listbox):
    try:
        eng = word_entry.get().strip()
        kor = meaning_entry.get().strip()
        if eng and kor:
            if any(eng in word for word in words):
                messagebox.showwarning("Duplicate Error", "이미 존재하는 단어입니다.")
            else:
                words.append({eng: kor})
                update_word_listbox(words, word_listbox)
                word_entry.delete(0, tk.END)
                meaning_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "단어와 뜻 모두 입력해주세요.")
    except Exception as e:
        messagebox.showerror("에러", "일시적인 오류가 발생했습니다. 나중에 다시 시도해주세요.")

def update_word(words, word_entry, meaning_entry, word_listbox):
    try:
        selected = word_listbox.curselection()
        if selected:
            index = selected[0]
            eng = word_entry.get().strip()
            kor = meaning_entry.get().strip()
            if eng and kor:
                words[index] = {eng: kor}
                update_word_listbox(words, word_listbox)
                word_entry.delete(0, tk.END)
                meaning_entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Input Error", "단어와 뜻 모두 입력해주세요.")
        else:
            eng = word_entry.get().strip()
            kor = meaning_entry.get().strip()
            found = False
            for i, word in enumerate(words):
                if eng in word:
                    words[i][eng] = kor
                    found = True
                    break
            if found:
                update_word_listbox(words, word_listbox)
                word_entry.delete(0, tk.END)
                meaning_entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Word Not Found", "해당 단어는 존재하지 않습니다.")
    except Exception as e:
        messagebox.showerror("에러", "일시적인 오류가 발생했습니다. 나중에 다시 시도해주세요.")

def delete_word(words, word_entry, meaning_entry, word_listbox):
    try:
        eng = word_entry.get().strip()
        kor = meaning_entry.get().strip()
        selected = word_listbox.curselection()
        if selected:
            index = selected[0]
            word = list(words[index].keys())[0]
            meaning = words[index][word]
            if word == eng and meaning == kor:
                del words[index]
                update_word_listbox(words, word_listbox)
                word_entry.delete(0, tk.END)
                meaning_entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Mismatch Error", "해당 단어와 뜻이 일치하지 않습니다.")
        else:
            found = False
            for i, word in enumerate(words):
                if eng in word and word[eng] == kor:
                    del words[i]
                    found = True
                    break
            if found:
                update_word_listbox(words, word_listbox)
                word_entry.delete(0, tk.END)
                meaning_entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Word Not Found", "해당 단어와 뜻이 일치하지 않습니다.")
    except Exception as e:
        messagebox.showerror("에러", "일시적인 오류가 발생했습니다. 나중에 다시 시도해주세요.")

def save_words_to_file(words, file_path='wordDB.py'):
    try:
        words_data = {"words": words}
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write("words = ")
            json.dump(words_data["words"], file, ensure_ascii=False, indent=4)
    except Exception as e:
        messagebox.showerror("에러", "일시적인 오류가 발생했습니다. 나중에 다시 시도해주세요.")
# 전역 변수
words_per_page = 200

def open_manager_window():
    try:
        manager_window = customtkinter.CTkToplevel()
        manager_window.title("Word Manager")
        manager_window.geometry("450x500+100+100")
        manager_window.resizable(False, False)
        manager_window.config(background=bgColor)
        # 초기 단어 데이터
        words = wordDB.words

        manager_window.attributes("-topmost", True)
        manager_window.update()  # Update the window to apply the topmost attribute
        manager_window.attributes("-topmost", False)

        # 단어 목록 표시
        word_listbox = tk.Listbox(manager_window, height=15, width=60)
        word_listbox.pack(pady=10)
        word_listbox.config(background=bgColor)

        

        start_index =  0
        end_index = len(words)

        canvas = tk.Canvas(word_listbox)
        canvas.config(background=bgColor)
        scrollbar = ttk.Scrollbar(word_listbox, orient="vertical", command=canvas.yview)

        word_frame = tk.Frame(canvas)
        word_frame.config(background=bgColor)
        word_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
                )
        )    
        
        canvas.create_window((0, 0), window=word_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set,background=bgColor)
        canvas.config(background=bgColor,width=350,height=300)
        
        for i, word in enumerate(words[start_index:end_index], start=start_index):
            for english_word, meaning in word.items():
                word_label = tk.Label(word_frame, text=f"{english_word}: {meaning}", anchor='w', justify='left', wraplength=360,background=bgColor,font=('맑은 고딕',14))
                word_label.pack(anchor="w", padx=10, pady=5)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        # 초기 단어 목록 업데이트
        update_word_listbox(words, word_listbox)

        # 단어 추가/수정/삭제를 위한 엔트리와 버튼
        word_frame=customtkinter.CTkFrame(manager_window,bg_color=bgColor,fg_color=bgColor)
        word_frame.pack(pady=10)
        word_label=customtkinter.CTkLabel(word_frame, text="Word:",text_color="black",bg_color=bgColor)
        word_label.pack(side="left",padx=14)
        word_entry = customtkinter.CTkEntry(word_frame,bg_color=bgColor)
        word_entry.pack(side="left",padx=14)
        
        meaning_frame=customtkinter.CTkFrame(manager_window,bg_color=bgColor,fg_color=bgColor)
        meaning_frame.pack(pady=10)
        meaning_label=customtkinter.CTkLabel(meaning_frame, text="Meaning:",text_color="black",bg_color=bgColor)
        meaning_label.pack(side="left",padx=5)
        meaning_entry = customtkinter.CTkEntry(meaning_frame,bg_color=bgColor)
        meaning_entry.pack(side="left",padx=5)
        
        button_frame = customtkinter.CTkFrame(manager_window,bg_color=bgColor,fg_color=bgColor)
        button_frame.pack(pady=10)
        add_button = customtkinter.CTkButton(button_frame, text="추가",text_color="white",bg_color=bgColor,fg_color=fgColor, corner_radius=32,command=lambda: add_word(words, word_entry, meaning_entry, word_listbox))
        add_button.pack(side="left")
        update_button = customtkinter.CTkButton(button_frame, text="수정", text_color="white",bg_color=bgColor,fg_color=fgColor,corner_radius=32,command=lambda: update_word(words, word_entry, meaning_entry, word_listbox))
        update_button.pack(side="left",padx=7)
        delete_button = customtkinter.CTkButton(button_frame, text="삭제",text_color="white",bg_color=bgColor,fg_color=fgColor ,corner_radius=32,command=lambda: delete_word(words, word_entry, meaning_entry, word_listbox))
        delete_button.pack()
        # 완료 버튼을 추가합니다
        complete_button = customtkinter.CTkButton(manager_window, text="완료", text_color="white",bg_color=bgColor,fg_color=fgColor,hover_color=hoverColor,corner_radius=32,command=lambda: save_words_to_file(words))
        complete_button.pack()

            # 로그아웃 기능
        def logout():
            confirm = messagebox.askokcancel("로그아웃", "정말 로그아웃 하시겠습니까?")
            if confirm:
                manager_window.destroy()  # 현재 창 닫기
                open_login_window(manager_window)  # 로그인 창 열기

        logout_button = customtkinter.CTkButton(manager_window, text="로그아웃", text_color="white",bg_color=bgColor, fg_color=fgColor, hover_color=hoverColor, corner_radius=32, command=logout)
        logout_button.pack(pady=10)

        manager_window.attributes("-topmost", True)
        manager_window.lift()
        manager_window.after(100, lambda: manager_window.attributes("-topmost", False))
        manager_window.mainloop()

    except Exception as e:
        messagebox.showerror("에러", "일시적인 오류가 발생했습니다. 나중에 다시 시도해주세요.")

