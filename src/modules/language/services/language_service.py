from pathlib import Path
from typing import cast

from injector import inject
from openai import OpenAI
from pandas import read_csv

from common.enums import Language
from common.env.env_config import EnvVariables
from common.lib.ai_client.ai_client_adapter import AiClientAdapter
from common.loggers.models.abstracts.logger_abstract import Logger
from common.utils import FileUtils
from modules.language.maps.card_interface_map import card_interface_map
from modules.word.services.word_service import WordService

from ..models.interfaces import Row
from ..models.interfaces.card_response_interfaces.card_response_interface import (
    CardResponseBase,
)
from ..transformers.language_transformer import LanguageTransformer


class LanguageService:
    @inject
    def __init__(
        self,
        word_service: WordService,
        ai_client_adapter: AiClientAdapter,
        language_transformer: LanguageTransformer,
        logger: Logger,
    ) -> None:
        self._file = LanguageService.__name__

        self._env = EnvVariables.get()

        self._logger = logger

        self._word_service = word_service
        self.__ai_client_adapter = ai_client_adapter
        self._language_transformer = language_transformer

        self._ai_client = OpenAI(api_key=self._env.ai.key)

    def _build_prompt_messages(self, row: Row) -> list[dict[str, str]]:
        word = row["word"]
        language = row["language"]
        category = row.get("category") or "general"
        context = (
            row.get("context")
            or f"Informal, everyday {Language(language).value} used in spoken conversation or {Language(language).value} as second language learning"
        )

        user_prompt = (
            f"Generate a structured language card for the word '{word}' in {language}. "
            f"Focus on the most commonly used sense of the word when it functions as a {category}. "
        )

        if context:
            user_prompt += (
                f'The word appears in the following context: "{context}". '
                "Use this to guide your definition and example. "
            )

        return [
            {
                "role": "system",
                "content": (
                    "You are a polyglot linguist with over 10 years of experience in semantics, lexicography, and language education. "
                    "You specialize in identifying the most common and natural usages of words across different languages, providing accurate and culturally aware definitions and examples."
                ),
            },
            {"role": "user", "content": user_prompt},
        ]

    async def _process_row(self, row: Row) -> CardResponseBase | None:
        method = self._process_row.__name__

        word = row["word"]
        language = row["language"]

        try:
            self._logger.debug(
                f"Fetching data for word[{word}] with language[{language}]",
                file=self._file,
                method=method,
            )
            return self.__ai_client_adapter.get_structured_response(
                messages=self._build_prompt_messages(row),
                response_interface=card_interface_map[str(language)],
            )
        except Exception as e:
            self._logger.error(
                f"Error processing row: {row}, Error: {e}",
                file=self._file,
                method=method,
            )
            raise

    async def process_csv(self, file_name: str) -> None:
        df = read_csv(file_name, delimiter=",")

        for index, row in df.iterrows():
            try:
                card_response = await self._process_row(cast(Row, row.to_dict()))

                if not card_response:
                    continue

                transformed_word = await self._language_transformer.to_entity(
                    card_info=card_response
                )
                self._word_service.create(word=transformed_word)

            except Exception as e:
                self._logger.error(
                    f"Skipping row[{index}] due to error: {e}",
                    file=self._file,
                    method=self.process_csv.__name__,
                )
                continue

        if self._env.actions.delete:
            FileUtils.remove_file(file_path=Path(file_name))
