from managers.member_manager import MemberManager
from managers.movie_manager import MovieManager
from managers.review_manager import ReviewManager
#  ↓ .py 끌어오면 날릴것들 ↓
import json
import os
from datetime import datetime
from types import SimpleNamespace


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

# 임시 클래스
# class Member:
#     def __init__(self, member_id=str, name=str, password=str, email=str, phone=str, reg_date=str, role = str):

#         if not member_id.strip():
#             raise ValueError("회원 ID는 필수입니다.")

#         if not name.strip():
#             raise ValueError("이름은 필수입니다.")

#         if "@" not in email:
#             raise ValueError("이메일 형식이 올바르지 않습니다.")

#         if not password:
#             raise ValueError("패스워드는 필수입니다.")
        
#         self.member_id = member_id
#         self.name = name
#         self.password = password
#         self.email = email
#         self.phone = phone
#         self.reg_date = reg_date
#         self.role = role

# 임시 더미 리스트
# dummy_db = {
#     "testuser": {
#         "member_id": "testuser",
#         "name": "홍길동",
#         "phone": "010-1234-5678",
#         "email": "test@naver.com",
#         "password": "123",
#         "reg_date": "2026-10-20",
#         "role": "USER"
#     },
#     "admin123": {
#         "member_id": "admin123",
#         "name": "관리자",
#         "phone": "010-0000-0000",
#         "email": "admin@naver.com",
#         "password": "123",
#         "reg_date": "2026-10-22",
#         "role": "admin"
#     }
# }

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
        print(f"{idx+1}. {review.member_id} | {review.rating}점 | 추천 {""} | 비추천 {""}")
        print(f"   {review.review}")


# 회원 가입 선택 시
def register(member_manager):
    print("사용자 정보를 입력해주세요.")
    
    member_id = input("ID: ").strip()
    name = input("이름: ").strip()
    phone = input("연락처: ").strip()
    email = input("Email: ").strip()
    password = input("비밀번호: ").strip()

    if not member_id or not name or not phone or not email or not password:
        print("회원가입 실패. 모든 항목을 입력해주세요.")
        return False
    
    result = member_manager.do_member_save(
        member_id, name, password, email, phone
        )

    if result:
        print(f"{name}님 환영합니다! 회원가입이 완료되었습니다.")
        return True
    else:
        print("회원 가입에 실패했습니다.")
        return False

# 로그인 선택 시
def login(member_manager) -> bool: 
    member_id = input("ID를 입력하세요: ").strip()
    password = input("비밀번호를 입력하세요: ").strip()

    #### 임시
    for member in member_manager.members:
        if str(member["member_id"]) == member_id:
            if member["password"] == password:

                if member.get("role", "USER").upper() == "ADMIN":
                    print("관리자 계정으로 로그인 되었습니다.")

                else:
                    print("로그인 되었습니다.")

                return member

            else:
                print("비밀번호가 일치하지 않습니다.")
                return None
    else:
        print("아이디가 존재하지 않습니다.")
    return None
        # user_info = dummy_db[member_id]
        # return Member(
        #     user_info["member_id"],
        #     user_info["name"],
        #     user_info["phone"],
        #     user_info["email"],
        #     user_info["password"],
        #     user_info["reg_date"],
        #     user_info["role"],
        # )
    
    # elif member_id in dummy_db and dummy_db[member_id]["password"] == password:
    #     print("로그인 되었습니다.")
    #     # 임시
    #     user_info = dummy_db[member_id]
    #     return Member(
    #         user_info["member_id"],
    #         user_info["name"],
    #         user_info["phone"],
    #         user_info["email"],
    #         user_info["password"],
    #         user_info["reg_date"],
    #         user_info["role"],
    #     )
    # else:
    #     print("\n등록된 아이디가 없거나 비밀번호가 일치하지 않습니다.")
    #     return False
    # ###

# 로그인 후
def show_main_menu(user):
    print("="*50)
    print(f"{user.name}님 안녕하세요.")
    print("1. 영화검색")
    print("2. 리뷰조회")
    print("3. 리뷰작성")
    
    if user.get("role", "USER").upper() == "ADMIN":
        print("4.회원조회")
    print("5. 종료")

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

# 리뷰 작성
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
            while True:
                try:
                    rate = float(input("평점을 입력해주세요 (0-5): "))
                    if 0<= rate <=5:
                        break
                    print("0~5 사이의 점수를 입력해주세요")
                except ValueError:
                    print("숫자를 입력해주세요")
            while True:
                content = input("리뷰를 작성해주세요: ").strip()
                if not content:
                    print("리뷰 내용을 입력해주세요")
                    continue
                if len(content) > 100:
                    print("리뷰는 100자 이내로 작성해주세요")
                    continue
                break
            while True:
                recommand = input("추천 하시겠습니까? (y/n)").strip().lower()
                if recommand == 'y' or recommand == 'n':
                    break
                print("y 또는 n을 입력해주세요")
            
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

            

