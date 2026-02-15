from injector import inject
from openai import BaseModel

from common.enums.language_enum import Language
from common.enums.word_category_enum import WordCategory
from common.lib.ai_client.ai_client_adapter import AiClientAdapter
from common.lib.http_client.http_client_adapter import HttpClientAdapter, HttpOptions
from common.loggers.models.abstracts.logger_abstract import Logger
from modules.language.models.interfaces.word_context_response_interface import (
    Context,
    WordContextResponse,
)


class Definition(BaseModel):
    definition: str


class Meaning(BaseModel):
    partOfSpeech: str
    definitions: list[Definition]


class DictionaryApiResponse(BaseModel):
    word: str
    meanings: list[Meaning]


class LanguageRepository:
    @inject
    def __init__(
        self, ai_client: AiClientAdapter, http_client: HttpClientAdapter, logger: Logger
    ):
        self._file = LanguageRepository.__name__

        self._ai_client = ai_client
        self._http_client = http_client
        self._logger = logger

    def _extract_word_context(self, meaning: Meaning) -> Context:
        return Context(
            category=WordCategory(meaning.partOfSpeech),
            definition=meaning.definitions[0].definition,
        )

    async def _get_context_from_api(self, *, word: str) -> WordContextResponse | None:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

        response = await self._http_client.request(
            url,
            http_options=HttpOptions(method="GET"),
            response_model=DictionaryApiResponse,
        )

        if response is not None:
            return WordContextResponse(
                word=word,
                context=[
                    self._extract_word_context(meaning) for meaning in response.meanings
                ],
            )

    async def _get_context_from_ai_client(
        self, *, word: str, language: Language
    ) -> WordContextResponse:
        prompt = [
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
                    f'Provide the 3 most common contemporary definitions of the word "{word} in the {language.value} language".\n'
                    "Requirements:\n"
                    "- Order by frequency (most common first)\n"
                    "- Keep definitions concise (1–2 sentences)\n"
                    "- Avoid archaic or rare meanings unless widely used"
                ),
            },
        ]

        response = self._ai_client.get_structured_response(
            messages=prompt, response_interface=WordContextResponse
        )

        return response

    async def get_word_context(
        self, *, word: str, language: Language
    ) -> WordContextResponse:
        try:
            if language.value == "en":
                response = await self._get_context_from_api(word=word)
                if response:
                    return response
                
            return await self._get_context_from_ai_client(word=word, language=language)
        except Exception as e:
            raise RuntimeError(f"Failed to get context for word {word}") from e
