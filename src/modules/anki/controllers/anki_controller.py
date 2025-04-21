from injector import inject
from fastapi import APIRouter, Request
from ..services.anki_service import AnkiService


class AnkiController:
    @inject
    def __init__(self, anki_service: AnkiService) -> None:
        self.__anki_service = anki_service
        self.__router = APIRouter()
        self.__register_routes()

    def __register_routes(self):
        @self.__router.post("")
        async def create_cards(req: Request):
            result = self.__anki_service.create_cards()
            return {"url": result}

    def get_router(self) -> APIRouter:
        return self.__router
