from pathlib import Path
from re import escape, sub
from typing import Literal, Optional, List

from injector import inject

from common.loggers.logger import AppLogger
from common.utils import GoogleUtils, ImageUtils
from common.env.env_config import get_env_variables
from modules.scraper.services.scraper_service import ScraperService
from modules.word.models.entities.word_entity import Word
from ..models.interfaces.card_response_interface import CardResponse


class LanguageTransformer:

    @inject
    def __init__(self, scraper_service: ScraperService):
        self._scraper_service = scraper_service

        self._logger = AppLogger(label=LanguageTransformer.__name__)
        self._env = get_env_variables()

    def _capitalize_text_array(self, text: List[str]) -> str:
        if len(text) == 0:
            return ""

        first_word = text[0].capitalize()
        if len(text) == 1:
            return first_word

        return ", ".join([first_word] + text[1:])

    def _get_audio_path(
        self, word: str, prefix: Literal["", "plural", "singular"] = ""
    ) -> str:
        full_prefix = f"{prefix}_" if prefix else ""

        return f"{self._env.anki.media}/{full_prefix}{word}.mp3"

    def _check_word_forms(
        self, base_word: str, word_forms: Optional[str]
    ) -> str:
        if word_forms and word_forms != ", ":
            return word_forms[:-1] if word_forms[-1] == "," else word_forms
        else:
            return f"{base_word[0].upper()}{base_word[1:]}"

    async def to_entity(self, card_info: CardResponse):
        self._logger.debug(
            f"Transforming word[{card_info.word}]",
            self.to_entity.__name__,
        )

        try:
            word = card_info.word
            language = card_info.language
            plural = self._capitalize_text_array(card_info.plural)
            singular = self._capitalize_text_array(card_info.singular)
            synonyms = self._capitalize_text_array(card_info.synonyms)
            sentence = sub(
                rf"\b{escape(word)}\b", f"[{word}]", card_info.sentence
            )
            partial_sentence = sub(
                rf"\b{escape(word)}\b", "{...}", card_info.sentence
            )
            word_forms = self._capitalize_text_array(
                card_info.singular + card_info.plural
            )

            giphy_image_url = await self._scraper_service.get_image_url(
                {"query": word, "target_language": language, "source": "giphy"}
            )

            pinterest_image_url = await self._scraper_service.get_image_url(
                {
                    "query": word,
                    "target_language": language,
                    "source": "pinterest",
                }
            )

            sentence_path = await GoogleUtils.synthetize_text(
                text=sentence,
                language=language,
                output_file=Path(self._get_audio_path(word=word)),
            )

            plural_audio_path = ""
            if len(plural) > 0:
                plural_audio_path = await GoogleUtils.synthetize_text(
                    text=plural,
                    language=language,
                    output_file=Path(
                        self._get_audio_path(word=word, prefix="plural")
                    ),
                )

            singular_audio_path = ""
            if len(singular) > 0:
                singular_audio_path = await GoogleUtils.synthetize_text(
                    text=singular,
                    language=language,
                    output_file=Path(
                        self._get_audio_path(word=word, prefix="singular")
                    ),
                )

            new_word = Word(
                word=self._check_word_forms(word, word_forms),
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
                image=await ImageUtils.download_from_url(
                    {
                        "url": giphy_image_url,
                        "word": word,
                        "source": self._env.anki.media,
                    }
                ),
                image_2=await ImageUtils.download_from_url(
                    {
                        "url": pinterest_image_url,
                        "word": word,
                        "source": self._env.anki.media,
                    }
                ),
            )
            return new_word
        except Exception as e:
            self._logger.error(
                f"Error transforming card: {e}", self.to_entity.__name__
            )
            raise
