# member_manager.py
import json
import re
from pathlib import Path

from models.member import Member


class MemberManager:
    def __init__(self) -> None:
        self.file_path = (
            Path(__file__).resolve().parent.parent / "data" / "members.json"
        )
        self.members = self.load_members()

    # members.json 파일에서 회원 정보 불러오기
    def load_members(self) -> list[dict[str, str]]:
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    # members.json 파일에 회원 정보 저장
    def save_members(self) -> None:
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(self.members, file, ensure_ascii=False, indent=4)

    # 회원 정보 존재 여부 확인
    def is_exist(self, member_id: str) -> bool:
        for member in self.members:
            if member_id == member['member_id']:
                return True
        return False

    # 회원 정보 유효성 검사
    def is_valid_member(self, member: Member) -> bool:

        # 자료형 검사: 모든 값이 str인지 확인
        if not all(
            isinstance(value, str)
            for value in [
                member.member_id,
                member.password,
                member.email,
                member.phone_number,
            ]
        ):
            return False

        # 유효성 검사
        # 아이디: 영문 또는 숫자, 4~12자리
        id_pattern = r"[a-zA-Z0-9]{4,12}"

        # 비밀번호: 영문 + 숫자 필수, 8~10자리
        password_pattern = r"(?=.*[a-zA-Z])(?=.*[0-9])[a-zA-Z0-9]{8,10}"

        # 이메일: 이메일 형식
        email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

        # 전화번호: 010으로 시작하는 11자리
        phone_pattern = r"010[0-9]{8}"

        if not re.fullmatch(id_pattern, member.member_id):
            return False

        if not re.fullmatch(password_pattern, member.password):
            return False

        if not re.fullmatch(email_pattern, member.email):
            return False

        if not re.fullmatch(phone_pattern, member.phone_number):
            return False

        return True


def main():
    # 파일 불러오기(load_members) 테스트
    manager = MemberManager()
    print(manager.members[0])

    # 회원 정보 존재 여부 확인 테스트
    print(manager.is_exist('user01'))
    print(manager.is_exist('admin'))


if __name__ == "__main__":
    main()
