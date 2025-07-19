import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from review_analysis.crawling.base_crawler import BaseCrawler
from utils.logger import setup_logger

logger = setup_logger()


class RottenTomatoesCrawler(BaseCrawler):
    def __init__(self, output_dir: str):
        super().__init__(output_dir)
        self.reviews = []

    def start_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)
        logger.info("브라우저 시작 완료")

    def scrape_reviews(self):
        self.start_browser()
        url = "https://www.rottentomatoes.com/m/parasite_2019/reviews?type=user"
        self.driver.get(url)
        time.sleep(3)
        logger.info("리뷰 수집 시작")

        max_clicks = 50
        same_count_repeat_limit = 3
        prev_count = 0
        same_count_repeats = 0

        for i in range(max_clicks):
            review_cards = self.driver.find_elements(
                By.CLASS_NAME, "audience-review-row"
            )
            curr_count = len(review_cards)
            logger.info(f"[Load {i}] 현재 수집 수: {curr_count}")

            if curr_count == prev_count:
                same_count_repeats += 1
            else:
                same_count_repeats = 0

            if same_count_repeats >= same_count_repeat_limit:
                logger.info("리뷰 수 증가 없음. 종료.")
                break

            prev_count = curr_count

            button_clicked = self.driver.execute_script(
                """
                const shadowHost = document.querySelector('rt-button[data-qa="load-more-btn"]');
                if (!shadowHost) return false;
                const shadowRoot = shadowHost.shadowRoot;
                if (!shadowRoot) return false;
                const button = shadowRoot.querySelector('button');
                if (button && !button.disabled) {
                    button.click();
                    return true;
                }
                return false;
            """
            )

            if not button_clicked:
                logger.info("Load More 버튼 클릭 실패 또는 없음.")
                break

            try:
                WebDriverWait(self.driver, 10).until(
                    lambda d: len(d.find_elements(By.CLASS_NAME, "audience-review-row"))
                    > curr_count
                )
            except:
                logger.warning("리뷰 수 증가 없음. 타임아웃.")
                break

        review_cards = self.driver.find_elements(By.CLASS_NAME, "audience-review-row")
        logger.info(f"최종 수집 리뷰 수: {len(review_cards)}")

        for idx, card in enumerate(review_cards):
            try:
                stars_tag = card.find_element(By.TAG_NAME, "rating-stars-group")
                stars = float(stars_tag.get_attribute("score"))
                date = card.find_element(
                    By.CLASS_NAME, "audience-reviews__duration"
                ).text
                review = card.find_element(
                    By.CLASS_NAME, "audience-reviews__review"
                ).text
                self.reviews.append({"rating": stars, "date": date, "review": review})
            except Exception as e:
                logger.warning(f"[{idx}] 리뷰 파싱 실패: {e}")
                continue

        logger.info(f"최종 수집 리뷰 수: {len(self.reviews)}")
        self.driver.quit()
        logger.info("브라우저 종료")

    def save_to_database(self):
        if not self.reviews:
            logger.warning("저장할 리뷰가 없습니다.")
            return
        df = pd.DataFrame(self.reviews)
        os.makedirs(self.output_dir, exist_ok=True)
        save_path = os.path.join(self.output_dir, "reviews_rottentomatoes.csv")
        df.to_csv(save_path, index=False)
        logger.info(f"CSV 저장 완료: {save_path}")
