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

    # 개별 항목 유효성 검사
    def is_valid_field(self, field: str, value: str) -> bool:
        patterns = {
            'member_id': r'[a-zA-Z0-9]{4,12}',
            'name': r'.+',
            'password': r'(?=.*[a-zA-Z])(?=.*[0-9])[a-zA-Z0-9]{8,10}',
            'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            'phone': r'010[0-9]{8}',
        }

        # 자료형 및 빈 값 검사
        if not isinstance(value, str) or not value.strip():
            return False

        return re.fullmatch(patterns[field], value) is not None

    # 회원가입 유효성 검사
    def is_valid_member(self, member: Member) -> bool:
        fields = {
            'member_id': member.member_id,
            'name': member.name,
            'password': member.password,
            'email': member.email,
            'phone': member.phone,
        }

        for field, value in fields.items():
            if not self.is_valid_field(field, value):
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

    def do_retrieve(self) -> list:
        if not self.members:
            print('존재하는 회원이 없습니다.')

        return self.members

    def do_select_one(self, member_id: str) -> Member:
        for member in self.members:
            if member_id == member['member_id']:
                return member
        print('존재하는 회원이 없습니다.')
        return None

    # 회원 수정 유효성 검사
    def is_valid_update_member(self, member: Member) -> bool:
        # 아이디 검사
        if not self.is_valid_field('member_id', member.member_id):
            return False

        fields = {
            'name': member.name,
            'password': member.password,
            'email': member.email,
            'phone': member.phone,
        }

        # 수정할 정보가 없는 경우
        if all(value is None for value in fields.values()):
            return False

        # 입력한 항목만 유효성 검사
        for field, value in fields.items():
            if value is not None:
                if not self.is_valid_field(field, value):
                    return False

        return True

    # 회원 정보 수정
    def do_update(self, update_member: Member) -> bool:
        if not self.is_valid_update_member(update_member):
            return False

        for member in self.members:
            if update_member.member_id == member['member_id']:
                if update_member.name is not None:
                    member['name'] = update_member.name

                if update_member.password is not None:
                    member['password'] = update_member.password

                if update_member.email is not None:
                    member['email'] = update_member.email

                if update_member.phone is not None:
                    member['phone'] = update_member.phone

                self.save_members()
                return True

        return False

    def do_delete(self, member_id: str) -> bool:
        for member in self.members:
            if member_id == member['member_id']:
                self.members.remove(member)
                self.save_members()
                print('회원 삭제가 완료되었습니다.')
                return True

        print('회원 정보가 없습니다.')
        return False


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

    print('\n=== 회원 정보 전체 조회 테스트 ===')
    print(manager.do_retrieve())

    print('\n=== 회원 정보 상세 조회 테스트 ===')
    print(f'user01: {manager.do_select_one("user01")}')
    print(f'user99: {manager.do_select_one("user99")}')

    print('\n=== 회원 정보 수정 테스트 ===')
    update_member1 = Member('user01', '홍길동1', 'abc12345', 'test11@gmail.com')
    update_member2 = Member('user99', '홍길동1', 'abc12345', 'test11@gmail.com')

    print(f'user01: {manager.do_update(update_member1)}')
    print(f'user99: {manager.do_update(update_member2)}')

    print('\n=== 회원 정보 삭제 테스트 ===')
    # 존재하는 회원 삭제
    print(manager.do_delete('user01'))
    # 존재하지 않는 회원 삭제
    print(manager.do_delete('user99'))


if __name__ == "__main__":
    main()
