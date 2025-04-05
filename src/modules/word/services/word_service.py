from pathlib import Path
from uuid import uuid4
import pandas as pd
from injector import inject
from sqlalchemy.orm import Session
from common.database.strategies.database_strategy import DatabaseStrategy
from ..models.entities.word_entity import Word


class WordService():
    @inject
    def __init__(self, db: DatabaseStrategy) -> None:
        self.__session: Session = db.create_session()

    def create(self, word: Word) -> Word:
        new_word = self.__session.add(word)
        self.__session.commit()
        self.__session.refresh(word)
        return new_word

    def find_all(self, filters: dict):
        query = self.__session.query(Word)

        if "category" in filters:
            query = query.filter(Word.category == filters["category"])

        if "word" in filters:
            query = query.filter(Word.word.contains(filters["word"]))

        return query.all()

    def __transform_word(self, word: Word):
        return {
            "id": word.id,
            "word": word.word,
            "category": word.category,
            "definition": word.definition,
            "sentence": word.sentence,
            "sentence_audio": word.sentence_audio,
            "phonetics": word.phonetics,
            "partial_sentence": word.partial_sentence,
            "singular": word.singular,
            "singular_audio": word.singular_audio,
            "plural": word.plural,
            "plural_audio": word.plural_audio,
            "synonyms": word.synonyms,
            "image": word.image,
            "image_2": word.image_2,
        }

    def get_as_csv(self, filters: dict):
        query = self.__session.query(Word)

        if "category" in filters:
            query = query.filter(Word.category == filters["category"])

        if "word" in filters:
            query = query.filter(Word.word.contains(filters["word"]))

        result = query.all()
        words = [self.__transform_word(word) for word in result]
        df = pd.DataFrame(words)

        output_path = Path("output") / f"{uuid4()}.csv"

        df.to_csv(output_path, index=False)
        return {"status": "OK"}

    def delete_all(self):
        self.__session.query(Word).delete()
