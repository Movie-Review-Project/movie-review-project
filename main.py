
# 시작 화면
def show_start_menu():
    print("="*50)
    print("(영화 리뷰 & 관람 기록 관리 시스템)")
    print("="*50)
    print("1. 로그인")
    print("2. 회원가입")
    print("="*50)
    start = int(input("선택:"))
    print("")
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

    menu = int(input())
    return menu

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
    menu = show_main_menu()

    if menu == 1:
        find_movie()
    elif menu == 4:
        member_info()



if __name__ == "__main__":
    main()