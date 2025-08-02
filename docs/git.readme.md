## Git

### 코드 실행 방법

#### 가상환경 설정
cmd 루트 디렉토리에서 다음과 같은 명령을 입력해주세요.
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

#### Web
루트 디렉토리에서 다음과 같은 명령을 입력해주세요.
```bash
uvicorn app.main:app --reload
```

또한 다음과 같은 명령어로 도커로 실행할 수도 있습니다.
```bash
# 이미지 빌드
docker build -f Dockerfile -t newbie-project .

# 컨테이너 실행
docker run -p 8000:8000 --env-file .env newbie-project
```

인터넷 주소창에 다음과 같은 주소를 입력해주세요.
```html
http://localhost:8000/static/index.html
```

#### crawling
루트 디렉토리에서 다음과 같은 명령을 입력해주세요.
```bash
python -m review_analysis.crawling.main -o database -a
```

#### preprocessing
> preprocessing 은 konlpy를 사용합니다.
> 먼저 [konlpy 문서](https://konlpy.org/en/latest/install/)에 따라 konlpy를 설치해주세요. 

루트 디렉토리에서 다음과 같은 명령을 입력해주세요.
```bash
python -m review_analysis.preprocessing.main -o database -a
```

만일 오류가 발생한다면 도커로 실행할 수도 있습니다. (단, -a 만 가능합니다.)
```bash
# 이미지 빌드
docker build -f Dockerfile.preprocessing -t preprocessing-app .

# 컨테이너 실행 (볼륨 마운트)
docker run -v {원하는 출력 경로 (절대경로로)}:/output preprocessing-app
```