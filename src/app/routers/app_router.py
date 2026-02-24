from fastapi import APIRouter
from injector import Injector

from health.routers.health_router import HealthRouter
from modules.anki.routers.anki_router import AnkiRouter
from modules.language.routers.language_router import LanguageRouter
from modules.task.routers.task_router import TaskRouter
from modules.upload.routers.upload_router import UploadRouter
from modules.word.routers.word_router import WordRouter


class AppRouter:
    def __init__(self, injector: Injector):
        self._router = APIRouter()
        self._injector = injector
        self._register_routes()

    @property
    def router(self) -> APIRouter:
        return self._router

    def _register_routes(self):
        health_router = self._injector.get(HealthRouter)
        upload_router = self._injector.get(UploadRouter)
        language_router = self._injector.get(LanguageRouter)
        word_router = self._injector.get(WordRouter)
        anki_router = self._injector.get(AnkiRouter)
        task_router = self._injector.get(TaskRouter)

        self._router.include_router(health_router.router)
        self._router.include_router(upload_router.router)
        self._router.include_router(word_router.router)
        self._router.include_router(anki_router.router)
        self._router.include_router(language_router.router)
        self._router.include_router(task_router.router)
