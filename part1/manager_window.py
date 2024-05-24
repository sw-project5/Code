import tkinter as tk
from tkinter import messagebox
import wordDB  # wordDB.py 파일을 가져옵니다.
import json
import os

def update_word_listbox(words, word_listbox):
    word_listbox.delete(0, tk.END)
    for word in words:
        for eng, kor in word.items():
            word_listbox.insert(tk.END, f"{eng}: {kor}")

def add_word(words, word_entry, meaning_entry, word_listbox):
    eng = word_entry.get().strip()
    kor = meaning_entry.get().strip()
    if eng and kor:
        words.append({eng: kor})
        update_word_listbox(words, word_listbox)
        word_entry.delete(0, tk.END)
        meaning_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Both fields must be filled")

def update_word(words, word_entry, meaning_entry, word_listbox):
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
            messagebox.showwarning("Input Error", "Both fields must be filled")
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
            messagebox.showwarning("Word Not Found", "The word is not in the list")

def delete_word(words, word_entry, word_listbox):
    selected = word_listbox.curselection()
    if selected:
        index = selected[0]
        del words[index]
        update_word_listbox(words, word_listbox)
    else:
        eng = word_entry.get().strip()
        found = False
        for i, word in enumerate(words):
            if eng in word:
                del words[i]
                found = True
                break
        if found:
            update_word_listbox(words, word_listbox)
            word_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Word Not Found", "The word is not in the list")

def save_words_to_file(words, file_path='wordDB.py'):
    words_data = {"words": words}
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write("words = ")
        json.dump(words_data["words"], file, ensure_ascii=False, indent=4)

def main():
    root = tk.Tk()
    root.title("Word Manager")
    root.geometry("450x500+100+100")
    root.resizable(False, False)

    # 초기 단어 데이터
    words = wordDB.words

    # 단어 목록 표시
    word_listbox = tk.Listbox(root, height=10, width=50)
    word_listbox.grid(row=0, column=0, columnspan=3)

    # 초기 단어 목록 업데이트
    update_word_listbox(words, word_listbox)

    # 단어 추가/수정/삭제를 위한 엔트리와 버튼
    tk.Label(root, text="Word:").grid(row=1, column=0)
    word_entry = tk.Entry(root)
    word_entry.grid(row=1, column=1, columnspan=2)

    tk.Label(root, text="Meaning:").grid(row=2, column=0)
    meaning_entry = tk.Entry(root)
    meaning_entry.grid(row=2, column=1, columnspan=2)

    button_frame = tk.Frame(root)
    button_frame.grid(row=3, column=0, columnspan=3)

    add_button = tk.Button(button_frame, text="Add", command=lambda: add_word(words, word_entry, meaning_entry, word_listbox))
    add_button.grid(row=0, column=0)

    update_button = tk.Button(button_frame, text="Update", command=lambda: update_word(words, word_entry, meaning_entry, word_listbox))
    update_button.grid(row=0, column=1)

    delete_button = tk.Button(button_frame, text="Delete", command=lambda: delete_word(words, word_entry, word_listbox))
    delete_button.grid(row=0, column=2)

    # 완료 버튼을 추가합니다
    complete_button = tk.Button(root, text="Complete", command=lambda: save_words_to_file(words))
    complete_button.grid(row=4, column=0, columnspan=3)

    root.mainloop()

if __name__ == "__main__":
    main()

