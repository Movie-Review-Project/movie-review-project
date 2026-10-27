import json
import os
from datetime import date, datetime

from models.review import Review

# 프로젝트 최상위 폴더 경로 (이 파일이 있는 managers 폴더의 상위 폴더)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 리뷰 저장 파일 경로 → 실행 위치와 상관없이 항상 data/reviews.json을 찾음
REVIEW_FILE = os.path.join(BASE_DIR, "data", "reviews.json")


# 리뷰 여러 개를 저장·조회·수정·삭제하는 "기능" 담당 (화면 출력 없음, 데이터만 반환)
class ReviewManager:
    # 매니저 생성 시 실행: 리뷰 저장소 준비 후 파일에서 불러옴
    def __init__(self):
        # 전체 리뷰 보관함 {review_id: Review 객체}
        self.reviews: dict[int, Review] = {}
        # 시작하자마자 reviews.json 내용을 불러옴
        self._load_reviews()

    # [내부용] reviews.json → self.reviews
    def _load_reviews(self) -> None:
        # 파일이 없으면 (첫 실행) 빈 상태로 시작
        if not os.path.exists(REVIEW_FILE):
            return
        # encoding="utf-8": Windows 기본 인코딩(cp949)으로 읽으면 한글 깨짐
        with open(REVIEW_FILE, "r", encoding="utf-8") as f:
            text = f.read()
        # 파일이 비어 있으면 빈 상태로 시작
        if text.strip() == "":
            return
        # 형식이 깨졌으면 여기서 에러 발생 → 조용히 넘어가면 나중에 저장하면서 기존 데이터를 덮어써 날릴 수 있음
        data_list = json.loads(text)
        # 딕셔너리 하나씩 Review 객체로 바꿔서 review_id를 키로 저장
        for data in data_list:
            review = Review.from_dict(data)
            self.reviews[review.review_id] = review

    # [내부용] self.reviews → reviews.json (성공 True / 실패 False)
    def _save_reviews(self) -> bool:
        try:
            with open(REVIEW_FILE, "w", encoding="utf-8") as f:
                json.dump(
                    [r.to_dict() for r in self.reviews.values()],  # 객체 → 딕셔너리 리스트
                    f,
                    ensure_ascii=False,  # 한글을 \uae30 같은 코드가 아니라 그대로 저장
                    indent=2,            # 사람이 읽기 좋게 줄바꿈·들여쓰기
                )
            return True
        except OSError:
            # data 폴더 없음, 권한 문제 등으로 저장 실패
            return False

    # [내부용] 특정 영화의 리뷰만 골라서 리스트로 반환 (평균·Top3·리뷰 조회에서 재사용)
    # 양쪽을 str로 바꿔서 비교 → 저장값·전달값이 int든 str든 매칭됨
    def _get_reviews_by_movie(self, movie_id: str) -> list[Review]:
        return [r for r in self.reviews.values() if str(r.movie_id) == str(movie_id)]

    # [내부용] 날짜 문자열 → "YYYY-MM-DD"로 통일 (형식이 틀리거나 None이면 None)
    # 예: "2026-1-5" → "2026-01-05", "2026-13-01" → None
    def _to_date_text(self, text: str | None) -> str | None:
        try:
            return datetime.strptime(text, "%Y-%m-%d").date().isoformat()
        except (TypeError, ValueError):
            return None

    # [내부용] 저장·수정 전 값 검사 (화면에서 1차 검사해도 데이터 보호용으로 한 번 더)
    def _is_valid(self, review: Review) -> bool:
        # 평점: 1.0 ~ 5.0
        if not (1.0 <= review.rating <= 5.0):
            return False
        # 리뷰 내용: 빈 값 불가
        if review.review.strip() == "":
            return False
        # 관람 날짜: 형식이 맞아야 하고, 미래 날짜 불가
        watch_text = self._to_date_text(review.watch_date)
        if watch_text is None:
            return False
        if watch_text > date.today().isoformat():
            return False
        return True

    # [리뷰 작성] 새 리뷰 저장 → 성공 True / 실패 False
    # review_id, reg_date는 여기서 자동으로 채움 (호출하는 쪽은 None으로 넘기면 됨)
    def do_review_save(self, review: Review) -> bool:
        if not self._is_valid(review):
            return False
        # movie_id는 항상 str로 저장 (int로 넘어와도 JSON에 섞이지 않게)
        review.movie_id = str(review.movie_id)
        # 관람 날짜를 YYYY-MM-DD로 통일
        review.watch_date = self._to_date_text(review.watch_date)
        # 새 ID = 기존 최대 ID + 1 (리뷰가 하나도 없으면 1)
        review.review_id = max(self.reviews.keys(), default=0) + 1
        # 작성 일자 = 오늘 (YYYY-MM-DD → 작성일 정렬이 문자열 비교로 정확히 동작)
        review.reg_date = date.today().isoformat()
        self.reviews[review.review_id] = review
        # 파일 저장 실패 시 방금 넣은 리뷰를 다시 빼서 메모리와 파일 상태를 맞춤
        if not self._save_reviews():
            del self.reviews[review.review_id]
            return False
        return True

    # [내 관람 기록] 특정 회원이 쓴 리뷰만, 작성일 최신순으로 반환
    def do_personal_review_retrieve(self, member_id: int) -> list[Review]:
        my_reviews = [r for r in self.reviews.values() if r.member_id == member_id]
        # 작성일 같으면 review_id 큰 것(나중에 쓴 것)이 앞
        return sorted(my_reviews, key=lambda r: (r.reg_date, r.review_id), reverse=True)

    # [리뷰 수정] review_id가 같은 기존 리뷰의 내용을 교체 → 성공 여부 반환
    # 수정 가능: recommend, rating, review, watch_date / 유지: member_id, movie_id, reg_date
    def do_personal_review_update(self, review: Review) -> bool:
        original = self.reviews.get(review.review_id)
        # 없는 리뷰
        if original is None:
            return False
        # 작성자 본인만 수정 가능
        if original.member_id != review.member_id:
            return False
        if not self._is_valid(review):
            return False
        # 저장 실패 대비 기존 값 보관
        backup = (original.recommend, original.rating, original.review, original.watch_date)
        original.recommend = review.recommend
        original.rating = review.rating
        original.review = review.review
        original.watch_date = self._to_date_text(review.watch_date)
        # 파일 저장 실패 시 원래 값으로 되돌림
        if not self._save_reviews():
            original.recommend, original.rating, original.review, original.watch_date = backup
            return False
        return True

    # [리뷰 삭제] review_id에 해당하는 리뷰 삭제 → 성공 여부 반환 (없는 ID면 False)
    # ※ member_id 인자가 없어 본인 확인 불가 → 호출하는 쪽이 "내 리뷰 목록"에서 고른 ID만 넘겨야 함
    def do_personal_review_delete(self, review_id: int) -> bool:
        # pop: 꺼내면서 삭제, 없으면 None
        removed = self.reviews.pop(review_id, None)
        if removed is None:
            return False
        # 파일 저장 실패 시 다시 넣어서 복구
        if not self._save_reviews():
            self.reviews[review_id] = removed
            return False
        return True

    # [리뷰 조회] 특정 영화 리뷰를 조건에 맞게 필터·정렬해서 반환
    # recommend: True=추천만 / False=비추천만 / None=전체
    # sort_by: "rating"(평점) / "reg_date"(작성일), order: "asc"(오름차순) / "desc"(내림차순)
    def do_review_retrieve(self, movie_id: str, recommend: bool | None, sort_by: str, order: str) -> list[Review]:
        # 잘못된 정렬 값이면 바로 에러 → 호출하는 쪽 코드 실수를 빨리 발견
        if sort_by not in ("rating", "reg_date"):
            raise ValueError(f"sort_by는 'rating' 또는 'reg_date'만 가능합니다: {sort_by}")
        if order not in ("asc", "desc"):
            raise ValueError(f"order는 'asc' 또는 'desc'만 가능합니다: {order}")
        # 1) 해당 영화 리뷰만
        movie_reviews = self._get_reviews_by_movie(movie_id)
        # 2) 추천 여부 필터 (None이면 건너뜀 → 전체)
        if recommend is not None:
            movie_reviews = [r for r in movie_reviews if r.recommend == recommend]
        # 3) desc면 내림차순
        reverse = order == "desc"
        # 4) 평점순: 평점 같으면 작성일로 한 번 더 정렬
        if sort_by == "rating":
            return sorted(movie_reviews, key=lambda r: (r.rating, r.reg_date), reverse=reverse)
        # 작성일순: 작성일 같으면 review_id(먼저 등록된 순)로 한 번 더 정렬
        return sorted(movie_reviews, key=lambda r: (r.reg_date, r.review_id), reverse=reverse)

    # [영화 상세] 특정 영화의 평균 평점 반환
    # 리뷰가 없으면 None (0으로 나누기 에러 방지)
    def do_review_avg_rating(self, movie_id: str) -> float | None:
        movie_reviews = self._get_reviews_by_movie(movie_id)
        # 리뷰 0개면 평균을 낼 수 없으니 None
        if len(movie_reviews) == 0:
            return None
        # 평점 합계 / 리뷰 개수
        total = sum(r.rating for r in movie_reviews)
        return total / len(movie_reviews)

    # [영화 상세] 특정 영화의 리뷰 Top3 반환
    # 기준: 평점 높은 순, 평점 같으면 최신 작성순 (팀 미정 → 가정)
    def do_review_top3(self, movie_id: str) -> list[Review]:
        movie_reviews = self._get_reviews_by_movie(movie_id)
        # (평점, 작성일) 묶음 기준 내림차순 → 평점이 같으면 작성일이 늦은 리뷰가 앞
        sorted_reviews = sorted(movie_reviews, key=lambda r: (r.rating, r.reg_date), reverse=True)
        # 앞에서 3개만 (3개 미만이면 있는 만큼만, 0개면 빈 리스트)
        return sorted_reviews[:3]
