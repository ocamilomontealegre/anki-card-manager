from time import sleep
from playwright.async_api import async_playwright
from common.loggers.logger import AppLogger
from common.env.env_config import get_env_variables
from .base_strategy import BaseStrategy


class UnplashStrategy(BaseStrategy):
    def __init__(self):
        self.__logger = AppLogger(label=UnplashStrategy.__name__)

        self.__unplash_env = get_env_variables().unplash

    async def get_firts_image_url(self, query: str) -> str:
        search_bar_selector = "input[type='search'][name='searchKeyword']"
        first_image_selector = "div[data-testid='masonry-grid-count-three'] img"

        try:
            async with async_playwright() as playwright:
                browser = await playwright.chromium.launch(headless=False)
                page = await browser.new_page()

                await page.goto(self.__unplash_env.url, wait_until="load")

                search_bar = page.locator(selector=search_bar_selector).first
                await search_bar.fill(value=query)
                await search_bar.press(key='Enter')
                sleep(5)

                image = page.locator(first_image_selector).nth(4)
                image_url = await image.get_attribute('src')
                return image_url
        except Exception as e:
            self.__logger.error(e, self.get_firts_image_url.__name__)
        finally:
            await browser.close()