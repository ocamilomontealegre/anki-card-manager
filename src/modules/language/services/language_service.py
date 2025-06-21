from pathlib import Path
from typing import cast, Union
from injector import inject

from pandas import read_csv
from openai import OpenAI

from common.loggers.logger import AppLogger
from common.utils import FileUtils
from common.env.env_config import get_env_variables
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
    ) -> None:
        self._env = get_env_variables()

        self._logger = AppLogger(label=LanguageService.__name__)

        self._word_service = word_service
        self._language_transformer = language_transformer
        self._cache_strategy = cache_strategy

        self._open_ai_client = OpenAI(api_key=self._env.openai.key)

    async def _process_row(self, row: Row) -> Union[CardResponse, None]:
        word = row["word"]
        language = row["language"]
        category = row.get("category") or "general"

        try:
            if await self._cache_strategy.read(key=word):
                self._logger.debug(f"Word data already in the cache: {word}")
                return

            self._logger.debug(
                f"Fetchin data for word[{word}] with language[{language}] and category[{category}]"
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
                    {
                        "role": "user",
                        "content": (
                            f"Generate a structured language card for the word '{word}' in {language}. "
                            f"Focus on the most commonly used sense of the word when it functions as a {category}. "
                            "Provide:\n"
                            "- A clear, learner-friendly definition, it should not content the word I'm searching for\n"
                            "- Plural and singular forms (if relevant)\n"
                            "- A list of common synonyms\n"
                            "- A natural example sentence using the word\n"
                            "- The IPA transcription of that sentence\n"
                            "Add subtle usage or cultural notes if they help clarify the meaning or usage."
                        ),
                    },
                ],
                response_format=CardResponse,
            )
            data = completion.choices[0].message.parsed
            await self._cache_strategy.write(key=word, value=word)
            return data
        except Exception as e:
            self._logger.error(
                f"Error processing row: {row}, Error: {e}",
                self._process_row.__name__,
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
                    return

                transformed_word = await self._language_transformer.to_entity(
                    card_info=card_response
                )
                self._word_service.create(word=transformed_word)

            except Exception as e:
                self._logger.error(f"Skipping row[{index}] due to error: {e}")
                continue

        # FileUtils.remove_file(file_path=Path(file_name))
