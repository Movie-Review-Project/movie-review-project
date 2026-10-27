# 리뷰 틀
class Review:
    def __init__(
            self,
            review_id: int,
            member_id: int,
            movie_id: str,
            recommend: bool,
            rating: float,
            review: str,
            watch_date: str,
            reg_date: str,
    ):
        self.review_id = review_id
        self.member_id = member_id
        self.movie_id = movie_id
        self.recommend = recommend
        self.rating = rating
        self.review = review
        self.watch_date = watch_date
        self.reg_date = reg_date

    # 리뷰 1개를 화면 형식으로 출력
    # index: 목록에서 몇 번째인지 (화면 번호), movie_name: 영화 제목 (MovieManager에서 조회해서 넘김)
    def show_info(self, index: int, movie_name: str) -> None:
        # 평점 표시: 5.0 → "5", 4.5 → "4.5" (불필요한 .0 제거)
        rating_text = f"{self.rating:g}"
        # 관람 날짜가 없는 예전 데이터 대비
        watch_text = self.watch_date if self.watch_date else "-"
        # True → "추천", False → "비추천"
        recommend_text = "추천" if self.recommend else "비추천"

        print(f"{index}. {movie_name} | {rating_text}점 | 관람 {watch_text}")
        print(f"   {recommend_text}")
        print(f"   {self.review}")

    def to_dict(self) -> dict:
        return {
            "review_id": self.review_id,
            "member_id": self.member_id,
            "movie_id": self.movie_id,
            "recommend": self.recommend,
            "rating": self.rating,
            "review": self.review,
            "watch_date": self.watch_date,
            "reg_date": self.reg_date
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Review":
        return cls(
            data["review_id"],
            data["member_id"],
            data["movie_id"],
            data["recommend"],
            data["rating"],
            data["review"],
            data.get("watch_date"),  # 예전 데이터에 없어도 에러 없이 None
            data["reg_date"]
        )