from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from common.loggers.logger import AppLogger
from common.env.env_config import get_env_variables
from common.exceptions import ImageScrapingException
from .base_strategy import BaseStrategy


class UnplashStrategy(BaseStrategy):
    def __init__(self):
        self.__logger = AppLogger(label=UnplashStrategy.__name__)
        self.__unplash_env = get_env_variables().unplash

    def get_image_url(self, query: str) -> str:
        image_selector = "img[data-testid='photo-grid-masonry-img']"
        driver = None

        try:
            options = Options()
            options.add_argument("--headless")
            driver = webdriver.Chrome(options=options)
            driver.get(f"{self.__unplash_env.url}/{query}")
            sleep(5)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            img = soup.select_one(image_selector)

            if not img:
                raise ImageScrapingException(
                    "No image found matching the selector"
                )

            return img["src"]
        except WebDriverException as e:
            self.__logger.error(
                f"Selenium error: {str(e)}", self.get_image_url.__name__
            )
            raise ImageScrapingException(f"Failed to scrape image: {str(e)}")
        except Exception as e:
            self.__logger.error(
                f"Unexpected error: {str(e)}", self.get_image_url.__name__
            )
            raise ImageScrapingException(
                f"Unexpected error while scraping: {str(e)}"
            )
        finally:
            if driver:
                driver.quit()
