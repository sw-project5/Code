import tkinter as tk
from tkinter import ttk
import json

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

def tier_board():
    root = tk.Tk()
    root.geometry("400x500")
    root.title("TOEIC Vocabulary Tier Leaderboard")

    # 트리뷰(트리 형태의 데이터 구조) 생성
    tree = ttk.Treeview(root, columns=('Username', 'Tier', 'Score'), show='headings')

    # 스크롤바 생성
    vsb = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    vsb.pack(side='right', fill='y')

    # 트리뷰에 스크롤바 연결
    tree.configure(yscrollcommand=vsb.set)

    # 각 컬럼 설정
    tree.heading('Username', text='Username')
    tree.heading('Tier', text='Tier')
    tree.heading('Score', text='Score')

    # 컬럼 너비 설정
    tree.column('Username', width=150)
    tree.column('Tier', width=100)
    tree.column('Score', width=100)

    # 사용자 데이터 로드 및 정렬
    user_data = load_user_data()
    sorted_members = [user for user in user_data if user.get('level') not in ['admin', None]]
    sorted_members = sorted(sorted_members, key=lambda x: (tier_ranking.get(x['level'], tier_ranking['N/A']), -x.get('score', 0), user_data.index(x)))

    # 정렬된 회원 정보를 트리뷰에 삽입
    for user in sorted_members:
        tree.insert('', 'end', values=(user['username'], user['level'], user.get('score', 0)))

    tree.pack()

    # tkinter 메인루프 실행
    root.mainloop()

