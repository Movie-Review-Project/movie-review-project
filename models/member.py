# member.py
import datetime


class Member:
    def __init__(
        self,
        member_id: str,
        name: str,
        password: str,
        email: str,
        phone: str,
        role: str = 'USER',
    ) -> None:
        self.member_id = member_id
        self.name = name
        self.password = password
        self.email = email
        self.phone = phone
        self.reg_date = datetime.date.today().isoformat()
        self.role = role
