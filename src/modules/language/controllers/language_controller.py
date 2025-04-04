from injector import inject
from fastapi import APIRouter
from ..services.language_service import LanguageService


class LanguageController:
    @inject
    def __init__(self, language_service: LanguageService) -> None:
        self.language_service = language_service
        self.__router = APIRouter()
        self.__register_routes()

    def __register_routes(self):
        pass

    def get_router(self) -> APIRouter:
        return self.__router