# 4. 회원 조회 선택할 경우
def member_info(member_manager):

    members = member_manager.do_retrieve()

    if not members:
        return
    
    # 임시 작성
    # file_path = r"멤버.json 경로"
    # # json 파일 여부 확인
    # if not os.path.exists(file_path):
    #     print("\nmembers.json 파일 조회 불가.")
    #     return
    # # json 파일 읽어오기
    # with open(file_path, "r", encoding="utf-8") as f:
    #     members = json.load(f)


    # 회원 조회
    admin_keyword = input("\n회원 정보를 입력해주세요. (ID, 이름, 연락처, Email)\n:").strip()

    right_members = []

    for member in members:
        if (
            admin_keyword in str(member.get("member_id", ""))
            or admin_keyword in member.get("name", "")
            or admin_keyword in member.get("phone", "")
            or admin_keyword in member.get("email", "")
        ):
            right_members.append(member)

    if not right_members:
        print("\n회원을 조회할 수 없습니다.")
        right_members = members

    for idx, member in enumerate(right_members):
        print("=" * 50)
        print(f"회원번호: {idx+1}")
        print(f"ID: {member.get('member_id', '')}")
        print(f"이름: {member.get('name', '')}")
        print(f"연락처: {member.get('phone', '')}")
        print(f"Email: {member.get('email', '')}")
        print(f"가입일: {member.get('reg_date', '')}")
        print(f"권한: {member.get('role', 'USER')}")


    # 관리자 메뉴 출력
    print("="*50)
    print("1. 회원 정보 수정")
    print("2. 회원 삭제")
    print("0. 돌아가기")

    admin_menu = input_int("선택: ", 1, 0)

    if admin_menu == 0:
        return

    #####작성중!!!!! 수정 또는 삭제할 멤버 선택
    member_number = input_int("회원 번호를 입력하세요", 1, len(right_members))

    selected_member = right_members[member_number - 1]
    member_id = selected_member["member_id"]

# 영화 검색 선택할 경우
def find_movie(movie_manager):
    ### 임시 json 끌어오기, 아래 주석 끝 부분까지 movie_manager 연결 후 삭제
    file_path = r"C:\AI_CAMP_20260921\98_PROJECT\movie-review-project\data\movies.json"

    # json 파일 여부 확인
    if not os.path.exists(file_path):
        print("\nmovies.json 파일 조회 불가.")
        return
    # json 파일 읽어오기
    with open(file_path, "r", encoding="utf-8") as file:
        movies_data = json.load(file)

    movies = []

    for mv in movies_data:
        movie = SimpleNamespace(**mv)

        movie.name = mv.get("movie_name", "")

        movies.append(movie)
    ### 여기까지 movie_manager 끌어오면 삭제

    if not movies:
        print("\n등록된 영화가 없습니다.")
        return

    while True:

        keyword = input("\n검색할 영화 제목을 입력하세요: ")

        # 영화 제목 검색 시 일부, 전체 출력 여부
        right_movies = [
            movie for movie in movies
            if keyword in movie.name
        ]

        # 검색 결과 조회 안되는 경우
        if not right_movies:
            print("="*50)
            print("\n검색어와 관련한 영화 정보를 찾을 수 없습니다.\n전체 영화 리스트를 출력합니다.")
            print("="*50)
            right_movies = movies
    
        else:
            print(f"\n[{keyword}] 검색 결과 -> {len(right_movies)}개")

        # 영화 목록 출력 (1번부터 마킹)
        for idx, movie in enumerate(right_movies):
            print(f"{idx+1}. {movie.name}")

        print("="*50)
    
        # 상세 정보 조회
        try:
            choice = int(input(
                "상세 정보를 열람할 영화의 번호를 입력하세요.\n"
                "0을 입력하면 영화 검색 화면으로 돌아갑니다.\n"
                "선택: "
            ))

            if choice == 0:
                continue

            if 1 <= choice <= len(right_movies):
                show_movie_info = right_movies[choice - 1]

                print("="*50)
                print(show_movie_info.name)
                print("="*50)

                print(f"장르: {show_movie_info.movie_genre}")
                print(f"개봉일: {show_movie_info.movie_release}")
                print(f"러닝타임: {show_movie_info.movie_running_time}분")
                print(f"줄거리: {show_movie_info.movie_intro}")

                # 나중에 만들 평균평점 출력
                # print(f"평균평점: {}")
                # 리뷰 Top3 출력 (연결 방법도 따로 만들기)
                # print("-"*50)
                # print(f"리뷰 TOP 3 : {}")
                return

            else:
                print("="*50)
                print("목록에 없는 번호입니다.")
                continue
        except ValueError:
            print("="*50)
            print("잘못된 접근입니다.\n화면에 보이는 영화 리스트의 맨 앞 숫자만 입력해주세요.")
            continue
    
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
    while(menu != 5):
        show_main_menu(member_manager.member)
        menu = input_int("선택: ", 1, 5)
        if menu == 1:
            find_movie(movie_manager)
        elif menu == 2: # 영화 리뷰 조회
            view_review(movie_manager, review_manager)
        elif menu == 3: # 리뷰 작성
            create_review(member_manager, movie_manager, review_manager)
        elif menu == 4:
            member_info()



if __name__ == "__main__":
    main()
