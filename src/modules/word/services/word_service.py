from datetime import datetime
from pathlib import Path
from uuid import uuid4

from injector import inject
from pandas import DataFrame

from common.env.env_config import EnvVariables
from common.loggers.models.abstracts.logger_abstract import Logger
from modules.word.repositories.word_repository import WordRepository

from ..models.entities.word_entity import Word
from ..models.interfaces.list_params import ListParams
from ..transformers.word_transformer import WordTransformer


class WordService:
    @inject
    def __init__(
        self,
        word_repository: WordRepository,
        word_transformer: WordTransformer,
        logger: Logger,
    ) -> None:
        self._word_repository = word_repository
        self._word_transformer = word_transformer

        self._logger = logger
        self._env = EnvVariables.get().anki

    def create(self, word: Word) -> Word:
        created_word = self._word_repository.create(word)
        self._logger.info(
            f"{Word.__name__}[{word.word}] created successfully.",
        )
        return created_word

    def list(self, filters: ListParams) -> tuple[list[Word], int]:
        words = self._word_repository.list(filters)

        self._logger.info(
            f"{Word.__name__}[{len(words)}] found",
        )

        return (words, len(words))

    def get_as_csv(self, filters: ListParams):
        result = self._word_repository.list(filters)
        words = [self._word_transformer.transform(word) for word in result]
        df = DataFrame(words)

        output_path = (
            Path(self._env.output)
            / f"{datetime.today().strftime('%Y-%m-%d')}-{uuid4()}.csv"
        )

        df.to_csv(output_path, index=False, header=False)
        self._logger.info(
            f"{Word.__name__}[{len(words)}] found",
        )
        return {"status": "OK"}
