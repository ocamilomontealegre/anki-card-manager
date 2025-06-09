import requests
from re import sub, escape
from uuid import uuid4
from pathlib import Path
from typing import List, Literal, Optional, Union, cast
from injector import inject
from pandas import read_csv
from openai import OpenAI
from common.loggers.logger import AppLogger
from common.utils.google_utils import GoogleUtils
from common.env.env_config import get_env_variables
from common.cache.strategies.cache_strategy import CacheStrategy
from modules.word.services.word_service import WordService
from modules.scraper.services.scraper_service import ScraperService
from modules.word.models.entities.word_entity import Word
from ..models.interfaces import CardResponse, Row


class LanguageService:
    @inject
    def __init__(
        self,
        word_service: WordService,
        scraper_service: ScraperService,
        cache_strategy: CacheStrategy,
    ) -> None:
        self.__env = get_env_variables()

        self.__logger = AppLogger(label=LanguageService.__name__)

        self.__word_service = word_service
        self.__scraper_service = scraper_service
        self.__cache_strategy = cache_strategy

        self.__open_ai_client = OpenAI(api_key=self.__env.openai.key)

    def __download_image(self, url: str, word: str) -> str:
        response = requests.get(url, stream=True)

        extension = ""
        if "giphy" in url:
            extension = "gif"
        else:
            extension = "jpg"

        path = (
            Path(self.__env.anki.media)
            / f"{word}_{uuid4().hex[:8]}.{extension}"
        )
        with open(path, "wb") as f:
            for chunk in response.iter_content(8192):
                f.write(chunk)

        return str(path)

    def __get_audio_path(
        self, word: str, prefix: Literal["", "plural", "singular"] = ""
    ) -> str:
        full_prefix = f"{prefix}_" if prefix else ""

        return f"{self.__env.anki.media}/{full_prefix}{word}.mp3"

    def __check_word_forms(
        self, base_word: str, word_forms: Optional[str]
    ) -> str:
        if word_forms and word_forms != ", ":
            return word_forms[:-1] if word_forms[-1] == "," else word_forms
        else:
            return f"{base_word[0].upper()}{base_word[1:]}"

    async def __transform_card(self, card_info: CardResponse) -> Word:
        try:
            word = card_info.word
            language = card_info.language
            plural = ", ".join(
                list(map(lambda x: x.capitalize(), card_info.plural))
            )
            singular = ", ".join(
                list(map(lambda x: x.capitalize(), card_info.singular))
            )
            synonyms = ", ".join(
                list(map(lambda x: x.capitalize(), card_info.synonyms))
            )
            sentence = card_info.sentence
            partial_sentence = sub(rf"\b{escape(word)}\b", "[...]", sentence)
            word_forms = f"{singular}, {plural}"

            giphy_image_url = self.__scraper_service.get_giphy_image_url(
                query=word
            )

            unplash_image_url = self.__scraper_service.get_unplash_image_url(
                query=word
            )
            sentence_path = await GoogleUtils.synthetize_text(
                text=sentence,
                language=language,
                output_file=Path(self.__get_audio_path(word=word)),
            )

            plural_audio_path = ""
            if len(plural) > 0:
                plural_audio_path = await GoogleUtils.synthetize_text(
                    text=plural,
                    language=language,
                    output_file=Path(
                        self.__get_audio_path(word=word, prefix="plural")
                    ),
                )

            singular_audio_path = ""
            if len(singular) > 0:
                singular_audio_path = await GoogleUtils.synthetize_text(
                    text=singular,
                    language=language,
                    output_file=Path(
                        self.__get_audio_path(word=word, prefix="singular")
                    ),
                )

            new_word = Word(
                word=self.__check_word_forms(word, word_forms),
                language=language.value,
                category=card_info.category.value.capitalize(),
                definition=card_info.definition.capitalize(),
                sentence=sentence,
                phonetics=card_info.sentence_phonetics,
                sentence_audio=sentence_path,
                partial_sentence=partial_sentence,
                singular=singular,
                singular_audio=singular_audio_path,
                plural=plural,
                plural_audio=plural_audio_path,
                synonyms=synonyms,
                image=self.__download_image(giphy_image_url, word),
                image_2=self.__download_image(unplash_image_url, word),
            )
            print("NEW_CARD: ", new_word)
            return new_word
        except Exception as e:
            self.__logger.error(
                f"Error transforming card: {e}", self.__transform_card.__name__
            )
            raise

    def process_cards(self, cards_info: List[Word]) -> None:
        self.__word_service.create_many(cards_info)

    async def process_row(self, row: Row) -> Union[CardResponse, None]:
        word = row["word"]
        language = row["language"]
        category = row.get("category") or "general"
        if category == "general":
            self.__logger.warning(f"Using default category for word: {word}")

        try:
            if await self.__cache_strategy.read(key=word):
                self.__logger.debug(f"Word data already in the cache: {word}")
                return

            completion = self.__open_ai_client.beta.chat.completions.parse(
                model=self.__env.openai.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a polyglot language expert with over 10 years of experience in linguistics, translation, and cross-linguistic analysis.",
                    },
                    {
                        "role": "user",
                        "content": f"Could you provide the definition of the word '{word}' in {language}, when it functions as a {category}? Please include any relevant nuances, usage examples, and cultural or contextual insights, if applicable.",
                    },
                ],
                response_format=CardResponse,
            )
            data = completion.choices[0].message.parsed
            await self.__cache_strategy.write(key=word, value=word)
            return data
        except Exception as e:
            self.__logger.error(
                f"Error processing row: {row}, Error: {e}",
                self.process_row.__name__,
            )
            raise

    async def process_csv(self, file_name: str) -> None:
        df = read_csv(file_name, delimiter=",")

        words_data: List[CardResponse] = []
        for index, row in df.iterrows():
            try:
                card_response = await self.process_row(
                    cast(Row, row.to_dict())
                )
                if card_response:
                    words_data.append(card_response)
            except Exception as e:
                self.__logger.error(f"Skipping row {index} due to error: {e}")
                continue

        transformed_words: List[Word] = []
        for card_response in words_data:
            try:
                self.__logger.debug(f"WORD: {card_response.word}")
                transformed_word = await self.__transform_card(card_response)
                transformed_words.append(transformed_word)
            except Exception as e:
                self.__logger.error(f"Failed to transform card response: {e}")
                continue

        self.process_cards(transformed_words)
