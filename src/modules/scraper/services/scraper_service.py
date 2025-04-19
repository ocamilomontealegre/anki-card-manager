from injector import inject
from ..strategies.base_strategy import BaseStrategy


class ScraperService():
    @inject
    def __init__(self, scraper_strategy: BaseStrategy):
        self.__scraper_strategy = scraper_strategy

    def get_image_url(self, query: str) -> str:
        return self.__scraper_strategy.get_firts_image_url(query=query)
