from injector import inject
from fastapi import APIRouter
from ..services.anki_service import AnkiService
from ..models.dto.create_cards_dto import CreateCardsDto


class AnkiController:
    @inject
    def __init__(self, anki_service: AnkiService) -> None:
        self.__anki_service = anki_service
        self.__router = APIRouter()
        self.__register_routes()

    def __register_routes(self):
        @self.__router.post("")
        async def create_cards(body: CreateCardsDto):
            result = self.__anki_service.create_cards(body or {})
            return {"url": result}

    def get_router(self) -> APIRouter:
        return self.__router
