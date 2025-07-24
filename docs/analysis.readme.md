# 기생충 리뷰 데이터 분석 리포트 

---

## EDA:

### 평점 분포

| 플랫폼        | 평균 평점 |
|---------------|-----------|
| Letterboxd    | **9.47**  |
| Naver         | **8.17**  |
| RottenTomatoes| **8.70**  |

<div align="center">
  <img src="https://github.com/user-attachments/assets/ca770c49-e25d-466a-a2db-36ce51062447" width="300"/>
  <img src="https://github.com/user-attachments/assets/be223f60-3aab-4ab4-8e36-8d92418a4ead" width="300"/>
  <img src="https://github.com/user-attachments/assets/ff517de3-da6d-40ad-ab0f-0cdaae532540" width="300"/>
</div>

Letterboxd는 가장 높은 평점을 보이며, 전반적으로 긍정적인 리뷰가 많았다.  
Naver는 비교적 평점이 고르게 분포되어 있었다.
RottenTomatoes는 감정 표현이 적극적으로 반영되어 높은 점수가 자주 등장했다.
이상치로는 Naver는 리뷰가 na 인 리뷰가 9개 있었다.
긴 리뷰는 있었지만, 오류등으로 길게 나온 리뷰가 아닌거로 판단해 이상치 처라하지 않았다.

---

### ✏리뷰 길이 분포

| 플랫폼         | 평균 길이 (자 수 기준) |
|----------------|------------------------|
| Letterboxd     | **442.14자**           |
| Naver          | **27.11자**            |
| RottenTomatoes | **171.41자**           |

Letterboxd는 감상 중심의 긴 서술형 리뷰가 많았다.  
Naver는 짧은 단문 리뷰가 대부분으로, 핵심적인 감정만 표현하는 경향이 있다.  
RottenTomatoes는 감정과 평가가 균형 있게 담긴 중간 길이의 리뷰가 많다.

---

### 주요 단어 (Top 20 Frequency)

<div align="center">
  <img src="https://github.com/user-attachments/assets/cf61ae72-f9cc-4296-b43b-f500ddf88a08" width="300"/>
  <img src="https://github.com/user-attachments/assets/f1e11e44-52ea-488b-a42b-64620e2f29a1" width="300"/>
  <img src="https://github.com/user-attachments/assets/efd4a2d2-d1ce-4676-921b-2b7a92b10d01" width="300"/>
</div>

Letterboxd는 “best”, “like”, “ever” 등 강한 감정 표현이 반복적으로 등장했다.  
Naver는 “재밌다”, “좋다”, “불편하다” 등 감정 중심 표현이 주요 키워드로 나타났다.  
RottenTomatoes는 “good”, “great”, “really”, “character” 등 다양한 감정 및 서술 단어가 고르게 분포했다.

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
플랫폼별 별점 분포 시각화:
![image](/review_analysis/plots/rating_distribution.png)

주요 차이:
| 항목             | Letterboxd       | Naver              | RottenTomatoes               |
|------------------|------------------|--------------------|------------------------------|
| 평균 평점        | **9.47**         | 8.17               | 8.70                         |
| 리뷰 길이        | **442.14자**      | 27.11자            | 171.41자                     |
| 감정 표현 단어   | best, like, ever | 재밌다, 좋다, 불편하다 | best, good, great, really, like |

Letterboxd는 감정 표현이 강하고 리뷰가 서술 중심으로 상대적으로 길었다.  
Naver는 감정을 짧고 직관적으로 표현하는 단문 리뷰가 많았다.  
RottenTomatoes는 감정 표현과 내용 중심 키워드가 균형 있게 나타나며, 빈도수 범위를 확장하면 `cinematography`, `brilliant`, `plot` 등의 키워드도 등장하였다.
