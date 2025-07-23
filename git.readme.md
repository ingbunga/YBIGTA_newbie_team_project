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
루트 디렉토리에서 다음과 같은 명령을 입력해주세요.
```bash
python -m review_analysis.preprocessing.main -o database -a
```