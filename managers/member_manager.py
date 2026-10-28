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
        self.members: list[Member] = self.load_members()
        self.member: Member | None = None

    # members.json 파일에서 회원 정보 불러오기
    def load_members(self) -> list[Member]:
        """members.json 파일에서 회원 정보 불러오기"""

        if not self.file_path.exists():
            return []

        with self.file_path.open('r', encoding='utf-8') as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError('회원 JSON 데이터는 리스트여야 합니다.')

        return [Member(**item) for item in data]

    # members.json 파일에 회원 정보 저장
    def save_members(self) -> None:
        """members.json 파일에 회원 정보 저장"""

        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        with self.file_path.open('w', encoding='utf-8') as file:
            json.dump(
                [member.to_dict() for member in self.members],
                file,
                ensure_ascii=False,
                indent=4,
            )

    # 회원 정보 존재 여부 확인
    def is_exist(self, member_id: str) -> bool:
        """회원ID로 존재 여부 확인"""

        for member in self.members:
            if member_id == member.member_id:
                return True
        return False

    # 개별 항목 유효성 검사
    def is_valid_field(self, field: str, value: object) -> bool:
        """회원가입, 회원 수정 시 입력한 데이터 유효성 검사"""

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
        """회원가입 시 입력한 데이터 유효성 검사"""

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
    def do_member_save(
        self,
        member_id: str,
        name: str,
        password: str,
        email: str,
        phone: str,
        role: str = 'USER',
    ) -> bool:
        """회원가입(회원 정보 추가) 기능"""

        member = Member(member_id, name, password, email, phone, role)

        # 회원 정보 유효성 검사
        if not self.is_valid_member(member):
            print('회원 정보를 정확하게 입력해주세요.')
            return False

        # 아이디 중복 검사
        if self.is_exist(member_id):
            print('이미 존재하는 회원 ID입니다.')
            return False

        self.members.append(member)

        try:
            self.save_members()
        except Exception as e:
            self.members.pop()
            print('회원 정보 저장 중 오류 발생:', e)
            return False

        return True

    # 회원 전체 조회
    def do_retrieve(self) -> list[Member]:
        """전체 회원 조회"""

        if not self.members:
            print('존재하는 회원이 없습니다.')

        return self.members.copy()

    # 회원 검색
    def do_search_members(
        self,
        field: str | None = None,
        keyword: str | None = None,
        sort_by: str | None = None,
        descending: bool = False,
    ) -> list[Member]:
        """회원 검색 기능"""

        # 검색 및 정렬 조건 검사
        if field not in ('member_id', 'name', 'email', 'phone', None):
            return []

        if sort_by not in ('name', 'reg_date', None):
            return []

        # 검색 조건과 검색어는 함께 입력해야 함
        if (field is None) != (keyword is None):
            return []

        result = self.members.copy()

        # 검색 조건이 있는 경우
        if field is not None:
            if not isinstance(keyword, str) or not keyword.strip():
                return []

            result = [
                member
                for member in result
                if keyword.casefold() in getattr(member, field).casefold()
            ]

        # 정렬 조건이 있는 경우
        if sort_by is not None:
            result.sort(
                key=lambda member: getattr(member, sort_by),
                reverse=descending,
            )

        return result

    # 회원 수정 유효성 검사
    def is_valid_update_member(
        self,
        member_id: str,
        name: str | None = None,
        password: str | None = None,
        email: str | None = None,
        phone: str | None = None,
    ) -> bool:
        """회원 정보 수정 유효성 검사"""

        # 아이디 검사
        if not self.is_valid_field('member_id', member_id):
            return False

        fields = {
            'name': name,
            'password': password,
            'email': email,
            'phone': phone,
        }

        # 수정할 정보가 없는 경우
        if all(value is None for value in fields.values()):
            return False

        # 입력한 항목만 유효성 검사
        for field, value in fields.items():
            if value is not None and not self.is_valid_field(field, value):
                return False

        return True

    # 회원 정보 수정
    def do_member_update(
        self,
        member_id: str,
        name: str | None = None,
        password: str | None = None,
        email: str | None = None,
        phone: str | None = None,
    ) -> bool:
        """회원 정보 수정 기능"""

        # 회원 수정 유효성 검사
        if not self.is_valid_update_member(member_id, name, password, email, phone):
            print('수정할 회원 정보를 확인해주세요.')
            return False

        for index, current_member in enumerate(self.members):
            if member_id == current_member.member_id:
                # 기존 회원 정보를 딕셔너리로 복사
                member_data = current_member.to_dict()

                if name is not None:
                    member_data['name'] = name

                if password is not None:
                    member_data['password'] = password

                if email is not None:
                    member_data['email'] = email

                if phone is not None:
                    member_data['phone'] = phone

                # 수정된 회원 객체로 교체
                member = Member(**member_data)
                self.members[index] = member

                try:
                    self.save_members()
                except Exception as e:
                    self.members[index] = current_member
                    print('회원 정보 수정 중 오류 발생:', e)
                    return False

                # 로그인한 회원의 정보라면 갱신
                if self.member is current_member:
                    self.member = member

                print('회원 정보가 수정되었습니다.')
                return True

        print('존재하는 회원이 없습니다.')
        return False

    # 회원 삭제
    def do_member_delete(self, member_id: str) -> bool:
        """회원 정보 삭제 기능"""

        # 관리자 권한 확인
        is_admin = any(
            member.member_id == member_id and member.role == 'ADMIN'
            for member in self.members
        )

        if not is_admin:
            print('관리자만 회원을 삭제할 수 있습니다.')
            return False

        # 회원 삭제
        for index, member in enumerate(self.members):
            if member_id == member.member_id:
                self.members.pop(index)

                try:
                    self.save_members()
                except Exception as e:
                    self.members.insert(index, member)
                    print('회원 삭제 중 오류 발생:', e)
                    return False

                # 현재 로그인한 회원이 삭제된 경우
                if self.member is member:
                    self.member = None

                print('회원 삭제가 완료되었습니다.')
                return True

        print('회원 정보가 없습니다.')
        return False

    # 로그인
    def login(self, member_id: str, password: str) -> bool:
        """로그인 기능"""

        self.member = None

        if (
            not isinstance(member_id, str)
            or not member_id.strip()
            or not isinstance(password, str)
            or not password.strip()
        ):
            print('아이디 혹은 비밀번호를 필수로 입력해주세요.')
            return False

        for member in self.members:
            if member_id == member.member_id and password == member.password:
                self.member = member
                print('로그인에 성공하였습니다.')
                return True

        print('아이디 혹은 비밀번호가 일치하지 않습니다.')
        return False
