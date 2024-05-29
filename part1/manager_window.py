import tkinter as tk
from tkinter import messagebox
import wordDB  # wordDB.py 파일을 가져옵니다.
import json
import os

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

def open_manager_window():
    try:
        manager_window = tk.Tk()
        manager_window.title("Word Manager")
        manager_window.geometry("450x500+100+100")
        manager_window.resizable(False, False)

        # 초기 단어 데이터
        words = wordDB.words

        # 단어 목록 표시
        word_listbox = tk.Listbox(manager_window, height=10, width=50)
        word_listbox.grid(row=0, column=0, columnspan=3)

        # 초기 단어 목록 업데이트
        update_word_listbox(words, word_listbox)

        # 단어 추가/수정/삭제를 위한 엔트리와 버튼
        tk.Label(manager_window, text="Word:").grid(row=1, column=0)
        word_entry = tk.Entry(manager_window)
        word_entry.grid(row=1, column=1, columnspan=2)

        tk.Label(manager_window, text="Meaning:").grid(row=2, column=0)
        meaning_entry = tk.Entry(manager_window)
        meaning_entry.grid(row=2, column=1, columnspan=2)

        button_frame = tk.Frame(manager_window)
        button_frame.grid(row=3, column=0, columnspan=3)

        add_button = tk.Button(button_frame, text="Add", command=lambda: add_word(words, word_entry, meaning_entry, word_listbox))
        add_button.grid(row=0, column=0)

        update_button = tk.Button(button_frame, text="Update", command=lambda: update_word(words, word_entry, meaning_entry, word_listbox))
        update_button.grid(row=0, column=1)

        delete_button = tk.Button(button_frame, text="Delete", command=lambda: delete_word(words, word_entry, meaning_entry, word_listbox))
        delete_button.grid(row=0, column=2)

        # 완료 버튼을 추가합니다
        complete_button = tk.Button(manager_window, text="Complete", command=lambda: save_words_to_file(words))
        complete_button.grid(row=4, column=0, columnspan=3)

        manager_window.mainloop()

    except Exception as e:
        messagebox.showerror("에러", "일시적인 오류가 발생했습니다. 나중에 다시 시도해주세요.")

if __name__ == "__main__":
    open_manager_window()