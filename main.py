

def show_start_menu():
    print("="*50)
    print("(영화 리뷰 & 관람 기록 관리 시스템)")
    print("="*50)
    print("1. 로그인")
    print("2. 회원가입")
    print("3. 관리자")
    print("="*50)
    start = int(input("선택:"))
    print("")
    return start


def main():
    # 시작 화면
    start = show_start_menu()
    while start > 3 or start < 1:
        print("다시선택")
        start = show_start_menu()




if __name__ == "__main__":
    main()