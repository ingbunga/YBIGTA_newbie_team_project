# <EDA>
## 평점 분포
<img width="680" height="508" alt="image" src="https://github.com/user-attachments/assets/ee730127-b3a6-48d7-ae77-c297ad498e84" /><img width="684" height="507" alt="image" src="https://github.com/user-attachments/assets/ca770c49-e25d-466a-a2db-36ce51062447" />
<img width="727" height="514" alt="image" src="https://github.com/user-attachments/assets/be223f60-3aab-4ab4-8e36-8d92418a4ead" />
<img width="680" height="508" alt="image" src="https://github.com/user-attachments/assets/ff517de3-da6d-40ad-ab0f-0cdaae532540" />

naver 평균: 8.17
letterboxd 평균: 9.47
rottentomatoes평균: 8.70



## 길이 분포
naver:27.11자
letterboxd:442.14자
rottentomatoes:171.41자


## 주요 단어

<img width="801" height="435" alt="image" src="https://github.com/user-attachments/assets/cf61ae72-f9cc-4296-b43b-f500ddf88a08" />

<img width="796" height="426" alt="image" src="https://github.com/user-attachments/assets/efd4a2d2-d1ce-4676-921b-2b7a92b10d01" />

<img width="807" height="436" alt="image" src="https://github.com/user-attachments/assets/f1e11e44-52ea-488b-a42b-64620e2f29a1" />



# <전처리>
## -결측치 처리: 모든 Null값 제거

## -이상치 제거: 리뷰 길이 기준 Z-score로 비정상적으로 짧은 리뷰 제거 (Z < -2)

## -텍스트 전처리:
특수문자 제거 → 알파벳/숫자/공백만 남김

단어 토큰화 → nltk.word_tokenize 사용

불용어 제거 (nltk.stopwords)

표제어 추출 (WordNetLemmatizer)

최종적으로 토큰을 다시 문자열로 합침

## -파생 변수
review_length: 각 리뷰의 길이 (문자 수 기준)

review_z: 리뷰 길이의 Z-score

keywords: TF-IDF 기반 중요 단어 5개 추출 (문서별)


## -텍스트 벡터화
TfidfVectorizer(max_features=100) 사용

각 리뷰를 100차원 벡터로 변환

상위 TF-IDF 점수 기준으로 문서별 주요 키워드 5개 추출 후 저장


# <비교 분석>
주요 감정단어
naver: 재밌다, 좋다, 불편하다..
letterboxd: best, like, ever
rottentomatoes:best, good, great, really,like, 
rottentomatoes가 상대적으로 감정을 표현하는 단어가 다양했고 빈도수도 높았다.
