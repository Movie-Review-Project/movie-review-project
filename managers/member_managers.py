from models.member import Member

class MemberManager:
    def __init__(self):
        self.members = []
        self.member = Member("admin", "이름", "asdf", "dlf@dd.com", "admin")


