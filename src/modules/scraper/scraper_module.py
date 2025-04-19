from injector import Binder, Module, singleton
from .strategies.base_strategy import BaseStrategy
from .strategies.giphy_strategy import GiphyStrategy
from .strategies.unplash_strategy import UnplashStrategy


class ScraperModule(Module):
    def configure(self, binder: Binder):
        binder.bind(BaseStrategy, to=UnplashStrategy, scope=singleton)
