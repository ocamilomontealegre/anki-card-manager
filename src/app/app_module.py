from injector import Binder, Module, singleton

from health.health_module import HealthModule
from common.cache.cache_module import CacheModule
from common.database.database_module import DatabaseModule
from common.loggers.models.abstracts.logger_abstract import Logger
from common.loggers.app_logger import AppLogger
from modules.upload.upload_module import UploadModule
from modules.language.language_module import LanguageModule
from modules.word.word_module import WordModule
from modules.scraper.scraper_module import ScraperModule
from modules.anki.anki_module import AnkiModule
from modules.task.task_module import TaskModule


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
        binder.install(module=TaskModule)

        binder.bind(Logger, to=AppLogger, scope=singleton)
