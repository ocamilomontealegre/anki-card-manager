from word.models.entities.word_entity import Word

from common.database.strategies.database_strategy import DatabaseStrategy
from modules.word.models.interfaces.list_params import ListParams


class WordRepository:
    def __init__(self, db_strategy: DatabaseStrategy):
        self._session = db_strategy.create_session()

    def _get_filter_query(self, filters: ListParams):
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

    def list(self, params: ListParams) -> list[Word]:
        off_set = params.offset or 0
        limit = params.limit or 100

        query = self._get_filter_query(params)
        words = query.offset(off_set).limit(limit).all()

        return words

    def create(self, word: Word) -> Word:
        self._session.add(word)
        self._session.commit()
        self._session.refresh(word)

        return word
