from pyee.asyncio import AsyncIOEventEmitter
from injector import Binder, Module, singleton
from health.health_module import HealthModule
from common.cache.cache_module import CacheModule
from common.database.database_module import DatabaseModule
from modules.upload.upload_module import UploadModule
from modules.language.language_module import LanguageModule
from modules.word.word_module import WordModule
from modules.scraper.scraper_module import ScraperModule
from modules.anki.anki_module import AnkiModule


class AppModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.install(module=HealthModule)
        binder.install(module=DatabaseModule)
        binder.install(module=CacheModule)
        binder.install(module=UploadModule)
        binder.install(module=LanguageModule)
        binder.install(module=WordModule)
        binder.install(module=ScraperModule)
        binder.install(module=AnkiModule)
        binder.bind(
            AsyncIOEventEmitter, to=AsyncIOEventEmitter, scope=singleton
        )
