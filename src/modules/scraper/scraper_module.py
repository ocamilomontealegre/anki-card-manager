from injector import Binder, Module, singleton
from .services.scraper_service import ScraperService
from .strategies.giphy_strategy import GiphyStrategy
from .strategies.unplash_strategy import UnplashStrategy


class ScraperModule(Module):
    def configure(self, binder: Binder):
        binder.bind(ScraperService, to=ScraperService, scope=singleton)
        binder.bind(GiphyStrategy, to=GiphyStrategy, scope=singleton)
        binder.bind(UnplashStrategy, to=UnplashStrategy, scope=singleton)
