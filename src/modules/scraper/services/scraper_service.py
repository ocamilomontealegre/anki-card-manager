from injector import inject
from ..strategies.giphy_strategy import GiphyStrategy
from ..strategies.unplash_strategy import UnplashStrategy


class ScraperService():
    @inject
    def __init__(self, giphy_strategy: GiphyStrategy, unplash_strategy: UnplashStrategy):
        self.__giphy_strategy = giphy_strategy
        self.__unplash_strategy = unplash_strategy

    def get_giphy_image_url(self, query: str) -> str:
        return self.__giphy_strategy.get_image_url(query=query)

    def get_unplash_image_url(self, query: str) -> str:
        return self.__unplash_strategy.get_image_url(query=query)
