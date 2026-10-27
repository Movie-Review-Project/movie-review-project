from managers.member_manager import MemberManager
from managers.movie_manager import MovieManager
from managers.review_manager import ReviewManager

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
    print("1. 회원가입   2. 로그인")
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
        print(f"{idx+1}. {movie.movie_name}")

# 리뷰 출력
def show_review(review_manager, movie, sort):
    reviews = review_manager.do_review_retrieve(movie.movie_id, sort)
    print("="*50)
    print(f"리뷰 목록 - {movie.movie_name}")
    print("="*50)
    print(f"평균평점 : {review_manager.do_review_avg_rating(movie.movie_id)} / 5.0 (리뷰 {len(reviews)}개)")
    print("-"*50)
    for idx, review in enumerate(reviews):
        print(f"{idx+1}. {review.member_id} | {review.rating}점 | {'추천' if review.recommand == 'y' else '비추천'}")
        print(f"   {review.review}")


# 회원 가입 선택 시
def register():
    pass

# 로그인 선택 시
def login() -> bool: 
    pass

# 로그인 후
def show_main_menu(user):
    print("1. 영화검색")
    print("2. 영화 리뷰조회")
    print("3. 리뷰작성")
    print("4. 내 리뷰 조회 및 수정")
    print("5. 회원조회")
    print("6. 종료")

# 2. 리뷰 조회
def view_review(movie_manager, review_manager): 
    print("영화를 선택해 주세요")
    print("="*50)
    show_movie_list(movie_manager)
    movie_idx = input_int("영화번호: ", 1, len(movie_manager.movies))-1 

    movie = movie_manager.movies[movie_idx]
    
    print("리뷰 정렬 방법을 선택해 주세요")
    print("1. 최신    2. 평점")
    sort = input_int("정렬방법: ", 1, 2)
    show_review(review_manager, movie, sort)

# 3. 리뷰 작성
def create_review(member_manager, movie_manager, review_manager):
    is_exit = False
    while not is_exit:
        print("영화를 선택해 주세요")
        print("="*50)
        show_movie_list(movie_manager)
        movie_idx = input_int("영화번호: ", 1, len(movie_manager.movies))-1 
        movie = movie_manager.movies[movie_idx]
        print("="*50)
        print("리뷰 작성 -", movie.movie_name)
        
        while True:
            rate, content, recommand = input_review_info()
            success = review_manager.do_review_save(member_manager.member.member_id, movie.movie_id, rate, content, recommand)
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
def update_review(member_manager, review_manager, movie_manager):
    while True:
        reviews = review_manager.do_personal_review_retrieve(member_manager.member.member_id)
        for idx, review in enumerate(reviews):
            print(f"{idx+1}. {movie_manager.id_to_title(review.movie_id)} | {review.rating} | 관람 {review.reg_date} | {"추천" if review.recommand == 'y' else "비추천"}")
            print(review.review)
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

# 영화 검색 선택할 경우
def find_movie():
    pass

def main():
    # 시작 화면
    member_manager = MemberManager()
    movie_manager = MovieManager()
    review_manager = ReviewManager()
    
    while member_manager.member is None:
        start = show_start_menu()

        if start == 1: # 회원가입
            register()
        elif start == 2: # 로그인
            login()
    # 로그인 후
    menu = 0
    while(menu != 6):
        show_main_menu(member_manager)
        menu = input_int("선택: ", 1, 6)
        if menu == 1:
            # find_movie()
            pass
        elif menu == 2: # 영화 리뷰 조회
            view_review(movie_manager, review_manager)
        elif menu == 3: # 리뷰 작성
            create_review(member_manager, movie_manager, review_manager)
        elif menu == 4: # 리뷰 수정
            update_review(member_manager, review_manager, movie_manager)
        elif menu == 5:
            if member_manager.member.role != "admin":
                print("회원 조회는 관리자만 할 수 있습니다")
                continue

            member_info()



if __name__ == "__main__":
    main()
