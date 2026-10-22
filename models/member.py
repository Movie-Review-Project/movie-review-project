# member.py
import datetime


class Member:

    def __init__(self, member_id, name, password, email, phone, role='USER'):
        self.member_id = member_id
        self.name = name
        self.password = password
        self.email = email
        self.phone = phone
        self.reg_date = datetime.date('YYYY-MM-DD')
        self.role = role