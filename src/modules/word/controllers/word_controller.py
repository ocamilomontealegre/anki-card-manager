from injector import inject
from fastapi import APIRouter, Depends
from common.enums import AppEndpoints
from common.models import ListPaginated, DeleteMany
from ..models.interfaces.find_all_params import FindAllParams
from ..services.word_service import WordService
from ..transformers.word_transformer import WordTransformer


class WordController:
    @inject
    def __init__(
        self, word_service: WordService, word_transformer: WordTransformer
    ) -> None:
        self._word_service = word_service
        self._word_transformer = word_transformer
        self._router = APIRouter(prefix=AppEndpoints.WORD.value, tags=["Word"])
        self._register_routes()

    def _register_routes(self):
        @self._router.get("", response_model=ListPaginated)
        async def list_paginated(params: FindAllParams = Depends()):
            (words, size) = self._word_service.list_paginated(params)
            transformed_words = [
                self._word_transformer.transform(word) for word in words
            ]
            return ListPaginated(
                items=transformed_words,
                total=len(transformed_words),
                page=((params.offset or 0) // (params.limit or 1)) + 1,
                size=params.limit or 1,
            )

        @self._router.get("/csv")
        async def get_as_csv(params: FindAllParams = Depends()):
            return self._word_service.get_as_csv(params)

        @self._router.delete("", response_model=DeleteMany)
        async def delete_all():
            return self._word_service.delete_all()

    def get_router(self) -> APIRouter:
        return self._router
