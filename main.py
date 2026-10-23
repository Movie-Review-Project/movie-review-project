# from managers.member_manager import add_member
import json
import os
from datetime import datetime

# 임시 클래스
class Member:
    def __init__(self, member_id=str, name=str, password=str, email=str, phone=str, reg_date=str, role = str):

        if not member_id.strip():
            raise ValueError("회원 ID는 필수입니다.")

        if not name.strip():
            raise ValueError("이름은 필수입니다.")

        if "@" not in email:
            raise ValueError("이메일 형식이 올바르지 않습니다.")

        if not password:
            raise ValueError("패스워드는 필수입니다.")
        
        self.member_id = member_id
        self.name = name
        self.password = password
        self.email = email
        self.phone = phone
        self.reg_date = reg_date
        self.role = role

# 임시 더미 리스트
dummy_db = {
    "testuser": {
        "member_id": "testuser",
        "name": "홍길동",
        "phone": "010-1234-5678",
        "email": "test@naver.com",
        "password": "123",
        "reg_date": "2026-10-20",
        "role": "USER"
    },
    "admin123": {
        "member_id": "admin123",
        "name": "관리자",
        "phone": "010-0000-0000",
        "email": "admin@naver.com",
        "password": "123",
        "reg_date": "2026-10-22",
        "role": "admin"
    }
}

# 시작 화면
def show_start_menu():
    print("="*50)
    print("(영화 리뷰 & 관람 기록 관리 시스템)")
    print("="*50)
    print("1. 회원가입")
    print("2. 로그인")
    print("="*50)
    start = int(input("선택:"))
    print("")
    return start

# 테스트용 (나중에 member_manager.py의 add_member불러올 때 지우기)
def add_member(member_id="pcwk", name="이상무", phone="010-1111-2222", email="jamesol@naver.com", password="asd123", reg_date = "2026-10-23", role="USER"):
    # print(f"\n[시스템 텍스트] {name}님의 정보 전달 성공!")
    return member_id, name, password, reg_date, role
# ---

# 회원 가입 선택 시
def register():
    print("사용자 정보를 입력해주세요.")
    member_id = input("ID: ")
    name = input("이름: ")
    phone = input("연락처: ")
    email = input("Email: ")
    password = input("비밀번호: ")
    reg_date = datetime.now().strftime("%Y년%m월%d일")
    role = "USER"

    result = add_member(member_id, name, phone, email, password, reg_date, role)

    if result:
        # 임시 DB
        dummy_db[member_id] = {
            "member_id": member_id,
            "name": name,
            "phone": phone,
            "email": email,
            "password": password,
            "reg_date": reg_date,
            "role": role
            
        }
        print(f"{name}님 환영합니다! 회원 가입이 완료되었습니다.")
        return Member(member_id, name, phone, email, password, role)
    else:
        print("회원 가입에 실패했습니다.")
        return False

# 로그인 선택 시
def login() -> bool: 
    member_id = input("ID를 입력하세요: ")
    password = input("비밀번호를 입력하세요: ")

    #### 임시
    if member_id in dummy_db and dummy_db[member_id]["password"] == password and dummy_db[member_id]["role"] == "admin":
        print("관리자 계정으로 로그인 되었습니다.")
        user_info = dummy_db[member_id]
        return Member(
            user_info["member_id"],
            user_info["name"],
            user_info["phone"],
            user_info["email"],
            user_info["password"],
            user_info["reg_date"],
            user_info["role"],
        )
    
    elif member_id in dummy_db and dummy_db[member_id]["password"] == password:
        print("로그인 되었습니다.")
        # 임시
        user_info = dummy_db[member_id]
        return Member(
            user_info["member_id"],
            user_info["name"],
            user_info["phone"],
            user_info["email"],
            user_info["password"],
            user_info["reg_date"],
            user_info["role"],
        )
    else:
        print("\n등록된 아이디가 없거나 비밀번호가 일치하지 않습니다.")
        return False
    # ###

