from typing import Dict, TypedDict, Literal
from urllib.parse import quote
from bs4 import BeautifulSoup
from injector import inject
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from common.loggers.models.abstracts.logger_abstract import Logger
from common.utils.language_utils import LanguageUtils
from common.enums import Language
from common.env import EnvVariables


ImageSource = Literal["pinterest", "giphy"]

ImageSourceMap = Dict[ImageSource, str]


class GetImage(TypedDict):
    query: str
    target_language: Language
    source: ImageSource


class ScraperService:
    @inject
    def __init__(self, logger: Logger):
        self._file = ScraperService.__name__

        self._env = EnvVariables.get()
        self._logger = logger

        self._html_selectors: ImageSourceMap = {
            "pinterest": "div[role='list'] div[role='listitem'] img",
            "giphy": ".giphy-grid img",
        }

        self._image_engine: ImageSourceMap = {
            "pinterest": self._env.pinterest.url,
            "giphy": self._env.giphy.url,
        }

    async def get_image_url(self, data: GetImage) -> str:
        method = self.get_image_url.__name__

        query = data["query"]
        target_language = Language(data["target_language"])
        source = data["source"]

        if target_language != Language.ENGLISH:
            query = await LanguageUtils.translate(
                {
                    "text": query,
                    "source": target_language,
                    "target": Language.ENGLISH,
                }
            )

        self._logger.debug(
            f"Try to fetch image for word[{data['query']}]",
            file=self._file,
            method=method,
        )

        try:
            query_encoded = quote(query)
            url = f"{self._image_engine[source]}/{query_encoded}"

            options = ChromeOptions()
            options.add_argument("--headless")
            options.add_argument(
                "--disable-blink-features=AutomationControlled"
            )

            driver = Chrome(options=options)
            try:
                driver.get(url)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, self._html_selectors[source])
                    )
                )
                page_source = driver.page_source
            finally:
                driver.quit()

            soup = BeautifulSoup(page_source, "html.parser")
            imgs = soup.select(self._html_selectors[source])

            return str(imgs[0]["src"]) or ""
        except Exception as e:
            self._logger.error(
                f"Unexpected error: {e}",
                file=self._file,
                method=method,
            )
            return ""
