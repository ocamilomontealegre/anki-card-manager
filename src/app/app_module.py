from injector import Binder, Module, singleton

from common.cache.cache_module import CacheModule
from common.database.database_module import DatabaseModule
from common.lib.ai_client.ai_client_adapter import AiClientAdapter
from common.lib.ai_client.open_ai_client_adapter import OpenAiClientAdapter
from common.loggers.app_logger import AppLogger
from common.loggers.models.abstracts.logger_abstract import Logger
from health.health_module import HealthModule
from modules.anki.anki_module import AnkiModule
from modules.language.language_module import LanguageModule
from modules.scraper.scraper_module import ScraperModule
from modules.task.task_module import TaskModule
from modules.upload.upload_module import UploadModule
from modules.word.word_module import WordModule


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
        binder.bind(AiClientAdapter, to=OpenAiClientAdapter, scope=singleton)
