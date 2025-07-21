import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from review_analysis.crawling.base_crawler import BaseCrawler
from utils.logger import setup_logger

logger = setup_logger()

def star_text_to_float(star_text: str) -> float:
    stars = star_text.count("★")
    half = 0.5 if "½" in star_text else 0.0
    return stars + half

class LetterboxdCrawler(BaseCrawler):
    def __init__(self, output_dir: str):
        super().__init__(output_dir)
        self.reviews: list = []
        self.max_reviews = 1000

    def start_browser(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
)
        self.driver = webdriver.Chrome(options=options)
        logger.info("브라우저 시작 완료")

    def scrape_reviews(self):
        self.start_browser()
        page = 1
        logger.info("리뷰 수집 시작")

        while len(self.reviews) < self.max_reviews:
            url = f"https://letterboxd.com/film/parasite-2019/reviews/by/activity/page/{page}/"
            self.driver.get(url)
            logger.info(f"{page} 페이지 로딩 중...")
            time.sleep(2)

            review_cards = self.driver.find_elements(By.CLASS_NAME, "production-viewing")
            if not review_cards:
                logger.info("더 이상 리뷰 없음.")
                break

            for  card in review_cards:
                try:
                    # 평점 추출
                    rating = star_text_to_float(card.find_element(By.CLASS_NAME, "rating").text.strip())
                    if not rating:
                        continue

                    # 날짜 추출 (정확한 datetime)
                    date = card.find_element(By.CLASS_NAME, "timestamp").get_attribute("datetime")

                    # 리뷰 본문 추출
                    review = card.find_element(By.CLASS_NAME, "body-text").text.strip()
                    if not review:
                        continue

                    self.reviews.append({
                        "date": date,
                        "rating": rating,
                        "review": review
                    })

                    if len(self.reviews) >= self.max_reviews:
                        break

                except Exception as e:
                    continue

            logger.info(f"{page} 페이지 리뷰 수집 완료 (누적: {len(self.reviews)}개)")
            page += 1

        self.driver.quit()
        logger.info("브라우저 종료")

    def save_to_database(self):
        if not self.reviews:
            logger.warning("저장할 리뷰가 없습니다.")
            return
        df = pd.DataFrame(self.reviews)
        os.makedirs(self.output_dir, exist_ok=True)
        save_path = os.path.join(self.output_dir, "reviews_letterboxd.csv")
        df.to_csv(save_path, index=False, encoding='utf-8')
        logger.info(f"CSV 저장 완료: {save_path}")
