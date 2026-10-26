# movie_manager.py
from models.movie import Movie
import json
import os
from pathlib import Path

class MovieManager:

    def __init__(self,file_path:str|Path|None = None)->None:
        # 기본저장경로
        if file_path is None:
            file_path = (
                Path(__file__).resolve().parent.parent
                /'data'
                /'movies.json'
            )
        # 파일 경로
        self.file_path = file_path
        # 영화 목록
        self.movies : list[Movie] = []
        # 영화 목록 로드
        self.load_json()

    def load_json(self)->None:
        """JSON 파일에서 회원정보를 읽어옵니다."""
        if not self.file_path.exists():
            self.movies = []
            return

        with self.file_path.open("r",encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data,list):
            raise ValueError("회원 JSON 데이터는 리스트여야 합니다.")

        # JSON 딕셔너리를 Movie 객체로 변환
        self.movies = [
            Movie.from_dict(item) for item in data
        ]

    def save_json(self) -> None:
        """JSON 파일로 저장"""

        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        # Movie 객체를 딕셔너리로 변환
        data = [
            movie.to_dict()
            for movie in self.movies 
        ]

        with self.file_path.open("w",encoding="utf-8") as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4
            )

    def search_movie(self,movie_name:str) -> dict|None:
        """영화 제목으로 검색"""
        for film in self.movies:

            if movie_name == film.movie_name:
                return film

        return None

    def date_sort_movies(self) -> list[dict,dict]:
        """개봉일 최신순 정렬"""
        self.movies.sort(key=lambda movie: movie["movie_release"], reverse=True)
        return self.movies

    def do_add_movie(self,movie:Movie) -> int:
        """영화 추가"""
        # 기존 영화 중복 방지
        for film in self.movies:
            if film.movie_id == movie.movie_id:
                print("기존 영화가 존재합니다.")
                return 0

        self.movies.append(movie)

        try:
            self.save_json()
        except Exception:
            self.movies.remove(movie)

        return 1

    def do_delete_movie(self,movie_name:str) -> bool:
        """영화 이름으로 영화 삭제"""
        movie = self.search_movie(movie_name)

        if movie is None:
            return False

        self.movies.remove(movie)
        self.save_json()

        return True

    def do_update_movie(self,mod_movie:str) -> int:
        """영화 정보 수정"""
        exist_movie = self.search_movie(mod_movie.movie_name)

        if exist_movie is None:
            return 0

        exist_movie.movie_genre = mod_movie.movie_genre
        exist_movie.movie_intro = mod_movie.movie_intro

        return 1