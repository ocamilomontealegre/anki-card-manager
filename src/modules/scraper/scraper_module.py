from injector import Binder, Module, singleton
from .services.scraper_service import ScraperService


class ScraperModule(Module):
    def configure(self, binder: Binder):
        binder.bind(ScraperService, to=ScraperService, scope=singleton)
