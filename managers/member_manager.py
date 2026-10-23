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
                return False
        return True

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
            print('아이디 형식은 4~12 글자 영어나 숫자입니다.')
            return False

        if not re.fullmatch(password_pattern, member.password):
            print('비밀번호 형식은 8~10자리 영어나 숫자입니다.')
            return False

        if not re.fullmatch(email_pattern, member.email):
            print('이메일 형식이 올바르지 않습니다.')
            return False

        if not re.fullmatch(phone_pattern, member.phone):
            print('전화번호 11자리를 입력해주세요. (ex:01012341234)')
            return False

        return True

    # 회원 정보 추가
    def add_member(self, member: Member) -> bool:
        if not self.is_valid_member(member):
            print('회원 정보를 정확하게 입력해주세요.')
            return False

        if not self.is_exist(member.member_id):
            print('이미 존재하는 회원 ID입니다.')
            return False

        self.members.append(vars(member).copy())
        self.save_members()

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

    # 회원 정보 추가 테스트
    print('\n=== 회원 정보 추가 테스트 ===')
    member1 = Member('user01', '홍길동', 'abc12345', 'test1@gmail.com', '01012345678')
    member2 = Member('user01', '홍길순', 'abc12345', 'test2@gmail.com', '01012345678')
    member3 = Member('user02', '박민철', 'abc12345', 'test3@gmail.com', '01012345678')

    print(manager.add_member(member1))
    print(manager.add_member(member2))
    print(manager.add_member(member3))


if __name__ == "__main__":
    main()
