class Member:
    def __init__(self, member_id, name, password, email, role):
        self.member_id = member_id
        self.name = name
        self.password = password
        self.email = email
        self.role = role
        self.reg_date = None