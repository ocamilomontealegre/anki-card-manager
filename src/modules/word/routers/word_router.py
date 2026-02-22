from fastapi import APIRouter
from injector import inject

from common.enums.app_endpoints_enum import AppEndpoints
from modules.word.controllers.word_controller import WordController


class WordRouter:
    @inject
    def __init__(self, word_controller: WordController):
        self._router = APIRouter(prefix=AppEndpoints.WORD.value, tags=["Word"])
        self._language_controller = word_controller

        self._register_routes()

    @property
    def router(self) -> APIRouter:
        return self._router

    def _register_routes(self) -> None:
        self._router.add_api_route(
            "/",
            self._language_controller.list_paginated,
            methods=["GET"],
        )

        self._router.add_api_route(
            "/csv",
            self._language_controller.get_as_csv,
            methods=["GET"],
        )
