from injector import inject
from fastapi import APIRouter, Depends
from common.enums import AppEndpoints
from common.models import ListPaginated, DeleteMany
from ..models.inferfaces.find_all_params import FindAllParams
from ..services.word_service import WordService


class WordController:
    @inject
    def __init__(self, word_service: WordService) -> None:
        self.__word_service = word_service
        self.__router = APIRouter(
            prefix=AppEndpoints.WORD.value, tags=["Word"]
        )
        self.__register_routes()

    def __register_routes(self):

        @self.__router.get("", response_model=ListPaginated)
        async def list_paginated(params: FindAllParams = Depends()):
            return self.__word_service.list_paginated(params)

        @self.__router.get("/csv")
        async def get_as_csv(params: FindAllParams = Depends()):
            return self.__word_service.get_as_csv(params)

        @self.__router.delete("", response_model=DeleteMany)
        async def delete_all():
            return self.__word_service.delete_all()

    def get_router(self) -> APIRouter:
        return self.__router
