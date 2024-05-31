import tkinter as tk
from tkinter import ttk
import json
from PIL import Image
from customtkinter import CTkLabel, CTkImage
import customtkinter

# 기본 색상
bgColor="#FFDFB9"
fgColor="#A4193D"
hoverColor="#C850C0"

# 사용자 데이터 로드 함수
def load_user_data(filepath='users.json'):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

# 티어 순위를 정의합니다.
tier_ranking = {
    'Platinum': 1,
    'Gold': 2,
    'Silver': 3,
    'Bronze': 4,
    'Iron': 5,
    'N/A': 6  # 기본 값으로 사용자의 티어가 없는 경우
}

class TierLeaderboard:
    def __init__(self, master):
        self.master = master
        self.master.geometry("400x500")
        self.master.title("TOEIC Vocabulary Tier Leaderboard")
        self.master.config(background=bgColor)
        self.create_widgets()

    def create_widgets(self):
        ranktableImg = CTkImage(light_image=Image.open("rank_table2.png"),
                                dark_image=Image.open("rank_table2.png"),
                                size=(230, 230))
        # 이미지를 표시할 레이블 생성
        self.image_label = CTkLabel(self.master, text="", image=ranktableImg, bg_color=bgColor)
        self.image_label.pack(pady=10)

        # 스타일 생성 및 설정
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Custom.Treeview",
                        background=bgColor,
                        foreground='black',
                        fieldbackground=bgColor,
                        font=('맑은 고딕', 12))  # 글자 크기를 12로 설정
        style.map("Custom.Treeview", background=[("selected", fgColor)])

        style.configure("Custom.Treeview.Heading",
                        background=fgColor,
                        foreground=bgColor,
                        font=('맑은 고딕', 14, 'bold'))  # 헤더 글자 크기를 14로 설정

        # 트리뷰(트리 형태의 데이터 구조) 생성
        self.tree = ttk.Treeview(self.master, style="Custom.Treeview", columns=('Username', 'Tier', 'Score'), show='headings', height=10)

        # 스크롤바 생성
        self.vsb = ttk.Scrollbar(self.master, orient="vertical", command=self.tree.yview, style="Vertical.TScrollbar")
        self.tree.configure(yscrollcommand=self.vsb.set)

        # 스크롤바 스타일 설정
        style.configure("Vertical.TScrollbar",
                        troughcolor=bgColor,
                        background=fgColor,
                        arrowcolor=bgColor,
                        bordercolor=bgColor,
                        lightcolor=fgColor,
                        darkcolor=fgColor)

        # 각 컬럼 설정
        self.tree.heading('Username', text='Username')
        self.tree.heading('Tier', text='Tier')
        self.tree.heading('Score', text='Score')

        # 컬럼 너비 설정
        self.tree.column('Username', width=130, anchor='center')
        self.tree.column('Tier', width=130, anchor='center')
        self.tree.column('Score', width=130, anchor='center')

        # 사용자 데이터 로드 및 정렬
        user_data = load_user_data()
        sorted_members = [user for user in user_data if user.get('level') not in ['admin', None]]
        sorted_members = sorted(sorted_members, key=lambda x: (tier_ranking.get(x['level'], tier_ranking['N/A']), -x.get('score', 0), user_data.index(x)))

        # 정렬된 회원 정보를 트리뷰에 삽입
        for user in sorted_members:
            self.tree.insert('', 'end', values=(user['username'], user['level'], user.get('score', 0)))

        # 배치 설정
        self.tree.pack(side='left', fill='both', expand=True)
        self.vsb.pack(side='right', fill='y')

        # tkinter 메인루프 실행
        self.master.attributes("-topmost", True)
        self.master.after(100, lambda: self.master.attributes("-topmost", False))
        self.master.mainloop()

# Tkinter 창 실행
if __name__ == "__main__":
    root = customtkinter.CTk()
    app = TierLeaderboard(root)
