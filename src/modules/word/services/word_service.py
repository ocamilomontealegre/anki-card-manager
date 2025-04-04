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

    def find_all(self):
        words = self.__session.query(Word).all()
        return words

    def delete_all(self):
        self.__session.query(Word).delete()
