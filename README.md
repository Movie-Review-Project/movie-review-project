시네로그 (CineLog)
영화 리뷰 및 개인 관람 기록 관리 시스템
Python 기반 콘솔 프로그램으로 영화 정보를 검색하고, 리뷰와 평점 및 개인 관람 기록을 관리하는 프로젝트입니다.

프로젝트 소개
다양한 극장·OTT 플랫폼에서 관람한 영화의 기록을 한곳에 모아 관리할 수 있도록 기획했습니다. 사용자는 영화 정보를 검색하고, 관람한 작품의 리뷰와 평점을 남기거나 다른 사용자의 평가를 확인할 수 있습니다.
- 프로젝트명: 시네로그
- 팀: 리뷰는 못참지 (3조)
- 개발 기간: 2026.10.19 ~ 2026.10.30
- 팀원: 박민준(조장), 김범수, 김영범, 김준범, 황유나
주요 기능 (기획 기준)
구분	기능
회원 관리	회원가입, 로그인, 회원 정보 조회 및 관리
영화 정보 조회	TMDB API를 활용한 제목·줄거리·장르·개봉일 조회
영화 검색 및 정렬	제목·장르별 검색, 평점순·개봉일순 정렬
리뷰 및 평점 관리	리뷰 작성·조회·수정·삭제, 다른 사용자의 리뷰 조회
리뷰 검색 및 정렬	영화별 리뷰 조회, 평점 및 추천/비추천 기준 정렬
관람 기록	개인이 관람한 영화와 관람 날짜 조회
데이터 저장	JSON 파일을 활용한 회원·영화·리뷰 데이터 저장 및 불러오기


위 내용은 기획 기능 목록이며, 개별 기능의 구현 완료 여부를 의미하지 않습니다.

기술 스택
- Language: Python
- Interface: CLI (콘솔 기반)
- External API: TMDB API
- Data Storage: JSON
- Version Control: Git, GitHub
프로젝트 구조
project/
├── main.py                      # 프로그램 실행 및 메뉴 관리
├── models/                      # 데이터 모델 정의
│   ├── member.py                # Member 클래스
│   ├── movie.py                 # Movie 클래스
│   └── review.py                # Review 클래스
├── managers/                    # 데이터 및 기능 관리
│   ├── member_manager.py        # 회원가입, 로그인, 회원 관리
│   ├── movie_manager.py         # 영화 검색, 영화 관리
│   └── review_manager.py        # 리뷰 작성, 수정, 삭제 등
├── data/                        # JSON 데이터 파일
│   ├── members.json             # 회원 데이터
│   ├── movies.json              # 영화 데이터
│   └── reviews.json             # 리뷰 데이터
└── .gitignore                   # Git 추적 제외 설정
디렉터리별 역할
- models/: Member, Movie, Review 등 개별 객체의 속성과 데이터 변환 로직 정의
- managers/: JSON 데이터 로드·저장 및 회원·영화·리뷰 관련 기능 처리
- data/: JSON 형식의 영속 데이터 저장
- main.py: Manager 객체 생성, 사용자 메뉴 및 실행 흐름 관리
실행 방법
1. 저장소를 클론합니다.
   git clone https://github.com/Movie-Review-Project/movie-review-project.git
   cd movie-review-project
2. Python이 설치되어 있는지 확인합니다.
   python --version
3. 프로젝트 실행에 필요한 외부 라이브러리 및 TMDB API 인증 설정을 완료합니다. (구체적인 의존성 및 설정 방법은 구현 내용에 맞춰 업데이트 예정)
4. 프로그램을 실행합니다.
   python main.py
   운영체제에 따라 python3 main.py를 사용해야 할 수 있습니다.
프로그램 이용 흐름
프로그램 시작
├── 회원가입
├── 로그인
│   └── 사용자 메뉴
│       ├── 영화 검색
│       ├── 리뷰 조회
│       ├── 리뷰 작성
│       └── 회원 정보 조회
└── 관리자 기능
영화 검색 시 TMDB API로 영화 정보를 조회하고, 사용자가 선택한 영화의 리뷰를 작성하거나 조회하도록 설계했습니다.
협업 방식
- 기능별 브랜치에서 작업한 뒤 GitHub에 Push합니다.
- Pull Request를 통해 변경 내용을 검토하고 main 브랜치에 병합합니다.
- 공통으로 사용하는 모델·Manager의 인터페이스가 변경되면 팀원들과 공유합니다.
개발 목표
- 필수 CRUD 기능 구현
- Python 클래스·모듈을 활용한 기능별 구조화
- JSON 데이터 저장·불러오기
- GitHub를 통한 협업 및 개발 이력 관리
시네로그 — 영화의 순간을 기록하고, 감상을 나누는 공간
