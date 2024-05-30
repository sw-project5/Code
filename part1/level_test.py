import random
import json
import tkinter
from wordDB import words  # 단어 데이터베이스 임포트
from level import get_level_from_score
import customtkinter
from customtkinter import *
from tkinter import messagebox
from PIL import Image

class LevelTestWindow:
    def __init__(self):
        self.new_key_name = "english_word"
        self.new_value_name = "korean_meaning"
        self.new_questions = [{self.new_key_name: key, self.new_value_name: value} for item in words for key, value in item.items()]

        self.bgColor = "#FFDFB9"
        self.fgColor = "#A4193D"
        self.hoverColor = "#C850C0"

        self.answer = 0
        self.total_questions = 20
        self.correct_count = 0
        self.wrong_count = 0
        self.level = ""
        self.score = 0
        self.current_question = 0

        self.window = None
        self.question_label = None
        self.progress_label = None
        self.progress_canvas = None
        self.buttons = []
        self.entry = None
        self.check_btn = None
        self.current_user = None

    def load_user_data(self, filepath='users.json'):
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def save_user_data(self, users, filepath='users.json'):
        if not isinstance(users, list):
            raise ValueError("The data to be saved must be a list.")
        
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(users, file, ensure_ascii=False, indent=4)

    def update_user_data(self, users, current_user, level, score):
        for user in users:
            if user["username"] == current_user["username"]:
                user["level"] = level
                user["score"] = score
                break

    def open_wordleveltest_window(self, user):
        self.current_user = user
        self.window = customtkinter.CTkToplevel()
        self.window.title("영어 퀴즈")
        self.window.geometry("600x500+100+100")
        self.window.resizable(False, False)
        self.window.config(background=self.bgColor)

        level_text = customtkinter.CTkLabel(self.window, text="사용자의 수준을 알아보기 위해 레벨 테스트를 진행하겠습니다.", text_color="black", bg_color=self.bgColor, font=("맑은 고딕", 13))
        level_text.pack(pady=30)

        self.question_label = customtkinter.CTkLabel(self.window, width=30, height=4, text="test", text_color="black", font=("맑은 고딕", 20, "bold"), bg_color=self.bgColor)
        self.question_label.pack(pady=10)

        self.progress_label = customtkinter.CTkLabel(self.window, text=f"{self.current_question}/{self.total_questions}", font=("맑은 고딕", 12), text_color="black", bg_color=self.bgColor)
        self.progress_label.pack()

        self.progress_canvas = customtkinter.CTkCanvas(self.window, width=300, height=20, highlightthickness=0, highlightbackground=self.fgColor)
        self.progress_canvas.pack(pady=30)

        self.next_question()

        self.window.attributes("-topmost", True)
        self.window.after(100, lambda: self.window.attributes("-topmost", False))
        self.window.mainloop()

    def wrap_text(self, text, line_length):
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            if len(current_line) + len(word) + 1 <= line_length:
                current_line += (word + " ")
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())
        return "\n".join(lines)

    def next_question(self):
        if self.current_question == self.total_questions:
            for widget in self.window.winfo_children():
                widget.destroy()
            
            if self.correct_count >= 15:
                result_text = "통과하였습니다."
                self.score = self.current_user.get("score", 0)
                self.score += 1
            else:
                result_text = "통과하지 못했습니다."
                self.score = self.current_user.get('score', 0)

            self.level, print_score, self.score = get_level_from_score(self.score)
            self.current_user["level"] = self.level
            self.current_user["score"] = self.score

            level_text = f"맞은 문제의 수: {self.correct_count} 입니다.\n레벨은 {self.level}입니다.\n점수는 {print_score}점입니다."
            level_label = customtkinter.CTkLabel(self.window, text=level_text, text_color="black", bg_color=self.bgColor, font=("맑은 고딕", 20))
            level_label.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

            result_label = customtkinter.CTkLabel(self.window, text=result_text, text_color=self.fgColor, bg_color=self.bgColor, font=("맑은 고딕", 20, "bold"))
            result_label.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

            close_button = customtkinter.CTkButton(self.window, text="닫기", width=30, height=20, command=self.window.destroy, bg_color=self.bgColor, fg_color=self.fgColor, hover_color=self.hoverColor)
            close_button.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

            users = self.load_user_data()
            self.update_user_data(users, self.current_user, self.level, self.score)
            self.save_user_data(users)
            
            self.restart_test()
            return

        if self.current_question % 2 != 0:
            self.multi_choice_question()
        else:
            self.short_answer_question()

        self.current_question += 1
        self.progress_label.configure(text=f"{self.current_question}/{self.total_questions}")
        self.update_progress()

    def multi_choice_question(self):
        if self.buttons:
            for btn in self.buttons:
                btn.destroy()

        self.buttons = []
        for i in range(4):
            btn = customtkinter.CTkButton(self.window, width=200, height=50, text=f"{i+1}번", command=lambda idx=i: self.check_answer(idx), bg_color=self.bgColor, fg_color=self.fgColor, hover_color=self.hoverColor, corner_radius=32, text_color="white")
            btn.pack(pady=5)
            self.buttons.append(btn)

        multi_choice = random.sample(self.new_questions, 4)
        self.answer = random.randint(0, 3)
        cur_question = multi_choice[self.answer][self.new_key_name]
        self.question_label.configure(text=cur_question)

        for i in range(4):
            wrapped_text = self.wrap_text(multi_choice[i][self.new_value_name], 20)
            self.buttons[i].configure(text=wrapped_text, command=lambda idx=i: self.check_answer(idx))

    def short_answer_question(self):
        random_question = random.choice(self.new_questions)
        cur_question = random_question[self.new_value_name]
        self.answer = random_question[self.new_key_name]
        self.question_label.configure(text=cur_question)

        self.entry = customtkinter.CTkEntry(self.window, width=200, fg_color=self.bgColor, border_color=self.fgColor, text_color="black", corner_radius=0)
        self.entry.pack(pady=7)

        self.check_btn = customtkinter.CTkButton(self.window, text="확인", width=150, height=50, bg_color=self.bgColor, fg_color=self.fgColor, hover_color=self.hoverColor, corner_radius=32, text_color="white", font=("맑은 고딕", 16, "bold"), command=self.check_short_answer)
        self.check_btn.pack()

    def check_short_answer(self):
        user_answer = self.entry.get().strip().lower()
        if user_answer == self.answer.lower():
            self.correct_count += 1
        else:
            self.wrong_count += 1
        self.entry.destroy()
        self.check_btn.destroy()
        self.window.after(1, self.next_question)

    def check_answer(self, idx):
        if idx == self.answer:
            self.correct_count += 1
        else:
            self.wrong_count += 1
        if self.buttons:    
            for btn in self.buttons:
                btn.destroy()
            self.window.after(1, self.next_question)

    def update_progress(self):
        self.progress_canvas.delete("all")
        self.progress_canvas.create_rectangle(0, 0, 300, 20, outline=self.fgColor, width=2)
        self.progress_canvas.create_rectangle(1, 1, 299, 19, fill=self.bgColor, outline="")
        self.progress_canvas.create_rectangle(1, 1, self.current_question / self.total_questions * 299, 19, fill=self.fgColor, outline="")

    def restart_test(self):
        self.correct_count = 0
        self.wrong_count = 0
        self.current_question = 0