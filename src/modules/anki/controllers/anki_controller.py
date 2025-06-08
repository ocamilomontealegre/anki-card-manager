from injector import inject
from fastapi import APIRouter
from modules.word.models.inferfaces.find_all_params import FindAllParams
from ..tasks.anki_task import process_anki_cards


class AnkiController:
    @inject
    def __init__(self) -> None:
        self.__router = APIRouter()
        self.__register_routes()

    def __register_routes(self):
        @self.__router.post("")
        async def create_cards(body: FindAllParams):
            print("BODY:", body)
            result = process_anki_cards.delay(filters=body.model_dump())  # type: ignore
            return {"message": "OK"}

    def get_router(self) -> APIRouter:
        return self.__router
