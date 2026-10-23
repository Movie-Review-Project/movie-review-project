import MovieManager, MemberManager, ReviewManager

# 시작 화면
def show_start_menu():
    print("="*50)
    print("(영화 리뷰 & 관람 기록 관리 시스템)")
    print("="*50)
    print("1. 회원가입")
    print("2. 로그인")
    print("="*50)
    start = int(input("선택:"))
    print()
    return start

# 영화 목록 출력
def show_movie_list(movie_list):
    print("="*50)
    print("영화 목록")
    print("="*50)
    for idx, movie in enumerate(movie_list):
        print(f"{idx+1}. {movie.title}")

# 리뷰 출력
def show_review(review_list, title):
    print("="*50)
    print(f"리뷰 목록 - {title}")
    print("="*50)
    print(f"평균평점 : {ReviewManager.do_review_avg_rating(title)} / 5.0 (리뷰 {len(review_list)})")
    print("-"*50)
    for idx, review in enumerate(review_list):
        print(f"{idx+1}. {review.member_id} | {review.rating}점 | 추천 {""} | 비추천 {""}")
        print(f"    {review.review}")


# 회원 가입 선택 시
def register():
    pass

# 로그인 선택 시
def login() -> bool: 
    pass

# 로그인 후
def show_main_menu(user):
    print("1. 영화검색")
    print("2. 리뷰조회")
    print("3. 리뷰작성")
    if user.role == "admin":
        print("4.회원조회")
    print("5. 종료")
    menu = int(input())
    return menu

# 2. 리뷰 조회
def view_review(): 
    movie_list = MovieManager.do_movie_retrieve()
    print("영화를 선택해 주세요")
    show_movie_list(movie_list)
    movie_idx = int(input("영화번호: "))
    while movie_idx < 1 or movie_idx > len(movie_list):
        print("다시 선택해 주세요.")
        movie_idx = int(input("영화번호:"))

    movie = movie_list[movie_idx-1]
    
    print("리뷰 정렬 방법을 선택해 주세요")
    print("1. 최신    2. 평점")
    sort = int(input("정렬 방법"))
    while sort != 1 and sort != 2:
        print("다시 선택해 주세요.")
        sort = int(input("정렬 방법: "))
    reviews = ReviewManager.do_review_retrieve(movie.movie_id, sort)

    show_review(reviews, movie.movie_title)


# 4. 회원 조회 선택할 경우
def member_info():
    pass

# 영화 검색 선택할 경우
def find_movie():
    pass

def main():
    # 시작 화면
    is_login = False
    while is_login == False:
        start = show_start_menu()
        while start != 1 and start != 2:
            print("다시선택")
            start = show_start_menu()

        if start == 1: # 회원가입
            register()

        elif start == 2: # 로그인
            is_login = login()
    # 로그인 후
    menu = 0
    while(menu != 5):
        menu = show_main_menu()
        if menu == 1:
            find_movie()
        elif menu == 2: # 리뷰 조회
            view_review()
        elif menu == 3: # 리뷰 작성
            pass
        elif menu == 4:
            member_info()



if __name__ == "__main__":
    main()