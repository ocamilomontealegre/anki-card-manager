from fastapi import APIRouter
from injector import inject

from common.enums.app_endpoints_enum import AppEndpoints
from common.models.task_response_model import TaskResponse
from modules.language.controllers.language_controller import (
    LanguageController,
)
from modules.language.models.interfaces.word_context_response_interface import (
    WordContextResponse,
)


class LanguageRouter:
    @inject
    def __init__(self, language_controller: LanguageController):
        self._router = APIRouter(prefix=AppEndpoints.LANGUAGE.value, tags=["Language"])
        self._language_controller = language_controller

        self._register_routes()

    @property
    def router(self) -> APIRouter:
        return self._router

    def _register_routes(self) -> None:
        self._router.add_api_route(
            "/context",
            self._language_controller.get_word_context,
            methods=["POST"],
            response_model=WordContextResponse,
        )

        self._router.add_api_route(
            "/",
            self._language_controller.create_word_entry,
            methods=["POST"],
        )

        self._router.add_api_route(
            "/process",
            self._language_controller.process,
            methods=["POST"],
            response_model=TaskResponse,
        )
