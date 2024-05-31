import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from wordDB import words  # 단어 데이터베이스를 포함하는 모듈
import customtkinter 
from customtkinter import *
from PIL import Image
from abc import ABC, abstractmethod

# 검색 전략 인터페이스
class SearchStrategy(ABC):
    @abstractmethod
    def search(self, query, words):
        pass

# 영어 단어로 검색하는 전략
class EnglishWordSearch(SearchStrategy):
    def search(self, query, words):
        return [word for word in words if query in list(word.keys())[0].lower()]

# 뜻으로 검색하는 전략
class MeaningSearch(SearchStrategy):
    def search(self, query, words):
        return [word for word in words if query in list(word.values())[0].lower()]

class WordWindow:
    def __init__(self):
        self.bgColor = "#FFDFB9"
        self.fgColor = "#A4193D"
        self.hoverColor = "#C850C0"
        self.words_per_page = 200  # 페이지당 단어 수 줄이기
        self.search_strategy = EnglishWordSearch()  # 기본 검색 전략 설정

    def set_search_strategy(self, strategy):
        self.search_strategy = strategy

    def execute_search(self, query):
        if self.search_strategy:
            return self.search_strategy.search(query, words)
        else:
            raise ValueError("검색 전략이 설정되지 않았습니다.")

    def display_words(self, page_num):
        try:
            page_window = customtkinter.CTkToplevel(root)
            page_window.title(f"TOEICVOCAMACA - 단어장 (part {page_num})")
            page_window.geometry("700x500+100+100")
            page_window.resizable(False, False)
            page_window.config(background=self.bgColor)

            page_window.attributes("-topmost", True)
            page_window.update()  # Update the window to apply the topmost attribute
            page_window.attributes("-topmost", False)

            frame = tk.Frame(page_window, background=self.bgColor)
            frame.pack(pady=(20,0), fill="both", expand=True)

            start_index = (page_num - 1) * self.words_per_page
            end_index = min(start_index + self.words_per_page, len(words))

            columns = ('word', 'meaning')
            
            tree = ttk.Treeview(frame, columns=columns, show='headings', selectmode='none')

            tree.heading('word', text='단어')
            tree.heading('meaning', text='뜻')

            tree.column('word', width=150, anchor='w')
            tree.column('meaning', width=250, anchor='w')
            style = ttk.Style()
            style.configure('Treeview', rowheight=30)  # rowheight 값을 조정하여 뜻 컬럼의 행 높이를 설정합니다.
            
            for i, word in enumerate(words[start_index:end_index], start=start_index):
                for english_word, meaning in word.items():
                    tree.insert('', 'end', values=(english_word, meaning))

            tree.pack(side="left", fill="both", expand=True)

            scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side="right", fill="y")
            
            close_button = customtkinter.CTkButton(page_window, text="닫기", width=20, height=10, bg_color=self.bgColor, fg_color=self.fgColor, hover_color=self.hoverColor, command=page_window.destroy)
            close_button.pack(side="bottom", pady=10)

            page_window.attributes("-topmost", True)
            page_window.lift()
            page_window.after(100, lambda: page_window.attributes("-topmost", False))

            page_window.mainloop()

        except Exception as e:
            messagebox.showerror("에러", "일시적인 오류가 발생했습니다. 나중에 다시 시도해주세요.")

    def search_word(self):
        try:
            query = search_entry.get().strip().lower()
            if not query:
                return
            
            results = self.execute_search(query)  # 전략에 따라 검색 수행

            result_window = customtkinter.CTkToplevel(root)
            result_window.title("검색 결과")
            result_window.geometry("400x500+100+100")
            result_window.resizable(False, False)
            result_window.config(background=self.bgColor)

            result_window.attributes("-topmost", True)
            result_window.update()  # Update the window to apply the topmost attribute
            result_window.attributes("-topmost", False)

            frame = tk.Frame(result_window, background=self.bgColor)
            frame.pack(pady=(20, 0), fill="both", expand=True)

            columns = ('word', 'meaning')
            tree = ttk.Treeview(frame, columns=columns, show='headings', selectmode='none')

            tree.heading('word', text='단어')
            tree.heading('meaning', text='뜻')

            tree.column('word', width=150, anchor='w')
            tree.column('meaning', width=250, anchor='w')

            if results:
                for word in results:
                    for english_word, meaning in word.items():
                        tree.insert('', 'end', values=(english_word, meaning))
            else:
                tree.insert('', 'end', values=("검색 결과가 없습니다.", ""))

            tree.pack(side="left", fill="both", expand=True)

            scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side="right", fill="y")
            
            close_button = customtkinter.CTkButton(result_window, text="닫기", width=20, height=10, bg_color=self.bgColor, fg_color=self.fgColor, hover_color=self.hoverColor, command=result_window.destroy)
            close_button.pack(side="bottom", pady=10)

            result_window.attributes("-topmost", True)
            result_window.lift()
            result_window.after(100, lambda: result_window.attributes("-topmost", False))

            result_window.mainloop()
            
        except Exception as e:
            messagebox.showerror("에러", "일시적인 오류가 발생했습니다. 나중에 다시 시도해주세요.")

    def open_wordlist_window(self):
        try:
            global root, search_entry
            root = customtkinter.CTkToplevel()
            root.title("TOEICVOCAMACA - 단어장")
            root.geometry("400x500+100+100")
            root.resizable(False, False)
            root.config(background=self.bgColor)

            if words:
                # 검색창을 페이지 버튼 위에 배치
                search_frame = tk.Frame(root, background=self.bgColor)
                search_frame.pack(pady=(20, 0))

                search_label = tk.Label(search_frame, text="검색:", background=self.bgColor)
                search_label.pack(side="left", padx=5)

                search_entry = customtkinter.CTkEntry(search_frame, width=200)
                search_entry.pack(side="left", padx=5)

                search_button = customtkinter.CTkButton(search_frame, text="검색", bg_color=self.bgColor, fg_color=self.fgColor, hover_color=self.hoverColor, command=self.search_word)
                search_button.pack(side="left", padx=5)

                # 페이지 버튼을 위한 프레임 생성
                button_frame = tk.Frame(root, background=self.bgColor)
                button_frame.pack(pady=(10, 20))

                # 페이지 버튼 추가
                num_pages = (len(words) + self.words_per_page - 1) // self.words_per_page

                for page_num in range(1, num_pages + 1):
                    page_button = customtkinter.CTkButton(button_frame, text=f"Part {page_num}", bg_color=self.bgColor, fg_color=self.fgColor, hover_color=self.hoverColor, command=lambda num=page_num: self.display_words(num))
                    page_button.pack(side="top", pady=5)

                # 닫기 버튼을 아래에 배치
                close_button = customtkinter.CTkButton(root, text="닫기", width=20, height=10, command=root.destroy, bg_color=self.bgColor, fg_color=self.fgColor, hover_color=self.hoverColor)
                close_button.pack(side="bottom", pady=10)

            else:
                no_data_label = tk.Label(root, text="단어가 없습니다", anchor='w', justify='left')
                no_data_label.pack(pady=20)
                
            root.attributes("-topmost", True)
            root.after(100, lambda: root.attributes("-topmost", False))
            root.mainloop()

        except Exception as e:
            messagebox.showerror("에러", "일시적인 오류가 발생했습니다. 나중에 다시 시도해주세요.")

# # 사용 예시
# word_window = WordWindow()
# word_window.set_search_strategy(EnglishWordSearch())  # 기본 검색 전략 설정
# word_window.open_wordlist_window()
