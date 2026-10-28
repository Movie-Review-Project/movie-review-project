from managers.member_manager import MemberManager
from managers.movie_manager import MovieManager
from managers.review_manager import ReviewManager

# 정수 입력 (출력문구, min~max)
def input_int(prompt, min_val, max_val):
    while True:
        try:
            print("="*50)
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
        print("="*50)
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
        recommend = input("추천 하시겠습니까? (y/n)").strip().lower()
        if not recommend and allow_empty:
            recommend = None
            break
        if recommend == 'y' or recommend == 'n':
            break
        print("y 또는 n을 입력해주세요")

    return rate, content, recommend

# 시작 화면
def show_start_menu():
    print("="*50)
    print("(영화 리뷰 & 관람 기록 관리 시스템)")
    print("1. 회원가입   2. 로그인")
    start = input_int("선택: ", 1, 2)
    print()
    return start

# 영화 목록 출력
def show_movie_list(movie_list):
    print("영화를 선택해 주세요")
    print("="*50)
    print("영화 목록")
    print("="*50)
    for idx, movie in enumerate(movie_list):
        print(f"{idx+1}. {movie.movie_name}")
    movie_idx = input_int("영화번호: ", 1, len(movie_list))-1 
    movie = movie_list[movie_idx]
    return movie

# 리뷰 출력
def show_review(review_manager, movie, sort):
    reviews = review_manager.do_review_retrieve(movie.movie_id, sort)
    if not reviews:
        print("리뷰가 존재하지 않습니다")
    else:
        print("="*50)
        print(f"리뷰 목록 - {movie.movie_name}")
        print("-"*50)
        print(f"평균평점 : {review_manager.do_review_avg_rating(movie.movie_id)} / 5.0 (리뷰 {len(reviews)}개)")
        print("-"*50)
        for idx, review in enumerate(reviews):
            print(f"{idx+1}. {review.member_id} | {review.rating}점 | {'추천' if review.recommend == 'y' else '비추천'}")
            print(f"   {review.review}")


# 회원 가입 선택 시
def register(member_manager):
    print("사용자 정보를 입력해주세요.")
    
    member_id = input("ID: ").strip()
    name = input("이름: ").strip()
    phone = input("연락처: ").strip()
    email = input("Email: ").strip()
    password = input("비밀번호 (영문+숫자 조합 8~10자): ").strip()

    # 권한 받아서 넘겨주기
    print("="*50)
    print("1. 관리자")
    print("2. 일반 회원")
    role_menu = input_int("권한 선택", 1, 2)

    if role_menu == 1:
        role = "ADMIN"
    else:
        role = "USER"

    if not member_id or not name or not phone or not email or not password:
        print("회원가입 실패. 모든 항목을 입력해주세요.")
        return False
    
    result = member_manager.do_member_save(
        member_id, name, password, email, phone, role
        )

    if result:
        print(f"{name}님 환영합니다! 회원가입이 완료되었습니다.")
        return True
    else:
        print("회원 가입에 실패했습니다.")
        return False

# 로그인 선택 시
def login(member_manager): 
    member_id = input("ID를 입력하세요: ").strip()
    password = input("비밀번호를 입력하세요: ").strip()

    if not member_manager.login(member_id, password):
        return None

    for member in member_manager.members:
        if member.member_id == member_id:
            if member.role == "ADMIN":
                print("관리자 계정으로 로그인 되었습니다.")

            return member

    return None

# 로그인 후
def show_main_menu(member_manager):
    print("="*50)
    print(f"{member_manager.member.name}님 안녕하세요.\n")
    print("1. 영화검색")
    print("2. 영화 리뷰조회")
    print("3. 리뷰작성")
    print("4. 내 리뷰 조회 및 수정")
    print("5. 회원조회")
    print("6. 종료")
 
# 2. 리뷰 조회
def view_review(movie_manager, review_manager): 
    print("검색할 영화 제목을 입력해주세요, 리스트를 보고싶으시면 enter를 눌러주세요")
    keyword = input("검색할 영화 제목을 입력하세요: ").strip()
    print()
    movie = None
    if not keyword:
        movie = show_movie_list(movie_manager.movies)
    else:    
        right_movies = [
            movie for movie in movie_manager.movies
            if keyword in movie.movie_name
        ]
        if not right_movies:
            print("일치하는 영화가 없습니다")
            movie = show_movie_list(movie_manager.movies)
        else:
            movie = show_movie_list(right_movies)

    print("리뷰 정렬 방법을 선택해 주세요")
    print("1. 최신    2. 평점")
    sort = input_int("정렬방법: ", 1, 2)
    show_review(review_manager, movie, sort)

