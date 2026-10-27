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