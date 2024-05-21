import json

class UserManager:
    def __init__(self, user_file):
        self.user_file = user_file
        self.users = self.load_users()

    def load_users(self):
        try:
            with open(self.user_file, 'r') as file:
                users = json.load(file)
        except FileNotFoundError:
            users = {}
        return users

    def save_users(self):
        with open(self.user_file, 'w') as file:
            json.dump(self.users, file, indent=4)

    def add_user(self, username, password, birthdate, firstlogin):
        if username in self.users:
            return False  # 이미 존재하는 사용자명인 경우 실패

        # 생년월일을 YYMMDD 형식으로 저장
        self.users[username] = {
            'password': password,
            'birthdate': birthdate,
            'firstlogin': firstlogin
        }
        self.save_users()
        return True  # 회원가입 성공

    def check_user(self, username, password):
        if username in self.users and self.users[username]['password'] == password:
            return True  # 사용자명과 비밀번호 일치
        return False  # 사용자명 또는 비밀번호가 일치하지 않음
