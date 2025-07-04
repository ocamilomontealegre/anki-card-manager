from pathlib import Path
from typing import cast, Union
from injector import inject

from pandas import read_csv
from openai import OpenAI

from common.loggers.models.abstracts.logger_abstract import Logger
from common.utils import FileUtils
from common.env.env_config import EnvVariables
from common.cache.strategies.cache_strategy import CacheStrategy
from modules.word.services.word_service import WordService
from ..transformers.language_transformer import LanguageTransformer
from ..models.interfaces import CardResponse, Row


class LanguageService:
    @inject
    def __init__(
        self,
        word_service: WordService,
        language_transformer: LanguageTransformer,
        cache_strategy: CacheStrategy,
        logger: Logger,
    ) -> None:
        self._file = LanguageService.__name__

        self._env = EnvVariables.get()

        self._logger = logger

        self._word_service = word_service
        self._language_transformer = language_transformer
        self._cache_strategy = cache_strategy

        self._open_ai_client = OpenAI(api_key=self._env.openai.key)

    def _build_promp(self, row: Row) -> str:
        word = row["word"]
        language = row["language"]
        category = row.get("category") or "general"
        context = row.get("context")

        user_prompt = (
            f"Generate a structured language card for the word '{word}' in {language}. "
            f"Focus on the most commonly used sense of the word when it functions as a {category}. "
        )

        if context:
            user_prompt += (
                f'The word appears in the following context: "{context}". '
                "Use this to guide your definition and example. "
            )

        user_prompt += (
            "Provide:\n"
            "- A clear, learner-friendly definition, it should not contain the word I'm searching for\n"
            "- Plural and singular forms (if relevant)\n"
            "- A list of common synonyms\n"
            "- A natural example sentence using the word\n"
            "- The IPA transcription of that sentence\n"
            "Add subtle usage or cultural notes if they help clarify the meaning or usage."
        )

        return user_prompt

    async def _process_row(self, row: Row) -> Union[CardResponse, None]:
        method = self._process_row.__name__

        word = row["word"]
        language = row["language"]

        try:
            if await self._cache_strategy.read(key=word):
                self._logger.debug(
                    f"Word data already in the cache: {word}",
                    file=self._file,
                    method=method,
                )
                return

            self._logger.debug(
                f"Fetching data for word[{word}] with language[{language}]",
                file=self._file,
                method=method,
            )
            completion = self._open_ai_client.beta.chat.completions.parse(
                model=self._env.openai.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a polyglot linguist with over 10 years of experience in semantics, lexicography, and language education. "
                            "You specialize in identifying the most common and natural usages of words across different languages, providing accurate and culturally aware definitions and examples."
                        ),
                    },
                    {"role": "user", "content": self._build_promp(row)},
                ],
                response_format=CardResponse,
            )
            data = completion.choices[0].message.parsed
            await self._cache_strategy.write(key=word, value=word)
            return data
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
                card_response = await self._process_row(
                    cast(Row, row.to_dict())
                )

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
