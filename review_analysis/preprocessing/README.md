# 기생충 리뷰 데이터 분석 리포트 

---

## EDA: 

### 평점 분포

| 플랫폼 | 평균 평점 |
|--------|-----------|
| Naver | **8.17** |
| Letterboxd | **9.47** |
| RottenTomatoes | **8.70** |

<div align="center">
  <img src="https://github.com/user-attachments/assets/ca770c49-e25d-466a-a2db-36ce51062447" width="300"/>
  <img src="https://github.com/user-attachments/assets/be223f60-3aab-4ab4-8e36-8d92418a4ead" width="300"/>
  <img src="https://github.com/user-attachments/assets/ff517de3-da6d-40ad-ab0f-0cdaae532540" width="300"/>
</div>

Letterboxd는 평균 평점이 가장 높았고, Naver는 분포가 고르게 나타났다. RottenTomatoes는 감정 표현이 적극적으로 반영되어 전반적으로 평점이 높은 경향을 보였다.

---

### ✏️ 리뷰 길이 분포

| 플랫폼 | 평균 길이 (자 수 기준) |
|--------|----------------------|
| Naver | **27.11자** |
| Letterboxd | **442.14자** |
| RottenTomatoes | **171.41자** |

Letterboxd는 감상평 중심의 긴 리뷰가 많고, Naver는 짧은 감상 위주다. RottenTomatoes는 감정과 평가가 적절히 담긴 중간 길이의 리뷰가 많다.

---

### 주요 단어 (Top 20 Frequency)

<div align="center">
  <img src="https://github.com/user-attachments/assets/cf61ae72-f9cc-4296-b43b-f500ddf88a08" width="300"/>
  <img src="https://github.com/user-attachments/assets/efd4a2d2-d1ce-4676-921b-2b7a92b10d01" width="300"/>
  <img src="https://github.com/user-attachments/assets/f1e11e44-52ea-488b-a42b-64620e2f29a1" width="300"/>
</div>

Naver는 “재밌다”, “좋다”, “불편하다” 등 감정 중심 표현이 반복되고, Letterboxd는 “best”, “like”, “ever” 같은 강한 감정 표현이 자주 등장한다. RottenTomatoes는 “good”, “great”, “really”, “character” 등 감정과 서술적 단어가 다양하게 나타난다.

---

## 전처리 & Feature Engineering

- **결측치 처리**: 모든 `Null` 값 제거  
- **이상치 제거**: 리뷰 길이 기준 Z-score로 `Z < -2`인 데이터 제거  
- **텍스트 전처리**:
  - 특수문자 제거 → 알파벳/숫자/공백만 유지
  - 토큰화: `nltk.word_tokenize`
  - 불용어 제거: `nltk.stopwords`
  - 표제어 추출: `WordNetLemmatizer`
- **파생 변수 생성**:
  - `review_length`: 리뷰 길이
  - `review_z`: Z-score
  - `keywords`: TF-IDF 기반 주요 키워드 5개
- **TF-IDF 벡터화**:
  - `TfidfVectorizer(max_features=100)`
  - 각 리뷰를 100차원 벡터로 변환

---

## 비교 분석: 플랫폼 간 차이점

| 항목 | Naver | Letterboxd | RottenTomatoes |
|------|-------|-------------|----------------|
| 평균 평점 | 8.17 | **9.47** | 8.70 |
| 리뷰 길이 | 27.11자 | **442.14자** | 171.41자 |
| 감정 표현 단어 | 재밌다, 좋다, 불편하다 | best, like, ever | best, good, great, really, like |

RottenTomatoes는 감정 단어의 **다양성과 빈도**가 가장 풍부하며, 범위를 확장하면 `cinematography`, `brilliant`, `plot` 등 내용 기반 키워드도 다수 등장한다.  
리뷰 길이 기준으로는 Letterboxd가 서술 위주, Naver는 단문 감상 중심, RottenTomatoes는 균형형 스타일을 보였다.
