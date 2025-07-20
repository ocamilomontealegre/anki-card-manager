from time import sleep
from urllib.parse import quote_plus
from typing import Dict, TypedDict, Literal, List
from injector import inject
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from common.loggers.models.abstracts.logger_abstract import Logger
from common.env import EnvVariables


ImageSource = Literal["google"]

ImageSourceMap = Dict[ImageSource, str]


class GetImage(TypedDict):
    query: str
    source: ImageSource


class ScraperService:
    @inject
    def __init__(self, logger: Logger):
        self._file = ScraperService.__name__

        self._env = EnvVariables.get()
        self._logger = logger

        self._html_selectors: ImageSourceMap = {
            "google": "#center_col img[src^='data:image']",
        }

        self._image_engine: ImageSourceMap = {
            "google": self._env.google.images,
        }

    def _build_search_url(self, query: str, source: ImageSource) -> str:
        query_encoded = quote_plus(query)
        return f"{self._image_engine[source]}{query_encoded}"

    def _init_driver(self) -> Chrome:
        options = ChromeOptions()

        options.add_argument("--headless")
        options.add_argument("--disable-blink-features=AutomationControlled")
        return Chrome(options=options, version_main=137, use_subprocess=True)

    def get_image_url(self, data: GetImage) -> List[str]:
        method = self.get_image_url.__name__

        query = data["query"]
        source = data["source"]

        self._logger.debug(
            f"Try to fetch image for word[{data['query']}]",
            file=self._file,
            method=method,
        )

        try:
            search_url = self._build_search_url(query=query, source=source)

            image_urls = []

            with self._init_driver() as driver:
                driver.get(search_url)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, self._html_selectors[source])
                    )
                )

                sleep(2)

                images = driver.find_elements(
                    By.CSS_SELECTOR, self._html_selectors[source]
                )

                for _, image in enumerate(images):
                    try:
                        width = driver.execute_script(
                            "return arguments[0].naturalWidth;", image
                        )
                        height = driver.execute_script(
                            "return arguments[0].naturalHeight;", image
                        )

                        if width < 100 or height < 100:
                            continue

                        image.click()

                        full_image = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located(
                                (
                                    By.XPATH,
                                    "//img[@src and starts-with(@src, 'http') and not(contains(@src, 'gstatic.com')) and not(starts-with(@src, 'data:'))]",
                                )
                            )
                        )
                        image_url = full_image.get_attribute("src")
                        if image_url and image_url.startswith("http"):
                            image_urls.append(image_url)

                        if len(image_urls) == 2:
                            break
                    except Exception as e:
                        self._logger.error(
                            f"Error processing an image: {e}",
                            file=self._file,
                            method=method,
                        )
                        continue
            return image_urls
        except Exception as e:
            self._logger.error(
                f"Unexpected error: {e}",
                file=self._file,
                method=method,
            )
            return []
