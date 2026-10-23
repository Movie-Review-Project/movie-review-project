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
        # 자료형 및 빈 값 검사
        values = [
            member.member_id,
            member.name,
            member.password,
            member.email,
            member.phone,
        ]

        if not all(isinstance(value, str) and value.strip() for value in values):
            return False

        # 정규표현식
        id_pattern = r'[a-zA-Z0-9]{4,12}'

        password_pattern = r'(?=.*[a-zA-Z])(?=.*[0-9])[a-zA-Z0-9]{8,10}'
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        phone_pattern = r'010[0-9]{8}'

        if not re.fullmatch(id_pattern, member.member_id):
            return False

        if not re.fullmatch(password_pattern, member.password):
            return False

        if not re.fullmatch(email_pattern, member.email):
            return False

        if not re.fullmatch(phone_pattern, member.phone):
            return False

        return True


def main():

    manager = MemberManager()

    # 파일 불러오기 테스트
    print('=== 파일 불러오기 테스트 ===')
    if manager.members:
        print(manager.members[0])

    # 회원 정보 존재 여부 확인 테스트
    print('\n=== 회원 존재 여부 테스트 ===')
    print(manager.is_exist('user01'))
    print(manager.is_exist('admin'))

    # 회원 정보 유효성 검사 테스트
    print('\n=== 회원 정보 유효성 검사 테스트 ===')

    test_cases = [
        (
            '정상 회원',
            Member('user01', '홍길동', 'abc12345', 'test@gmail.com', '01012345678'),
            True,
        ),
        (
            '아이디 길이 부족',
            Member('abc', '홍길동', 'abc12345', 'test@gmail.com', '01012345678'),
            False,
        ),
        (
            '아이디 특수문자 포함',
            Member('user!', '홍길동', 'abc12345', 'test@gmail.com', '01012345678'),
            False,
        ),
        (
            '이름 누락',
            Member('user01', '', 'abc12345', 'test@gmail.com', '01012345678'),
            False,
        ),
        (
            '비밀번호 숫자 없음',
            Member('user01', '홍길동', 'abcdefgh', 'test@gmail.com', '01012345678'),
            False,
        ),
        (
            '비밀번호 영문 없음',
            Member('user01', '홍길동', '12345678', 'test@gmail.com', '01012345678'),
            False,
        ),
        (
            '비밀번호 길이 부족',
            Member('user01', '홍길동', 'abc1234', 'test@gmail.com', '01012345678'),
            False,
        ),
        (
            '이메일 형식 오류',
            Member('user01', '홍길동', 'abc12345', 'testgmail.com', '01012345678'),
            False,
        ),
        (
            '전화번호 형식 오류',
            Member('user01', '홍길동', 'abc12345', 'test@gmail.com', '0101234567'),
            False,
        ),
        (
            '전화번호 자료형 오류',
            Member('user01', '홍길동', 'abc12345', 'test@gmail.com', 1012345678),
            False,
        ),
    ]

    for name, member, expected in test_cases:
        result = manager.is_valid_member(member)
        status = 'PASS' if result == expected else 'FAIL'
        print(f'[{status}] {name}: {result}')


if __name__ == "__main__":
    main()
