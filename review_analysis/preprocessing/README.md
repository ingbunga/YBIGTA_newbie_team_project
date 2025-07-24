# 🎬 리뷰 데이터 분석 리포트 (EDA & 비교분석)

---

## 📊 \<EDA: 탐색적 데이터 분석>

### ⭐ 평점 분포

| 플랫폼            | 평균 평점    |
| -------------- | -------- |
| Naver          | **8.17** |
| Letterboxd     | **9.47** |
| RottenTomatoes | **8.70** |

<div align="center">
  <img src="https://github.com/user-attachments/assets/ca770c49-e25d-466a-a2db-36ce51062447" width="300"/>
  <img src="https://github.com/user-attachments/assets/be223f60-3aab-4ab4-8e36-8d92418a4ead" width="300"/>
  <img src="https://github.com/user-attachments/assets/ff517de3-da6d-40ad-ab0f-0cdaae532540" width="300"/>
</div>

* **Letterboxd**는 전반적으로 가장 높은 평점을 기록
* **Naver**는 중간 수준이지만 상대적으로 분포가 고르게 퍼져 있음
* **RottenTomatoes**는 감정 표현이 적극적인 경향으로 평점도 높게 형성됨

---

### ✏️ 리뷰 길이 분포

| 플랫폼            | 평균 길이 (자 수 기준) |
| -------------- | -------------- |
| Naver          | **27.11자**     |
| Letterboxd     | **442.14자**    |
| RottenTomatoes | **171.41자**    |

* **Letterboxd**는 감상평 중심으로 리뷰가 길고 서술적임
* **Naver**는 짧고 단답형 리뷰가 많아 정보 밀도는 낮은 편
* **RottenTomatoes**는 적당한 길이로 감정과 평가 모두 드러나는 스타일

---

### 📝 주요 단어 (Top 20 Frequency)

<div align="center">
  <img src="https://github.com/user-attachments/assets/cf61ae72-f9cc-4296-b43b-f500ddf88a08" width="300"/>
  <img src="https://github.com/user-attachments/assets/efd4a2d2-d1ce-4676-921b-2b7a92b10d01" width="300"/>
  <img src="https://github.com/user-attachments/assets/f1e11e44-52ea-488b-a42b-64620e2f29a1" width="300"/>
</div>

* Naver 리뷰는 **“재밌다”, “좋다”, “불편하다”** 등 감정 중심 단어가 반복
* Letterboxd는 **“best”, “like”, “ever”** 등 강한 표현이 많음
* RottenTomatoes는 **“good”, “great”, “really”, “character”** 등 다양한 감정 및 서술적 단어가 고르게 등장

---

## 🧹 <전처리 & Feature Engineering>

* **결측치 처리**: 모든 `Null` 값 제거
* **이상치 제거**: 리뷰 길이 기준 Z-score로 `Z < -2`인 데이터 제거
* **텍스트 전처리**

  * 특수문자 제거 → 알파벳/숫자/공백만 유지
  * 토큰화 → `nltk.word_tokenize`
  * 불용어 제거 → `nltk.stopwords`
  * 표제어 추출 → `WordNetLemmatizer`
* **파생 변수 생성**

  * `review_length`: 리뷰 길이
  * `review_z`: Z-score
  * `keywords`: TF-IDF 기반 주요 키워드 5개
* **TF-IDF 벡터화**

  * `TfidfVectorizer(max_features=100)`
  * 각 리뷰를 100차원 벡터로 변환

---

## 🔍 <비교 분석: 플랫폼 간 차이점>

| 항목       | Naver         | Letterboxd       | RottenTomatoes                  |
| -------- | ------------- | ---------------- | ------------------------------- |
| 평균 평점    | 8.17          | **9.47**         | 8.70                            |
| 리뷰 길이    | 27.11자        | **442.14자**      | 171.41자                         |
| 감정 표현 단어 | 재밌다, 좋다, 불편하다 | best, like, ever | best, good, great, really, like |

* **감정 단어 다양성**:
  RottenTomatoes가 가장 **풍부하고 다채로운 표현** 사용 → 분석 또는 모델링에서 정보 밀도 높음
* **글 길이**:
  Letterboxd는 **서술 중심**, Naver는 **짧은 감상 중심**, RottenTomatoes는 **균형적**

---

