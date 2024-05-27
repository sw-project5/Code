import tkinter as tk
from tkinter import ttk
from wordDB import words
import customtkinter 
from customtkinter import *
from PIL import Image

#기본 색상
bgColor="#FFDFB9"
fgColor="#A4193D"
hoverColor="#C850C0"

def display_words(page_num):
    page_window = customtkinter.CTkToplevel(root)
    page_window.title(f"TOEICVOCAMACA - 단어장 (페이지 {page_num})")
    page_window.geometry("400x500+100+100")
    page_window.resizable(False, False)
    page_window.config(background=bgColor)

    frame = tk.Frame(page_window)
    frame.pack(pady=20)
    frame.config(background=bgColor)

    start_index = (page_num - 1) * words_per_page
    end_index = min(start_index + words_per_page, len(words))

    canvas = tk.Canvas(frame)
    canvas.config(background=bgColor)
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    
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
    canvas.config(background=bgColor)

    for i, word in enumerate(words[start_index:end_index], start=start_index):
        for english_word, meaning in word.items():
            word_label = tk.Label(word_frame, text=f"{english_word}: {meaning}", anchor='w', justify='left', wraplength=360,background=bgColor)
            word_label.pack(anchor="w", padx=10, pady=5)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    close_button = customtkinter.CTkButton(page_window, text="닫기", width=20,height=10,bg_color=bgColor,fg_color=fgColor,hover_color=hoverColor,command=page_window.destroy)
    close_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

# 전역 변수
words_per_page = 200

def open_wordlist_window():
    global root
    root = customtkinter.CTkToplevel()
    root.title("TOEICVOCAMACA - 단어장")
    root.geometry("400x500+100+100")
    root.resizable(False, False)
    root.config(background=bgColor)

    if words:
        # 페이지 버튼을 위한 프레임 생성
        button_frame = tk.Frame(root)
        button_frame.pack(expand=True, pady=20)
        button_frame.config(background=bgColor)

        # 페이지 버튼 추가
        num_pages = (len(words) + words_per_page - 1) // words_per_page

        for page_num in range(1, num_pages + 1):
            page_button = customtkinter.CTkButton(button_frame, text=f"Part {page_num}",bg_color=bgColor,fg_color=fgColor,hover_color=hoverColor, command=lambda num=page_num: display_words(num))
            page_button.pack(side="top", pady=5)

        # 닫기 버튼을 아래에 배치
        close_button = customtkinter.CTkButton(root, text="닫기", width=20,height=10,command=root.destroy,bg_color=bgColor,fg_color=fgColor,hover_color=hoverColor)
        close_button.pack(side="bottom", pady=10)

        

    else:
        no_data_label = tk.Label(root, text="단어가 없습니다", anchor='w', justify='left')
        no_data_label.pack(pady=20)

    root.mainloop()