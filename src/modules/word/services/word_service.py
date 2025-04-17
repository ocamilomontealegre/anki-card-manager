from os import path as os_path
from typing import List
from pathlib import Path
from datetime import datetime
from uuid import uuid4
from pandas import DataFrame
from injector import inject
from sqlalchemy.orm import Session
from common.database.strategies.database_strategy import DatabaseStrategy
from common.loggers.logger import AppLogger
from common.env.env_config import get_env_variables
from ..models.entities.word_entity import Word
from ..models.inferfaces.find_all_params import FindAllParams


class WordService():
    @inject
    def __init__(self, db: DatabaseStrategy) -> None:
        self.__session: Session = db.create_session()

        self.__logger: AppLogger = AppLogger(label=WordService.__name__)
        self.__anki_env = get_env_variables().anki

    def __format_audio_path(self, audio_path) -> str:
        if audio_path:
            return f"[sound:{os_path.basename(audio_path)}]"
        else:
            return ""

    def __transform_word(self, word: Word) -> dict:
        return {
            "id": word.id,
            "word": word.word,
            "category": word.category,
            "definition": word.definition,
            "sentence": word.sentence,
            "sentence_audio": self.__format_audio_path(word.sentence_audio),
            "phonetics": f"/{word.phonetics}/",
            "partial_sentence": word.partial_sentence,
            "singular": word.singular,
            "singular_audio": self.__format_audio_path(word.singular_audio),
            "plural": word.plural,
            "plural_audio": self.__format_audio_path(word.plural_audio),
            "synonyms": word.synonyms,
            "image": os_path.basename(word.image),
            "image_2": os_path.basename(word.image_2),
        }

    def create(self, word: Word) -> Word:
        new_word = self.__session.add(word)
        self.__session.commit()
        self.__session.refresh(word)
        self.__logger.info(f"{Word.__name__}[{word.word}] created successfully.", context=self.create.__name__)
        return new_word

    def create_many(self, words: List[Word]):
        new_words = self.__session.add_all(words)
        self.__session.commit
        self.__logger.info(f"{new_words}")

    def find_all(self, filters: FindAllParams):
        query = self.__session.query(Word)

        if "limit" in filters:
            query = query.limit(filters.limit or 100)

        if "offset" in filters:
            query = query.offset(filters.offset or 0)

        if "sort" in filters:
            query = query.order_by(filters.sort or Word.created_at.desc())

        if "category" in filters:
            query = query.filter(Word.category == filters["category"])

        if "word" in filters:
            query = query.filter(Word.word.contains(filters["word"]))

        if "language" in filters:
            query = query.filter(Word.language == filters["language"].value)

        words = query.all()
        self.__logger.info(f"{Word.__name__}[{len(words)}] found", self.find_all.__name__)
        return {
            "items": words,
            "total": len(words),
        }

    def get_as_csv(self, filters: FindAllParams):
        query = self.__session.query(Word)

        if "limit" in filters:
            query = query.limit(filters.limit or 100)

        if "offset" in filters:
            query = query.offset(filters.offset or 0)

        if "sort" in filters:
            query = query.order_by(filters.sort or Word.created_at.desc())

        if "category" in filters:
            query = query.filter(Word.category == filters["category"])

        if "word" in filters:
            query = query.filter(Word.word.contains(filters["word"]))

        if "language" in filters:
            query = query.filter(Word.language == filters["language"].value)

        result = query.all()
        words = [self.__transform_word(word) for word in result]
        df = DataFrame(words)

        output_path = Path(self.__anki_env.output) / f"{datetime.today().strftime("%Y-%m-%d")}-{uuid4()}.csv"

        df.to_csv(output_path, index=False, header=False)
        self.__logger.info(f"{Word.__name__}[{len(words)}] found", self.get_as_csv.__name__)
        return {"status": "OK"}

    def delete_all(self):
        delete_words = self.__session.query(Word).delete()
        self.__session.commit()
        self.__logger.info(f"{Word.__name__}[{delete_words}] deleted successfully", self.delete_all.__name__)
        return {"deleted": "OK"}
