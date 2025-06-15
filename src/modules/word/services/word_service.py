from typing import List, Tuple
from pathlib import Path
from datetime import datetime
from uuid import uuid4
from pandas import DataFrame
from injector import inject
from sqlalchemy.orm import Session
from common.models import DeleteMany
from common.database.strategies.database_strategy import DatabaseStrategy
from common.loggers.logger import AppLogger
from common.env.env_config import get_env_variables
from ..models.entities.word_entity import Word
from ..models.inferfaces.find_all_params import FindAllParams
from ..transformers.word_transformer import WordTransformer


class WordService:
    @inject
    def __init__(
        self, word_transformer: WordTransformer, db: DatabaseStrategy
    ) -> None:
        self.__session: Session = db.create_session()

        self.__word_transformer = word_transformer

        self.__logger: AppLogger = AppLogger(label=WordService.__name__)
        self.__anki_env = get_env_variables().anki

    def _get_filter_query(self, filters: FindAllParams):
        query = self.__session.query(Word)

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
        self.__session.add(word)
        self.__session.commit()
        self.__session.refresh(word)
        self.__logger.info(
            f"{Word.__name__}[{word.word}] created successfully.",
            context=self.create.__name__,
        )
        return word

    def create_many(self, words: List[Word]):
        self.__session.add_all(words)
        self.__session.commit()
        self.__logger.info(
            f"{len(words)} words created successfully.",
            context=self.create_many.__name__,
        )

    def list_paginated(self, filters: FindAllParams) -> Tuple[List[Word], int]:
        off_set = filters.offset or 0
        limit = filters.limit or 100

        query = self._get_filter_query(filters)
        words = query.offset(off_set).limit(limit).all()

        self.__logger.info(
            f"{Word.__name__}[{len(words)}] found",
            self.list_paginated.__name__,
        )

        return (words, len(words))

    def get_as_csv(self, filters: FindAllParams):
        result = self._get_filter_query(filters).all()
        words = [self.__word_transformer.transform(word) for word in result]
        df = DataFrame(words)

        output_path = (
            Path(self.__anki_env.output)
            / f"{datetime.today().strftime('%Y-%m-%d')}-{uuid4()}.csv"
        )

        df.to_csv(output_path, index=False, header=False)
        self.__logger.info(
            f"{Word.__name__}[{len(words)}] found", self.get_as_csv.__name__
        )
        return {"status": "OK"}

    def delete_all(self) -> DeleteMany:
        delete_words = self.__session.query(Word).delete()
        self.__session.commit()
        self.__logger.info(
            f"{Word.__name__}[{delete_words}] deleted successfully",
            self.delete_all.__name__,
        )
        return DeleteMany(deleted="OK", total=delete_words)
