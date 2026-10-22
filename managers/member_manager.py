# member_manager.py
import json
from pathlib import Path


class MemberManager:
    def __init__(self):
        self.file_path = (
            Path(__file__).resolve().parent.parent / "data" / "members.json"
        )
        self.members = self.load_members()

    # members.json 파일에서 회원 정보 불러오기
    def load_members(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    # members.json 파일에 회원 정보 저장
    def save_members(self):
        with open(self.file_path, 'w', encoding='utf-8') as file:
            return json.dump(self.members, file, ensure_ascii=False, indent=4)

    # 회원 정보 존재 여부 확인
    def is_exist(self, user_id):
        for member in self.members:
            if user_id == member['member_id']:
                return True
        return False


def main():
    # 파일 불러오기(load_members) 테스트
    manager = MemberManager()
    print(manager.members[0])

    # 회원 정보 존재 여부 확인 테스트
    print(manager.is_exist('user01'))
    print(manager.is_exist('admin'))


if __name__ == "__main__":
    main()
