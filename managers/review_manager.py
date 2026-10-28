import json
import os
from datetime import date, datetime
from decimal import ROUND_HALF_UP, Decimal

from models.review import Review

# 프로젝트 최상위 폴더 경로 (이 파일이 있는 managers 폴더의 상위 폴더)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 리뷰 저장 파일 경로 → 실행 위치와 상관없이 항상 data/reviews.json을 찾음
REVIEW_FILE = os.path.join(BASE_DIR, "data", "reviews.json")


# 리뷰 여러 개를 저장·조회·수정·삭제하는 "기능" 담당 (화면 출력 없음, 데이터만 반환)
# 호출 형식은 팀 공용 main.py 기준
class ReviewManager:
    # 매니저 생성 시 실행: 리뷰 저장소 준비 후 파일에서 불러옴
    def __init__(self):
        # 전체 리뷰 보관함 {review_id: Review 객체}
        self.reviews: dict[int, Review] = {}
        # 지금까지 쓴 가장 큰 review_id (실행 중에 삭제된 번호가 다시 쓰이지 않게 기억)
        self._last_id = 0
        # 시작하자마자 reviews.json 내용을 불러옴
        self._load_reviews()

    # [내부용] reviews.json → self.reviews
    # 손으로 고친 데이터도 형식을 통일하고, 고칠 수 없는 데이터는 어디가 문제인지 알려주며 멈춤
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
        # JSON 문법이 깨졌으면 여기서 에러 → 조용히 넘어가면 다음 저장 때 기존 데이터를 덮어써 날릴 수 있음
        data_list = json.loads(text)
        if not isinstance(data_list, list):
            raise ValueError("reviews.json은 리뷰 목록([ ... ]) 형식이어야 합니다.")
        for index, data in enumerate(data_list, start=1):
            try:
                review = Review.from_dict(data)
            except (KeyError, TypeError) as e:
                raise ValueError(f"reviews.json {index}번째 항목에 필수 값이 없습니다: {e}") from None
            # review_id "1" → 1 (문자열이면 새 번호 계산 때 에러)
            try:
                review.review_id = int(review.review_id)
            except (TypeError, ValueError):
                raise ValueError(f"reviews.json {index}번째 항목의 review_id가 숫자가 아닙니다: {review.review_id!r}") from None
            # 평점 "4.5" → 4.5, 추천 "Y"/true → "y", 관람일 "" → None(입력 안 함) 으로 통일
            review.rating = self._to_rating(review.rating)
            review.recommend = self._to_yn(review.recommend)
            if self._is_blank(review.watch_date):
                review.watch_date = None
            if not self._is_valid(review):
                raise ValueError(
                    f"reviews.json {review.review_id}번 리뷰 값이 잘못됐습니다 "
                    "(평점 0~5, 내용, 추천 y/n, 회원·영화 ID, 관람일 확인)"
                )
            # 같은 번호가 두 번 있으면 하나가 조용히 사라지므로 멈춤
            if review.review_id in self.reviews:
                raise ValueError(f"reviews.json에 review_id {review.review_id}번이 중복돼 있습니다.")
            review.movie_id = str(review.movie_id)
            review.watch_date = self._to_date_text(review.watch_date) if review.watch_date is not None else None
            self.reviews[review.review_id] = review
        self._last_id = max(self.reviews.keys(), default=0)

    # [내부용] self.reviews → reviews.json (성공 True / 실패 False)
    # 1) 먼저 JSON 문자열로 변환 → 변환 중 오류가 나도 기존 파일은 그대로
    # 2) 임시 파일(.tmp)에 다 쓴 뒤 원본과 교체 → 쓰는 도중 꺼져도 원본 보존
    def _save_reviews(self) -> bool:
        temp_file = REVIEW_FILE + ".tmp"
        try:
            text = json.dumps(
                [r.to_dict() for r in self.reviews.values()],  # 객체 → 딕셔너리 리스트
                ensure_ascii=False,  # 한글을 코드 형태로 바꾸지 않고 그대로 저장
                indent=2,            # 사람이 읽기 좋게 줄바꿈·들여쓰기
            )
            with open(temp_file, "w", encoding="utf-8") as f:
                f.write(text)
            os.replace(temp_file, REVIEW_FILE)
            return True
        except (OSError, TypeError, ValueError):
            # OSError: data 폴더 없음·권한 문제 / TypeError·ValueError: JSON으로 바꿀 수 없는 값
            # 실패하면 남은 임시 파일 정리
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except OSError:
                pass
            return False

    # [내부용] 특정 영화의 리뷰만 골라서 리스트로 반환 (평균·Top3·리뷰 조회에서 재사용)
    # 양쪽을 str로 바꿔서 비교 → 저장값·전달값이 int든 str든 매칭됨
    def _get_reviews_by_movie(self, movie_id: str) -> list[Review]:
        return [r for r in self.reviews.values() if str(r.movie_id) == str(movie_id)]

    # [내부용] 값이 비었는지 (None, "", "   ")
    def _is_blank(self, value) -> bool:
        return value is None or str(value).strip() == ""

    # [내부용] 날짜 문자열 → "YYYY-MM-DD"로 통일 (형식이 틀리거나 None이면 None)
    # 예: "2026-1-5" → "2026-01-05", "2026-13-01" → None
    def _to_date_text(self, text: str | None) -> str | None:
        try:
            return datetime.strptime(text, "%Y-%m-%d").date().isoformat()
        except (TypeError, ValueError):
            return None

    # [내부용] 추천 여부 → 'y' / 'n'으로 통일 (알 수 없는 값이면 None)
    # 'y', 'Y', True → 'y' / 'n', 'N', False → 'n'
    def _to_yn(self, value) -> str | None:
        if value is True or (isinstance(value, str) and value.strip().lower() == "y"):
            return "y"
        if value is False or (isinstance(value, str) and value.strip().lower() == "n"):
            return "n"
        return None

    # [내부용] 평점 → 실수 변환 (input()으로 받은 "4.5" 같은 문자열 대비, 변환 불가면 None)
    # True/False는 숫자로 바뀌어 버리므로(True → 1.0) 평점으로 인정하지 않음
    def _to_rating(self, value) -> float | None:
        if isinstance(value, bool):
            return None
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    # [내부용] 저장·수정·불러오기 전 값 검사 (화면에서 1차 검사해도 데이터 보호용으로 한 번 더)
    def _is_valid(self, review: Review) -> bool:
        # 회원 ID·영화 ID: 비어 있으면 누구의 어떤 영화 리뷰인지 알 수 없음
        if self._is_blank(review.member_id) or self._is_blank(review.movie_id):
            return False
        # 평점: 숫자이고 0.0 ~ 5.0 (main.py 입력 범위 기준, NaN은 비교가 항상 False라 여기서 걸러짐)
        if isinstance(review.rating, bool) or not isinstance(review.rating, (int, float)):
            return False
        if not (0.0 <= review.rating <= 5.0):
            return False
        # 리뷰 내용: 문자열이고 빈 값 불가
        if not isinstance(review.review, str) or review.review.strip() == "":
            return False
        # 추천 여부: 'y' 또는 'n'만
        if review.recommend not in ("y", "n"):
            return False
        # 관람 날짜: 선택 항목 → 없으면 통과, 있으면 형식·미래 날짜 검사
        if review.watch_date is not None:
            watch_text = self._to_date_text(review.watch_date)
            if watch_text is None or watch_text > date.today().isoformat():
                return False
        return True

    # [리뷰 작성] 값을 받아 새 리뷰를 만들어 저장 → 성공 True / 실패 False
    # main.py 호출 형식: do_review_save(회원ID, 영화ID, 평점, 리뷰내용, 추천여부('y'/'n'))
    # watch_date(관람 날짜)는 선택. 안 넘기거나 빈 값이면 None으로 저장
    # review_id, reg_date는 여기서 자동 생성
    def do_review_save(
        self,
        member_id: int | str,
        movie_id: str,
        rating: float,
        review_text: str,
        recommend: str,
        watch_date: str | None = None,
    ) -> bool:
        rating = self._to_rating(rating)
        if rating is None:
            return False
        # 관람 날짜를 빈 값("")으로 넘기면 "입력 안 함"으로 처리
        if self._is_blank(watch_date):
            watch_date = None
        # 넘겨받은 값으로 Review 객체 생성 (ID·작성일은 아래에서 채움)
        new_review = Review(
            None,
            member_id,
            movie_id,
            self._to_yn(recommend),      # 'y'/'n'으로 통일
            rating,
            review_text,
            watch_date,
            None,
        )
        # 검사를 통과한 뒤에 형식 변환 (먼저 str()하면 None이 "None" 글자로 바뀌어 검사를 통과해 버림)
        if not self._is_valid(new_review):
            return False
        new_review.movie_id = str(movie_id).strip()      # movie_id는 항상 str로 저장
        if watch_date is not None:
            new_review.watch_date = self._to_date_text(watch_date)   # YYYY-MM-DD로 통일
        # 새 ID = 지금까지 쓴 가장 큰 번호 + 1 (실행 중 삭제된 번호는 다시 쓰지 않음)
        new_id = max(self._last_id, max(self.reviews.keys(), default=0)) + 1
        new_review.review_id = new_id
        # 작성 일자 = 오늘 (YYYY-MM-DD → 작성일 정렬이 문자열 비교로 정확히 동작)
        new_review.reg_date = date.today().isoformat()
        self.reviews[new_id] = new_review
        # 파일 저장 실패 시 방금 넣은 리뷰를 다시 빼서 메모리와 파일 상태를 맞춤
        if not self._save_reviews():
            del self.reviews[new_id]
            return False
        self._last_id = new_id
        return True

    # [내 관람 기록] 특정 회원이 쓴 리뷰만, 작성일 최신순으로 반환
    # 양쪽을 str로 바꿔서 비교 → 회원 ID가 int든 str든 매칭됨 (movie_id와 같은 방식)
    def do_personal_review_retrieve(self, member_id: int | str) -> list[Review]:
        my_reviews = [r for r in self.reviews.values() if str(r.member_id) == str(member_id)]
        # 작성일 같으면 review_id 큰 것(나중에 쓴 것)이 앞
        return sorted(my_reviews, key=lambda r: (r.reg_date, r.review_id), reverse=True)

    # [리뷰 수정] 기존 리뷰의 값을 바꿈 → 성공 여부 반환
    # main.py 호출 형식: do_personal_review_update(review, rating=, content=, recommend=)
    # None으로 넘긴 항목은 기존 값 유지 (main.py에서 Enter 입력 시 None)
    # review는 Review 객체 또는 review_id 둘 다 가능
    # ※ 회원 정보가 안 넘어와서 본인 확인 불가 → 화면에서 "내 리뷰 목록"의 리뷰만 넘겨야 함
    def do_personal_review_update(
        self,
        review: Review | int,
        rating: float | None = None,
        content: str | None = None,
        recommend: str | None = None,
        watch_date: str | None = None,
    ) -> bool:
        review_id = review.review_id if isinstance(review, Review) else review
        original = self.reviews.get(review_id)
        # 없는 리뷰
        if original is None:
            return False
        # None이면 기존 값, 아니면 새 값 (평점은 숫자 변환)
        new_rating = original.rating
        if rating is not None:
            new_rating = self._to_rating(rating)
            if new_rating is None:
                return False
        new_content = original.review if content is None else content
        new_recommend = original.recommend if recommend is None else self._to_yn(recommend)
        # 관람 날짜는 None·빈 값이면 기존 값 유지
        new_watch = original.watch_date if self._is_blank(watch_date) else watch_date
        # 바뀔 값으로 임시 객체를 만들어 검사 (검사 통과 전엔 원본 안 건드림)
        candidate = Review(
            original.review_id,
            original.member_id,
            original.movie_id,
            new_recommend,
            new_rating,
            new_content,
            new_watch,
            original.reg_date,
        )
        if not self._is_valid(candidate):
            return False
        # 저장 실패 대비 기존 값 보관
        backup = (original.recommend, original.rating, original.review, original.watch_date)
        original.recommend = new_recommend
        original.rating = new_rating
        original.review = new_content
        original.watch_date = self._to_date_text(new_watch) if new_watch is not None else None
        # 파일 저장 실패 시 원래 값으로 되돌림
        if not self._save_reviews():
            original.recommend, original.rating, original.review, original.watch_date = backup
            return False
        return True

    # [리뷰 삭제] 리뷰 삭제 → 성공 여부 반환 (없는 리뷰면 False)
    # main.py 호출 형식: do_personal_review_delete(review)
    # review는 Review 객체 또는 review_id 둘 다 가능
    # ※ 본인 확인 불가 → 화면에서 "내 리뷰 목록"의 리뷰만 넘겨야 함
    def do_personal_review_delete(self, review: Review | int) -> bool:
        review_id = review.review_id if isinstance(review, Review) else review
        # pop: 꺼내면서 삭제, 없으면 None
        removed = self.reviews.pop(review_id, None)
        if removed is None:
            return False
        # 파일 저장 실패 시 다시 넣어서 복구
        if not self._save_reviews():
            self.reviews[review_id] = removed
            return False
        return True

    # [리뷰 조회] 특정 영화 리뷰를 정렬해서 반환
    # main.py 호출 형식: do_review_retrieve(movie_id, sort)
    # sort: 1=최신순(작성일), 2=평점순 / "1", "2", "reg_date", "rating" 문자열도 허용
    # recommend(선택): 'y'=추천만 / 'n'=비추천만 / None=전체(기본)
    # order(선택): "desc"=내림차순(기본) / "asc"=오름차순
    def do_review_retrieve(
        self,
        movie_id: str,
        sort: int | str = 1,
        recommend: str | None = None,
        order: str = "desc",
    ) -> list[Review]:
        # 화면 번호(1, 2)와 문자열 둘 다 정렬 기준으로 변환
        sort_map = {
            1: "reg_date", 2: "rating",
            "1": "reg_date", "2": "rating",
            "reg_date": "reg_date", "rating": "rating",
        }
        # 잘못된 값이면 바로 에러 → 호출하는 쪽 코드 실수를 빨리 발견
        # (True는 1과 같은 값으로 취급돼 최신순으로 새어 들어가므로 따로 막음)
        if isinstance(sort, bool) or sort not in sort_map:
            raise ValueError(f"sort는 1(최신순), 2(평점순)만 가능합니다: {sort}")
        if order not in ("asc", "desc"):
            raise ValueError(f"order는 'asc' 또는 'desc'만 가능합니다: {order}")
        sort_by = sort_map[sort]
        # 1) 해당 영화 리뷰만
        movie_reviews = self._get_reviews_by_movie(movie_id)
        # 2) 추천 여부 필터 (None이면 건너뜀 → 전체, True/False로 넘겨도 'y'/'n'으로 변환)
        if recommend is not None:
            target = self._to_yn(recommend)
            # 'x' 같은 값이면 조용히 빈 목록을 주지 않고 에러 → 호출 실수를 빨리 발견
            if target is None:
                raise ValueError(f"recommend는 'y' 또는 'n'만 가능합니다: {recommend}")
            movie_reviews = [r for r in movie_reviews if r.recommend == target]
        # 3) desc면 내림차순
        reverse = order == "desc"
        # 4) 평점순: 평점 같으면 작성일로 한 번 더 정렬
        if sort_by == "rating":
            return sorted(movie_reviews, key=lambda r: (r.rating, r.reg_date), reverse=reverse)
        # 최신순: 작성일 같으면 review_id(나중에 등록된 것)로 한 번 더 정렬
        return sorted(movie_reviews, key=lambda r: (r.reg_date, r.review_id), reverse=reverse)

    # [영화 상세] 특정 영화의 평균 평점 반환 (소수점 1자리, 사사오입)
    # 리뷰가 없으면 None (0으로 나누기 에러 방지)
    def do_review_avg_rating(self, movie_id: str) -> float | None:
        movie_reviews = self._get_reviews_by_movie(movie_id)
        # 리뷰 0개면 평균을 낼 수 없으니 None
        if len(movie_reviews) == 0:
            return None
        # 평점 합계 / 리뷰 개수 → 소수점 1자리에서 반올림 (3.25 → 3.3)
        # 파이썬 round()는 3.25를 3.2로 만들어서(짝수 쪽으로 반올림) Decimal 사용
        total = Decimal(str(sum(r.rating for r in movie_reviews)))
        average = total / Decimal(len(movie_reviews))
        return float(average.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))

    # [영화 상세] 특정 영화의 리뷰 Top3 반환
    # 기준: 평점 높은 순, 평점 같으면 최신 작성순 (팀 미정 → 가정)
    def do_review_top3(self, movie_id: str) -> list[Review]:
        movie_reviews = self._get_reviews_by_movie(movie_id)
        # (평점, 작성일) 묶음 기준 내림차순 → 평점이 같으면 작성일이 늦은 리뷰가 앞
        sorted_reviews = sorted(movie_reviews, key=lambda r: (r.rating, r.reg_date), reverse=True)
        # 앞에서 3개만 (3개 미만이면 있는 만큼만, 0개면 빈 리스트)
        return sorted_reviews[:3]
