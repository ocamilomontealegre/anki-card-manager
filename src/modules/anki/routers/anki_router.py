from fastapi import APIRouter

from common.enums.app_endpoints_enum import AppEndpoints
from modules.anki.controllers.anki_controller import AnkiController


class AnkiRouter:
    def __init__(self, anki_controller: AnkiController):
        self._router = APIRouter(prefix=AppEndpoints.ANKI.value, tags=["Anki"])
        self._anki_controller = anki_controller

    @property
    def router(self) -> APIRouter:
        return self._router

    def _register_routes(self) -> None:
        self._router.add_api_route(
            "/",
            self._anki_controller.process,
            methods=["POST"],
        )
