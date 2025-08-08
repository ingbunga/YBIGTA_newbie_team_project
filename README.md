# 👥 5조 팀 소개

## 🧑‍💼 팀원 소개

### 👨‍💻 엄준서  
팀에서 가장 연식이 오래된 인간이며, 현재 팀장을 맡고 있습니다~


### 🧙 강성우
SICP 라는 책에서는 프로그래머를 마법사로 비유합니다. 컴퓨터의 영혼을 불러내는 존재라는 비유이죠. \
우리는 AI를 다루고 있지만, 비유는 여전히 유효합니다. 완전 멋있지 않나요? 그래서 저는 마법사가 되고 싶습니다. \
마법사가 되고 싶은 강성우라고 합니다.

### 👨‍🎓 한원석
저는 산업공학과 21학번 한원석입니다. 유능한 저희 조 다른 팀원들을 따라가기 위해 열심히 노력하고 있습니다.

# 크롤링 데이터 설명
[크롤링 데이터 readme 파일](docs/crawling.readme.md)

# EDA&FE, 시각화
[EDA & FE, 시각화 readme 파일](docs/analysis.readme.md)

# 코드 실행 방법
[코드 실행 방법 readme 파일](docs/git.readme.md)

# 프로젝트를 진행하며 깨달은 점, 마주쳤던 오류를 해결한 경험
[깨달은 점, 오류를 해결한 경험](docs/lessons_learned.md)

# AWS, DB 과제
[AWS, DB 과제](docs/aws_db.md)

---

## 🔒 GitHub 협업 흐름

![branch_protection](/github/branch_protection.png)

![push_rejected](/github/push_rejected.png)

![review_and_merged](/github/review_and_merged.png)


---

## 📦 RAG Agent 데모 (Streamlit + LangGraph)

로컬 실행 전 의존성 설치:

```bash
pip install -r requirements.txt
```

환경변수 설정(예: OpenAI):

```bash
# PowerShell
$Env:OPENAI_API_KEY = "YOUR_KEY"
```

앱 실행:

```bash
streamlit run streamlit_app.py
```

구성 요약:
- `st_app/graph/router.py`: LangGraph 라우팅. 파일 내부 LLM 분류로 `chat | subject_info | rag_review` 분기, 처리 후 `chat`으로 복귀.
- `st_app/graph/nodes/*`: 각 노드 구현
- `st_app/rag/*`: 임베딩/리트리버/프롬프트/LLM 래퍼
- `st_app/db/subject_information/subjects.json`: 대상 기본 정보
- `st_app/db/faiss_index/`: 첫 실행 시 자동 생성(`index.faiss`, `meta.json`)

배포 시 비밀키는 Cloud Secrets에 저장하세요. 배포 후 README에 링크와 스크린샷을 추가하면 채점 기준 1-3을 충족합니다.