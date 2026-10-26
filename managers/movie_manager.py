# movie_manager.py
from models.movie import Movie
import json
from pathlib import Path

class MovieManager:

    def __init__(self):

        json_path = Path(__file__).parent.parent/'data'/'movies.json'

        with open(json_path,"r",encoding="utf-8") as file:
            movie_data = json.load(file)

        self.movies = []

        for data in movie_data:
            movie = Movie(
                data["movie_id"],
                data["movie_name"],
                data["movie_genre"],
                data["movie_release"],
                data["movie_running_time"],
                data["movie_intro"]
            )
            self.movies.append(movie)


    def search_movie(self,movie_name:str) -> dict:
        """영화 제목으로 검색"""
        # 영화 딕셔너리 반환
        for film in self.movies:

            if movie_name == film.movie_title:
                return film

        return None

    def date_sort_movies(self):
        """개봉일 최신순 정렬"""
        self.movies.sort(key=lambda movie: movie["movie_release"], reverse=True)

    def genre_sort_movies(self):
        """장르순 정렬"""
        pass

    def do_add_movie(self):
        """영화 추가"""
        pass

    def do_delete_movie(self):
        """영화 삭제"""
        pass

    def do_modify_movie(self):
        """영화 정보 수정"""
        pass

