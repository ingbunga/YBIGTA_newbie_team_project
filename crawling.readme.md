# Crawling

## 데이터 소개

### reviews_letterboxd.csv

#### 크롤링한 사이트
[letterboxd](https://letterboxd.com/film/parasite-2019/reviews/)
#### 변수 (3개 동일)
|변수명 | 설명       |
|------|----------|
|date  | 날짜      |
|rating| 평점      |
|review| 리뷰 텍스트 |
#### 크롤링 리뷰 갯수
1000개

### reviews_naver.csv
#### 크롤링한 사이트
[네이버](https://search.naver.com/search.naver?query=%EA%B8%B0%EC%83%9D%EC%B6%A9)
#### 변수 (3개 동일)
|변수명 | 설명       |
|------|----------|
|date  | 날짜      |
|rating| 평점      |
|review| 리뷰 텍스트 |
#### 크롤링 리뷰 갯수
1000개

### reviews_rottentomatoes.csv
#### 크롤링한 사이트
[로튼 토마토](https://www.rottentomatoes.com/m/parasite_2019/reviews?type=user)
#### 변수 (3개 동일)
|변수명 | 설명       |
|------|----------|
|date  | 날짜      |
|rating| 평점      |
|review| 리뷰 텍스트 |
#### 크롤링 리뷰 갯수
1020개

## 크롤러 실행 방법
루트 디렉토리에서 다음과 같은 명령을 입력해주세요.
```sh
pip install -r requirements.txt
pip install selenium
pip install pandas
python -m review_analysis.crawling.main -o ./database -a
```
<!--
    pip install selenium
    pip install pandas

    는 requirements.txt에 포함될 시 삭제될 수 있음.
-->