# 로그인 후
def show_main_menu(user):
    print("="*50)
    print(f"{user.name}님 안녕하세요.")
    print("1. 영화검색")
    print("2. 리뷰조회")
    print("3. 리뷰작성")

    if user.role == "admin":
        print("4. 회원조회")
    print("="*50)
    menu = int(input("선택: "))
    return menu

# 4. 회원 조회 선택할 경우
def member_info():
    pass
    # 임시 작성
    # file_path = r"멤버.json 경로"
    # # json 파일 여부 확인
    # if not os.path.exists(file_path):
    #     print("\nmembers.json 파일 조회 불가.")
    #     return
    # # json 파일 읽어오기
    # with open(file_path, "r", encoding="utf-8") as f:
    #     members = json.load(f)

# 임시 멤버 리스트
    members = [{"member_id": "pc01", "name": "김철수", "password": "1234", "email": "jamesol@naver.com", "phone": "010-0111-1110", "reg_date": "2026년10월23일", "role": "USER"}]
    admin_keyword = input("\n회원 정보를 입력해주세요. (ID, 이름, 연락처, Email)\n:")

    right_members = [mb for mb in members if admin_keyword in mb.get("member_id", "")]
    if not right_members:
        print("\n회원을 조회할 수 없습니다.")
        right_members = members


# 영화 검색 선택할 경우
def find_movie():
    # 파일 경로
    file_path = r"C:\AI_CAMP_20260921\98_PROJECT\movie-review-project\example_data\movies.json"

    # json 파일 여부 확인
    if not os.path.exists(file_path):
        print("\nmovies.json 파일 조회 불가.")
        return
    # json 파일 읽어오기
    with open(file_path, "r", encoding="utf-8") as f:
        movies = json.load(f)

    keyword = input("\n검색할 영화 제목을 입력하세요: ")

    right_movies = [mv for mv in movies if keyword in mv.get("movie_name", "")]

    if not right_movies:
        print("="*50)
        print("\n검색어와 관련한 영화 정보를 찾을 수 없습니다.\n전체 영화 리스트를 출력합니다.")
        print("="*50)
        right_movies = movies
    else:
        print(f"\n[{keyword}] 검색 결과 -> {len(right_movies)}개")

    for index, mv in enumerate(right_movies, start=1):
        mvname = mv.get("movie_name")
        print(f"{index}. {mvname}")

    print("="*50)
    try:
        choice = int(input("상세 정보를 볼 영화의 번호를 입력하세요.\n\n0을 입력하면 영화 검색 화면으로 돌아갑니다."))

        if choice == 0:
            return find_movie()

        if 1 <= choice <= len(right_movies):
            show_movie_info = right_movies[choice - 1]

            print("="*50)
            print(show_movie_info.get("movie_name"))
            print("="*50)
            print(f"장르: {show_movie_info.get("movie_genre")}")
            print(f"개봉일: {show_movie_info.get("movie_release")}")
            print(f"러닝타임: {show_movie_info.get("movie_running_time")}분")
            print(f"줄거리: {show_movie_info.get("movie_intro")}")

            # 나중에 만들 평균평점 출력
            # print(f"평균평점: {}")
            # 리뷰 Top3 출력 (연결 방법도 따로 만들기)
            # print("-"*50)
            # print(f"리뷰 TOP 3 : {}")
        else:
            print("="*50)
            print("목록에 없는 번호입니다.")
            return find_movie()

    except ValueError:
        print("="*50)
        print("[잘못된 접근입니다.]\n화면에 보이는 영화 리스트의 맨 앞 숫자만 입력해주세요.")
        return find_movie()
    
def main():
    # 시작 화면
    is_login = False
    while is_login == False:
        start = show_start_menu()
        while start != 1 and start != 2:
            print("다시선택")
            start = show_start_menu()

        if start == 1: # 회원가입
            is_login = register()

        elif start == 2: # 로그인
            is_login = login()
    # 로그인 후
    menu = show_main_menu(is_login)

    if menu == 1:
        find_movie()
    elif menu == 4:
        member_info()



if __name__ == "__main__":
    main()