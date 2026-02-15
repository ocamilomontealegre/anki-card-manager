from fastapi import APIRouter
from injector import Injector

from health.controllers.health_controller import HealthController
from modules.anki.controllers.anki_controller import AnkiController
from modules.language.routers.language_router import LanguageRouter
from modules.scraper.controllers.scraper_controller import ScraperController
from modules.task.routers.task_router import TaskRouter
from modules.upload.controllers.upload_controller import UploadController
from modules.word.controllers.word_controller import WordController


class AppRouter:
    def __init__(self, injector: Injector):
        self._router = APIRouter()
        self._injector = injector
        self._register_routes()

    @property
    def router(self) -> APIRouter:
        return self._router

    def _register_routes(self):
        health_controller = self._injector.get(HealthController)
        upload_controller = self._injector.get(UploadController)
        language_router = self._injector.get(LanguageRouter)
        word_controller = self._injector.get(WordController)
        scraper_controller = self._injector.get(ScraperController)
        anki_controller = self._injector.get(AnkiController)
        task_router = self._injector.get(TaskRouter)

        self._router.include_router(health_controller.get_router())
        self._router.include_router(upload_controller.get_router())
        self._router.include_router(word_controller.get_router())
        self._router.include_router(scraper_controller.get_router())
        self._router.include_router(anki_controller.get_router())
        self._router.include_router(language_router.router)
        self._router.include_router(task_router.router)
