# movie.py

class Movie:

    def __init__(self,
                movie_id:str,
                movie_name:str,
                movie_genre:str,
                movie_release:str,
                movie_running_time:str,
                movie_intro:str
                ):
        
        self.__movie_id = movie_id
        self.__movie_name = movie_name
        self.__movie_genre = movie_genre
        self.__movie_release = movie_release
        self.__movie_running_time = movie_running_time
        self.__movie_intro = movie_intro

    @property
    def movie_id(self) -> str:
        """영화 ID 읽기 전용"""
        return self.__movie_id
    
    @property
    def movie_name(self) -> str:
        """영화 제목 읽기 전용"""
        return self.__movie_name

    @property
    def movie_genre(self) -> str:
        """영화 장르 읽기 전용"""
        return self.__movie_genre

    @property
    def movie_release(self) -> str:
        """영화 출시 일자 읽기 전용"""
        return self.__movie_release

    @property
    def movie_running_time(self) -> str:
        """영화 러닝 타임 읽기 전용"""
        return self.__movie_running_time

    @property
    def movie_intro(self) -> str:
        """영화 줄거리 읽기 전용"""
        return self.__movie_intro

    # setter
    @movie_id.setter
    def movie_id(self,value:str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("영화 ID는 필수 문자열입니다.")
        self.__movie_id = value

    @movie_name.setter
    def movie_name(self,value:str) -> None:
        if not isinstance(value,str) or not value.strip():
            raise ValueError("영화 제목은 필수 문자열입니다.")
        self.__movie_name = value

    @movie_genre.setter
    def movie_genre(self,value:str) -> None:
        if not isinstance(value,str) or value not in ["모험","공포","액션","코미디","드라마","가족","로맨스","범죄"]:
            raise ValueError("영화 장르는 모험,공포,액션,코미디,드라마,가족,로맨스,범죄 중 하나여야 합니다.")
        self.__movie_genre = value

    @movie_release.setter
    def movie_release(self,value:str) -> None:
        if not isinstance(value,str) or not value.strip():
            raise ValueError("영화 출시일은 필수 문자열입니다.")
        self.__movie_release = value

    @movie_running_time.setter
    def movie_running_time(self,value:str) -> None:
        if not isinstance(value,str) or not value.strip():
            raise ValueError("영화 러닝타임은 필수 문자열입니다.")
        self.__movie_running_time = value

    @movie_intro.setter
    def movie_intro(self,value:str) -> None:
        if not isinstance(value,str) or not value.strip():
            raise ValueError("영화 러닝타임은 필수 문자열입니다.")
        self.__movie_intro = value