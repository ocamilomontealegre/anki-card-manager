from fastapi import APIRouter, Depends
from injector import inject

from common.enums import AppEndpoints
from common.models import ListPaginated

from ..models.interfaces.list_params import ListParams
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

    async def list_paginated(self, params: ListParams = Depends()):
        (words, size) = self._word_service.list(params)
        transformed_words = [self._word_transformer.transform(word) for word in words]
        return ListPaginated(
            items=transformed_words,
            total=len(transformed_words),
            page=((params.offset or 0) // (params.limit or 1)) + 1,
            size=params.limit or 1,
        )

    async def get_as_csv(self, params: ListParams = Depends()):
        return self._word_service.get_as_csv(params)
