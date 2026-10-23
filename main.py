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
def view_review()->Movie, int: 
    print("영화를 선택해 주세요")
    movie_list = MovieManager.do_movie_retrieve()
    for idx, movie in enumerate(movie_list):
        print(f"{idx+1}. {movie.title}")
    movie_idx = int(input("영화번호:"))
    while movie_idx < 1 or movie_idx > len(movie_list):
        print("다시 선택해 주세요.")
        movie_idx = int(input("영화번호:"))
    
    print("정렬 방법을 선택해 주세요")
    print("1. 평점    2. 최신")
    sort = int(input("정렬 방법"))
    while sort != 1 and sort != 2:
        print("다시 선택해 주세요.")
        sort = int(input("정렬 방법"))

    return movie_list[movie_idx-1], sort # 영화 객체 반환 
        
        


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
            movie, sort = view_review()
            review_list = ReviewManager.do_review_retrieve(movie.movie_id, sort)
            for idx, review in enumerate(review_list):
                pass

        elif menu == 4:
            member_info()



if __name__ == "__main__":
    main()