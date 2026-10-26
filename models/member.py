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
    ) -> None:
        self.__member_id = member_id
        self.__name = name
        self.__password = password
        self.__email = email
        self.__phone = phone
        self.__reg_date = datetime.date.today().isoformat()
        self.__role = role

    @property
    def member_id(self):
        return self.__member_id

    @property
    def name(self):
        return self.__name

    @property
    def password(self):
        return self.__password

    @property
    def email(self):
        return self.__email

    @property
    def phone(self):
        return self.__phone

    # JSON 저장용 딕셔너리 변환
    def to_dict(self):
        return {
            'member_id': self.__member_id,
            'name': self.__name,
            'password': self.__password,
            'email': self.__email,
            'phone': self.__phone,
            'reg_date': self.__reg_date,
            'role': self.__role,
        }