# 3. 리뷰 작성
def create_review(member_manager, movie_manager, review_manager):
    is_exit = False
    while not is_exit:
        print("="*50)
        print("리뷰를 작성할 영화 제목을 입력해주세요, 리스트를 보고싶으시면 enter를 눌러주세요")
        keyword = input("검색할 영화 제목을 입력하세요: ").strip()
        print()
        movie = None
        if not keyword:
            movie = show_movie_list(movie_manager.movies)
        else:    
            right_movies = [
                movie for movie in movie_manager.movies
                if keyword in movie.movie_name
            ]
            if not right_movies:
                print("일치하는 영화가 없습니다")
                movie = show_movie_list(movie_manager.movies)
            else:
                movie = show_movie_list(right_movies)
        
        print("="*50)
        print("리뷰 작성 -", movie.movie_name)
        
        while True:
            rate, content, recommend = input_review_info()
            success = review_manager.do_review_save(member_manager.member.member_id, movie.movie_id, rate, content, recommend)
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
                print("리뷰 작성을 성공했습니다")
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
def update_review(member_manager, review_manager, movie_manager):
    while True:
        reviews = review_manager.do_personal_review_retrieve(member_manager.member.member_id)
        if not reviews:
            print("리뷰가 존재하지 않습니다")
        else:
            print("-"*50)
            for idx, review in enumerate(reviews):
                print(f"{idx+1}. {movie_manager.id_to_name(review.movie_id)} | {review.rating} | 관람 {review.reg_date} | {"추천" if review.recommend == 'y' else "비추천"}")
                print(review.review)
            print("리뷰 번호와 (수정/삭제)를 선택해 주세요")
            review_idx = input_int("리뷰 번호: ", 1, len(reviews))
            action = input_int("1. 수정  2.삭제: ", 1, 2)
            review = reviews[review_idx-1]
            if action == 1:
                print("수정할 내용을 입력해 주세요 없다면 enter를 눌러주세요")
                rate, content, recommend = input_review_info(allow_empty = True)
                success = review_manager.do_personal_review_update(review, rating=rate, content=content, recommend=recommend)
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
def member_info(member_manager):

    members = member_manager.do_retrieve()

    if not members:
        return

    # 회원 조회
    admin_keyword = input("\n회원 정보를 입력해주세요. (ID, 이름, 연락처, Email)\nEnter를 입력하면 전체 회원이 출력됩니다.\n입력: :").strip()

    right_members = []

    for member in members:
        if (
            admin_keyword in str(member.member_id)
            or admin_keyword in member.name
            or admin_keyword in member.phone
            or admin_keyword in member.email
        ):
            right_members.append(member)

    if not right_members:
        print("\n회원을 조회할 수 없습니다.")
        right_members = members

    for idx, member in enumerate(right_members):
        print("=" * 50)
        print(f"회원번호: {idx+1}")
        print(f"ID: {member.member_id}")
        print(f"이름: {member.name}")
        print(f"연락처: {member.phone}")
        print(f"Email: {member.email}")
        print(f"가입일: {member.reg_date}")
        print(f"권한: {member.role}")


    # 관리자 메뉴 출력
    print("="*50)
    print("1. 회원 정보 수정")
    print("2. 회원 삭제")
    print("0. 돌아가기")

    admin_menu = input_int("선택: ", 0, 2)

    if admin_menu == 0:
        return

    # 이름으로 검색 시 검색된 회원이 1명일 경우
    if len(right_members) == 1:
        selected_member = right_members[0]

    # 이름으로 검색 시 검색된 회원이 2명 이상일 경우
    else:
        print("동일한 검색 결과가 여러 명 존재합니다.")
        member_number = input_int("수정 또는 삭제할 회원 번호를 입력하세요.", 1, len(right_members))

        selected_member = right_members[member_number - 1]

    member_id = selected_member.member_id

    # 회원 정보 수정
    if admin_menu == 1:
        print("="*50)
        print("1. 이름 수정")
        print("2. 비밀번호 수정")
        print("3. 이메일 수정")
        print("4. 연락처 수정")
        print("0. 돌아가기")

        update_menu = input_int("선택: ", 0, 4)

        if update_menu == 0:
            return

        new_value = input("수정할 정보를 입력하세요: ").strip()

        if not new_value:
            print("수정할 정보를 입력해주세요.")
            return

        if update_menu == 1:
            member_manager.do_member_update(member_id, name=new_value)

        elif update_menu == 2:
            member_manager.do_member_update(member_id, password=new_value)

        elif update_menu == 3:
            member_manager.do_member_update(member_id, email=new_value)

        elif update_menu == 4:
            member_manager.do_member_update(member_id, phone=new_value)


    elif admin_menu == 2:
        print("="*50)
        print(f"삭제할 회원: {selected_member.name}")
        print(f"회원 ID: {member_id}")

        confirm = input("정말 삭제하시겠습니까? (y/n): ").strip().lower()

        if confirm == "y":
            admin_id = member_manager.member.member_id

            print(f"관리자 ID 확인: {admin_id}")
            print(f"관리자 권한 확인: {member_manager.member.role}")

            member_manager.do_member_delete(member_id)
        else:
            print("회원 삭제를 취소했습니다.")
    
