import tkinter as tk
from tkinter import ttk
from wordDB import words
import customtkinter 
from customtkinter import *
from PIL import Image

# 기본 색상
bgColor="#FFDFB9"
fgColor="#A4193D"
hoverColor="#C850C0"

def display_words(page_num):
    page_window = customtkinter.CTkToplevel(root)
    page_window.title(f"TOEICVOCAMACA - 단어장 (part {page_num})")
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

def search_word():
    query = search_entry.get().strip().lower()
    if not query:
        return
    
    result_window = customtkinter.CTkToplevel(root)
    result_window.title("검색 결과")
    result_window.geometry("400x500+100+100")
    result_window.resizable(False, False)
    result_window.config(background=bgColor)

    frame = tk.Frame(result_window)
    frame.pack(pady=20)
    frame.config(background=bgColor)

    canvas = tk.Canvas(frame)
    canvas.config(background=bgColor)
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)

    result_frame = tk.Frame(canvas)
    result_frame.config(background=bgColor)
    result_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=result_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set,background=bgColor)
    canvas.config(background=bgColor)

    results = [word for word in words if query in list(word.keys())[0].lower() or query in list(word.values())[0].lower()]
    
    if results:
        for word in results:
            for english_word, meaning in word.items():
                word_label = tk.Label(result_frame, text=f"{english_word}: {meaning}", anchor='w', justify='left', wraplength=360,background=bgColor)
                word_label.pack(anchor="w", padx=10, pady=5)
    else:
        no_result_label = tk.Label(result_frame, text="검색 결과가 없습니다.", anchor='w', justify='left', wraplength=360,background=bgColor)
        no_result_label.pack(anchor="w", padx=10, pady=5)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    close_button = customtkinter.CTkButton(result_window, text="닫기", width=20,height=10,bg_color=bgColor,fg_color=fgColor,hover_color=hoverColor,command=result_window.destroy)
    close_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

def open_wordlist_window():
    global root, search_entry
    root = customtkinter.CTkToplevel()
    root.title("TOEICVOCAMACA - 단어장")
    root.geometry("400x500+100+100")
    root.resizable(False, False)
    root.config(background=bgColor)

    if words:
        # 검색창을 페이지 버튼 위에 배치
        search_frame = tk.Frame(root, background=bgColor)
        search_frame.pack(pady=(20, 0))

        search_label = tk.Label(search_frame, text="검색:", background=bgColor)
        search_label.pack(side="left", padx=5)

        search_entry = customtkinter.CTkEntry(search_frame, width=200)
        search_entry.pack(side="left", padx=5)

        search_button = customtkinter.CTkButton(search_frame, text="검색", bg_color=bgColor, fg_color=fgColor, hover_color=hoverColor, command=search_word)
        search_button.pack(side="left", padx=5)

        # 페이지 버튼을 위한 프레임 생성
        button_frame = tk.Frame(root)
        button_frame.pack(pady=(10, 20))
        button_frame.config(background=bgColor)

        # 페이지 버튼 추가
        num_pages = (len(words) + words_per_page - 1) // words_per_page

        for page_num in range(1, num_pages + 1):
            page_button = customtkinter.CTkButton(button_frame, text=f"Part {page_num}",bg_color=bgColor,fg_color=fgColor,hover_color=hoverColor, command=lambda num=page_num: display_words(num))
            page_button.grid(row=page_num-1, pady=5)

        # 빈 행을 추가하여 페이지 버튼들을 가운데로 정렬
        empty_label = tk.Label(button_frame, text="", bg=bgColor)
        empty_label.grid(row=num_pages, pady=10)

    else:
        no_data_label = tk.Label(root, text="단어가 없습니다", anchor='w', justify='left')
        no_data_label.pack(pady=20)

    root.mainloop()

# Test the function
open_wordlist_window()
