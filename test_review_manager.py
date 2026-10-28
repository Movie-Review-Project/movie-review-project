# 리뷰 매니저 기능 확인용 테스트 파일 (최종 프로그램에는 포함 안 됨)
from managers.review_manager import ReviewManager

# 매니저 생성 → 이때 data/reviews.json을 자동으로 불러옴
m = ReviewManager()


# 리뷰 객체 리스트 → review_id만 뽑아서 보기 쉽게
def ids(reviews):
    return [r.review_id for r in reviews]


# 1) 불러오기 확인
print("=== 불러오기 ===")
print("리뷰 개수:", len(m.reviews))
print("1번 리뷰:", m.reviews[1].to_dict())

# 2) 평균 평점 확인
print("=== 평균 평점 ===")
print("영화1:", m.do_review_avg_rating(1))
print("영화3(리뷰 없음):", m.do_review_avg_rating(3))

# 3) Top3 확인
print("=== Top3 ===")
print("영화1:", ids(m.do_review_top3(1)))
print("영화2:", ids(m.do_review_top3(2)))

# 4) 리뷰 조회 (필터·정렬) 확인
print("=== 리뷰 조회 ===")
print("영화1 전체 / 평점 내림차순:", ids(m.do_review_retrieve(1, None, "rating", "desc")))
print("영화1 추천만 / 평점 오름차순:", ids(m.do_review_retrieve(1, True, "rating", "asc")))
print("영화1 비추천만 / 작성일 내림차순:", ids(m.do_review_retrieve(1, False, "reg_date", "desc")))
print("영화1 전체 / 작성일 내림차순:", ids(m.do_review_retrieve(1, None, "reg_date", "desc")))
print("리뷰 없는 영화3:", ids(m.do_review_retrieve(3, None, "rating", "desc")))

# 5) 잘못된 값이 들어오면 에러가 나는지 확인
try:
    m.do_review_retrieve(1, None, "title", "desc")
except ValueError as e:
    print("잘못된 sort_by:", e)