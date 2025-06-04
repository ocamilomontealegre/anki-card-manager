from injector import inject
from fastapi import APIRouter, Depends
from ..models.inferfaces.find_all_params import FindAllParams
from ..services.word_service import WordService


class WordController:
    @inject
    def __init__(self, word_service: WordService) -> None:
        self.__word_service = word_service
        self.__router = APIRouter()
        self.__register_routes()

    def __register_routes(self):

        @self.__router.get("/")
        async def find_all(params: FindAllParams = Depends()):
            return self.__word_service.find_all(params)

        @self.__router.get("/csv")
        async def get_as_csv(params: FindAllParams = Depends()):
            return self.__word_service.get_as_csv(params)

        @self.__router.delete("/")
        async def delete_all():
            return self.__word_service.delete_all()

    def get_router(self) -> APIRouter:
        return self.__router