# 영화 검색 선택할 경우
def find_movie(movie_manager, review_manager):

    movies = movie_manager.movies

    if not movies:
        print("\n등록된 영화가 없습니다.")
        return

    while True:
        keyword = input("\n검색할 영화 제목을 입력하세요.\n한 글자라도 영화 제목에 포함이 되면 해당 단어를 가진 영화의 목록이 출력됩니다.\nenter키만 누를 시 전체 영화 목록이 출력됩니다.\n\n 입력: ").strip()

        if keyword == "0":
            return
        
        # 영화 제목 검색 시 일부, 전체 출력 여부
        right_movies = [
            movie for movie in movies
            if keyword in movie.movie_name
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
            print(f"{idx+1}. {movie.movie_name}")

        print("="*50)
    
        # 상세 정보 조회
        choice = input_int(
            "상세 정보를 열람할 영화의 번호를 입력하세요. (0: 다시 검색): ",
            0,
            len(right_movies)
        )

        if choice == 0:
            continue

        selected_movie = right_movies[choice - 1]

        print("=" * 50)
        print(selected_movie.movie_name)
        print("=" * 50)
        print(f"장르: {selected_movie.movie_genre}")
        print(f"개봉일: {selected_movie.movie_release}")
        print(f"러닝타임: {selected_movie.movie_running_time}분")
        print(f"줄거리: {selected_movie.movie_intro}")

        print("="*50)

        avg_rating = review_manager.do_review_avg_rating(selected_movie.movie_id)

        if avg_rating is None:
            print("등록된 리뷰/평점이 없습니다.")
        else:
            print(f"평균 평점: {avg_rating:.1f} / 5.0")

        print("="*50)
        print("리뷰 TOP 3")

        top_reviews = review_manager.do_review_top3(selected_movie.movie_id)

        if not top_reviews:
            print("등록된 리뷰가 없습니다.")

        else:
            for idx, review in enumerate(top_reviews):
                print(f"{idx + 1}. {review.member_id} | {review.rating}점")
                print(f" {review.review}")
                print("="*50)
        
        print("\n")
        print("="*50)

        print("1. 추가 검색")
        print("0. 이전 메뉴로 돌아가기")

        choice = input_int("선택: ", 0, 1)

        if choice == 1:
            continue

        elif choice == 0:
            return
    
def main():
    # 시작 화면
    member_manager = MemberManager()
    movie_manager = MovieManager()
    review_manager = ReviewManager()
    
    while member_manager.member is None:
        start = show_start_menu()

        if start == 1: # 회원가입
            register(member_manager)
        elif start == 2: # 로그인
            login(member_manager)
    # 로그인 후
    menu = 0
    while(menu != 6):
        show_main_menu(member_manager)
        menu = input_int("선택: ", 1, 6)
        print("="*50)
        if menu == 1:
            find_movie(movie_manager, review_manager)

        elif menu == 2: # 영화 리뷰 조회
            view_review(movie_manager, review_manager)

        elif menu == 3:  # 리뷰 작성
            create_review(member_manager, movie_manager, review_manager)
        elif menu == 4: # 리뷰 수정
            update_review(member_manager, review_manager, movie_manager)
        elif menu == 5:
            if member_manager.member.role != "ADMIN":
                print("회원 조회는 관리자만 할 수 있습니다")
                continue

            member_info(member_manager)




if __name__ == "__main__":
    main()
