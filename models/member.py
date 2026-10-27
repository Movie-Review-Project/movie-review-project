# member.py
import datetime


class Member:
    def __init__(
        self,
        member_id: str,
        name: str | None = None,
        password: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        role: str = 'USER',
        reg_date: str | None = None,
    ) -> None:
        self.__member_id = member_id
        self.__name = name
        self.__password = password
        self.__email = email
        self.__phone = phone
        self.__reg_date = reg_date or datetime.date.today().isoformat()
        self.__role = role

    @property
    def member_id(self) -> str:
        return self.__member_id

    @property
    def name(self) -> str | None:
        return self.__name

    @property
    def password(self) -> str | None:
        return self.__password

    @property
    def email(self) -> str | None:
        return self.__email

    @property
    def phone(self) -> str | None:
        return self.__phone

    @property
    def reg_date(self) -> str:
        return self.__reg_date

    @property
    def role(self) -> str:
        return self.__role

    def to_dict(self) -> dict:
        """회원 객체를 딕셔너리로 변환"""
        return {
            'member_id': self.__member_id,
            'name': self.__name,
            'password': self.__password,
            'email': self.__email,
            'phone': self.__phone,
            'reg_date': self.__reg_date,
            'role': self.__role,
        }
