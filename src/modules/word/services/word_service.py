from typing import List, Tuple
from pathlib import Path
from datetime import datetime
from uuid import uuid4

from pandas import DataFrame
from injector import inject
from sqlalchemy.orm import Session

from common.models import DeleteMany
from common.database.strategies.database_strategy import DatabaseStrategy
from common.loggers.models.abstracts.logger_abstract import Logger
from common.env.env_config import EnvVariables
from ..models.entities.word_entity import Word
from ..models.interfaces.find_all_params import FindAllParams
from ..transformers.word_transformer import WordTransformer


class WordService:
    @inject
    def __init__(
        self,
        word_transformer: WordTransformer,
        db: DatabaseStrategy,
        logger: Logger,
    ) -> None:
        self._file = WordService.__name__

        self._session: Session = db.create_session()

        self._word_transformer = word_transformer

        self._logger = logger
        self._env = EnvVariables.get().anki

    def _get_filter_query(self, filters: FindAllParams):
        query = self._session.query(Word)

        query = query.order_by(Word.created_at.desc())

        if filters.category:
            query = query.filter(Word.category == filters.category)

        if filters.word:
            query = query.filter(Word.word.contains(filters.word))

        if filters.language:
            language = (
                filters.language.value
                if hasattr(filters.language, "value")
                else filters.language
            )
            query = query.filter(Word.language == language)

        return query

    def create(self, word: Word) -> Word:
        self._session.add(word)
        self._session.commit()
        self._session.refresh(word)
        self._logger.info(
            f"{Word.__name__}[{word.word}] created successfully.",
            file=self._file,
            method=self.create.__name__,
        )
        return word

    def create_many(self, words: List[Word]):
        self._session.add_all(words)
        self._session.commit()
        self._logger.info(
            f"{len(words)} words created successfully.",
            file=self._file,
            method=self.create_many.__name__,
        )

    def list_paginated(self, filters: FindAllParams) -> Tuple[List[Word], int]:
        off_set = filters.offset or 0
        limit = filters.limit or 100

        query = self._get_filter_query(filters)
        words = query.offset(off_set).limit(limit).all()

        self._logger.info(
            f"{Word.__name__}[{len(words)}] found",
            file=self._file,
            method=self.list_paginated.__name__,
        )

        return (words, len(words))

    def get_as_csv(self, filters: FindAllParams):
        result = self._get_filter_query(filters).all()
        words = [self._word_transformer.transform(word) for word in result]
        df = DataFrame(words)

        output_path = (
            Path(self._env.output)
            / f"{datetime.today().strftime('%Y-%m-%d')}-{uuid4()}.csv"
        )

        df.to_csv(output_path, index=False, header=False)
        self._logger.info(
            f"{Word.__name__}[{len(words)}] found",
            file=self._file,
            method=self.get_as_csv.__name__,
        )
        return {"status": "OK"}

    def delete_all(self) -> DeleteMany:
        delete_words = self._session.query(Word).delete()
        self._session.commit()
        self._logger.info(
            f"{Word.__name__}[{delete_words}] deleted successfully",
            file=self._file,
            method=self.delete_all.__name__,
        )
        return DeleteMany(deleted="OK", total=delete_words)
