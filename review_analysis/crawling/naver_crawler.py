import os
from dataclasses import dataclass
from typing import Optional
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException
from review_analysis.crawling.base_crawler import BaseCrawler
from utils.logger import setup_logger

logger = setup_logger()

@dataclass
class CrawledReview:
    rating: int
    date: str
    review: str

SCROLLER_SELECTOR = '#main_pack div._content[data-tab="audience"] > div.lego_review_list._scroller'


class NaverCrawler(BaseCrawler):
    def __init__(self, output_dir: str):
        super().__init__(output_dir)
        self.driver: Optional[webdriver.Chrome] = None
        self.reviews: list[CrawledReview] = []

    def start_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        logger.info("브라우저 시작 완료")

    def scrape_reviews(self):
        return self._scrape_reviews("기생충", 300)

    def _scrape_reviews(self, movie_name: str, limit: int = 100):
        self.start_browser()
        url = f"https://search.naver.com/search.naver?query=영화 {movie_name} 관람평"
        if not self.driver:
            raise RuntimeError("브라우저가 시작되지 않았습니다.")
        driver = self.driver
    
        driver.get(url)
        driver.implicitly_wait(10)
        logger.info("리뷰 수집 시작")

        scroller = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, SCROLLER_SELECTOR))
        )

        def get_scroller_height() -> int:
            return driver.execute_script("return arguments[0].scrollHeight", scroller)
        
        def scroll_to_bottom():
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroller)
        
        def get_review_count() -> int:
            return int(driver.execute_script("return document.querySelectorAll(arguments[0] + ' > ul > li').length", SCROLLER_SELECTOR))

        
        try:
            scroll_height = get_scroller_height()
            while get_review_count() < limit:
                logger.info(f"현재 스크롤 높이: {scroll_height}, 리뷰 수: {get_review_count()}")
                scroll_to_bottom()
                WebDriverWait(driver, 2).until(
                    lambda _: get_scroller_height() > scroll_height
                )
                scroll_height = get_scroller_height()
        except TimeoutException as e:
            logger.warning(f"스크롤 중 타임아웃 발생, 리뷰 없음 의심: {e}")
        

        def extract_review(element: WebElement) -> CrawledReview:
            rating = int(element.find_element(By.CSS_SELECTOR, "div.lego_movie_pure_star").text.strip().replace("별점(10점 만점 중)", ""))
            date = element.find_elements(By.CSS_SELECTOR, "dl.cm_upload_info > dd")[1].text.strip()
            review = element.find_element(By.CSS_SELECTOR, "div.area_review_content span._text").text
            return CrawledReview(rating=rating, date=date, review=review)
        
        review_elements = driver.find_elements(By.CSS_SELECTOR, SCROLLER_SELECTOR + " > ul > li")

        for element in review_elements:
            review = extract_review(element)
            self.reviews.append(review)

        logger.info(f"최종 수집 리뷰 수: {len(self.reviews)}")
        self.driver.quit()
        logger.info("브라우저 종료")
            
    def save_to_database(self):
        if not self.reviews:
            logger.warning("저장할 리뷰가 없습니다.")
            return
        df = pd.DataFrame(self.reviews)
        os.makedirs(self.output_dir, exist_ok=True)
        save_path = os.path.join(self.output_dir, "reviews_naver.csv")
        df.to_csv(save_path, index=False)
        logger.info(f"CSV 저장 완료: {save_path}")