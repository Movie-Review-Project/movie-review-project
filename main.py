# from managers.member_manager import add_member
from managers.member_manager import MemberManager
from managers.movie_manager import MovieManager
from managers.review_manager import ReviewManager

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

# 정수 입력 (출력문구, min~max)
def input_int(prompt, min_val, max_val):
    while True:
        try:
            num = int(input(prompt))
        except ValueError:
            print("정수를 입력해주세요")
            continue
        if min_val <= num <= max_val:
            return num
        print(f"{min_val}~{max_val} 사이의 숫자를 입력해주세요")

# 리뷰 내용 입력
def input_review_info(allow_empty = False):
    while True:
        rate = input("평점을 입력해주세요 (0-5): ").strip()
        if not rate and allow_empty:
            rate = None
            break
        try:
            rate = float(rate)
            if 0<= rate <=5:
                break
            print("0~5 사이의 점수를 입력해주세요")
        except ValueError:
            print("숫자를 입력해주세요")
    while True:
        content = input("리뷰를 작성해주세요: ").strip()
        if not content:
            if allow_empty:
                content = None
                break
            print("리뷰 내용을 입력해주세요")
            continue
        if len(content) > 100:
            print("리뷰는 100자 이내로 작성해주세요")
            continue
        break
    while True:
        recommand = input("추천 하시겠습니까? (y/n)").strip().lower()
        if not recommand and allow_empty:
            recommand = None
            break
        if recommand == 'y' or recommand == 'n':
            break
        print("y 또는 n을 입력해주세요")

    return rate, content, recommand

# 시작 화면
def show_start_menu():
    print("="*50)
    print("(영화 리뷰 & 관람 기록 관리 시스템)")
    start = input_int("선택: ", 1, 2)
    print()
    return start

# 영화 목록 출력
def show_movie_list(movie_manager):
    movie_list = movie_manager.movies
    print("="*50)
    print("영화 목록")
    print("="*50)
    for idx, movie in enumerate(movie_list):
        print(f"{idx+1}. {movie.name}")

# 리뷰 출력
def show_review(review_manager, movie, sort):
    reviews = review_manager.do_review_retrieve(movie.movie_id, sort)
    print("="*50)
    print(f"리뷰 목록 - {movie.movie_name}")
    print("="*50)
    print(f"평균평점 : {review_manager.do_review_avg_rating(movie.movie_id)} / 5.0 (리뷰 {len(reviews)})")
    print("-"*50)
    for idx, review in enumerate(reviews):
        print(f"{idx+1}. {review.member_id} | {review.rating}점 | {'추천' if review.recommand == 'y' else '비추천'}")
        print(f"   {review.review}")


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
    print("2. 영화 리뷰조회")
    print("3. 리뷰작성")
    print("4. 내 리뷰 조회 및 수정")
    if user.role == "admin":
        print("5.회원조회")
    print("6. 종료")

# 2. 리뷰 조회
def view_review(movie_manager, review_manager): 
    print("영화를 선택해 주세요")
    print("="*50)
    show_movie_list(movie_manager)
    movie_idx = input_int("영화번호: ", 1, len(movie_manager.movies))-1 

    movie_manager.movie = movie_manager.movies[movie_idx]
    
    print("리뷰 정렬 방법을 선택해 주세요")
    print("1. 최신    2. 평점")
    sort = input_int("정렬방법: ", 1, 2)
    show_review(review_manager, movie_manager.movie, sort)

# 3. 리뷰 작성
def create_review(member_manager, movie_manager, review_manager):
    is_exit = False
    while not is_exit:
        print("영화를 선택해 주세요")
        print("="*50)
        show_movie_list(movie_manager)
        movie_idx = input_int("영화번호: ", 1, len(movie_manager.movies))-1 
        movie_manager.movie = movie_manager.movies[movie_idx]
        print("="*50)
        print("리뷰 작성 -", movie_manager.movie.movie_name)
        
        while True:
            rate, content, recommand = input_review_info()
            success = review_manager.do_review_save(member_manager.member.member_id, movie_manager.movie.movie_id, rate, content, recommand)
            if not success:
                print("실패했습니다")
                print("1. 다시 작성    2. 종료")
                choose = input_int("선택: ", 1, 2)
                if choose == 1:
                    continue
                else:
                    is_exit = True
                    break
            else:
                break

        while not is_exit:
            write_more = input("추가 작성하시겠습니까? (y/n)").strip().lower()
            if write_more not in ('y', 'n'):
                print("y 또는 n을 입력해주세요")
                continue
            if write_more == 'n':
                is_exit = True
            break

# 내 리뷰 조회 및 수정
def update_review(member_manager, review_manager):
    while True:
        reviews = review_manager.do_personal_review_retrieve(member_manager.member.member_id)
        for idx, review in enumerate(reviews):
            print(f"{idx+1}. {review.show_info()}")
        print("리뷰 번호와 (수정/삭제)를 선택해 주세요")
        review_idx = input_int("리뷰 번호: ", 1, len(reviews))
        action = input_int("1. 수정  2.삭제: ", 1, 2)
        review = reviews[review_idx-1]
        if action == 1:
            print("수정할 내용을 입력해 주세요 없다면 enter를 눌러주세요")
            rate, content, recommand = input_review_info(allow_empty = True)
            success = review_manager.do_personal_review_update(review, rating=rate, content=content, recommand=recommand)
            if success:
                print("성공적으로 수정되었습니다")
            else:
                print("수정에 실패했습니다")
        else:
            success = review_manager.do_personal_review_delete(review)
            if success:
                print("성공적으로 삭제되었습니다")
            else:
                print("삭제에 실패했습니다")
        action = input_int("1. 추가 작업 진행   2. 종료: ", 1, 2)
        if action == 2:
            break 

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
    member_manager = MemberManager()
    movie_manager = MovieManager()
    review_manager = ReviewManager()
    
    while member_manager.member is None:
        start = show_start_menu()

        if start == 1: # 회원가입
            is_login = register()

        elif start == 2: # 로그인
            login()
    # 로그인 후
    menu = 0
    while(menu != 6):
        show_main_menu(member_manager.member)
        menu = input_int("선택: ", 1, 6)
        if menu == 1:
            find_movie()
        elif menu == 2: # 영화 리뷰 조회
            view_review(movie_manager, review_manager)
        elif menu == 3: # 리뷰 작성
            create_review(member_manager, movie_manager, review_manager)
        elif menu == 4: # 리뷰 수정
            update_review(member_manager, review_manager)
        elif menu == 5:
            if member_manager.member.role != "admin":
                print("회원 조회는 관리자만 할 수 있습니다")
                continue

            member_info()



if __name__ == "__main__":
    main()
