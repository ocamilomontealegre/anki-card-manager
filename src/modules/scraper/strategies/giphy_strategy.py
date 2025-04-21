from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from common.loggers.logger import AppLogger
from common.env.env_config import get_env_variables
from .base_strategy import BaseStrategy


class GiphyStrategy(BaseStrategy):
    def __init__(self):
        self.__logger = AppLogger(label=GiphyStrategy.__name__)

        self.__giphy_env = get_env_variables().giphy

    def get_image_url(self, query: str) -> str:
        first_image_selector = ".giphy-grid img"

        try:
            options = Options()
            options.add_argument("--headless")
            driver = webdriver.Chrome(options=options)
            driver.get(f"{self.__giphy_env.url}/{query}")
            sleep(5)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            print("SOUP: ", soup)
            img = soup.select_one(first_image_selector)

            if not img:
                raise Exception("Could not get image url") 

            return img["src"]
        except Exception as e:
            self.__logger.error(e, self.get_firts_image_url.__name__)
        finally:
            driver.quit()
