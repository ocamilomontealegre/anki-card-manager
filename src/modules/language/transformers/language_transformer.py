from pathlib import Path
from re import escape, sub
from typing import Literal, Optional, List

from injector import inject

from common.loggers.models.abstracts.logger_abstract import Logger
from common.utils import GoogleUtils, ImageUtils
from common.env.env_config import EnvVariables
from modules.scraper.services.scraper_service import ScraperService
from modules.word.models.entities.word_entity import Word
from ..models.interfaces.card_response_interface import CardResponse


class LanguageTransformer:

    @inject
    def __init__(self, scraper_service: ScraperService, logger: Logger):
        self._file = LanguageTransformer.__name__

        self._scraper_service = scraper_service

        self._logger = logger
        self._env = EnvVariables.get()

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

    def _scape_word(
        self,
        text: str,
        *,
        word_forms: List[str],
        type: Literal["simple", "compound"],
    ) -> str:
        pattern = r"\b(" + "|".join(escape(w) for w in word_forms) + r")\b"

        if type == "simple":
            return sub(pattern, "{...}", text)
        else:
            return sub(pattern, lambda m: f"[{m.group(0)}]", text)

    async def to_entity(self, card_info: CardResponse):
        method = self.to_entity.__name__

        self._logger.debug(
            f"Transforming word[{card_info.word}]",
            file=self._file,
            method=method,
        )

        try:
            word = card_info.word
            language = card_info.language
            plural = self._capitalize_text_array(card_info.plural)
            singular = self._capitalize_text_array(card_info.singular)
            synonyms = self._capitalize_text_array(card_info.synonyms)

            sentence = self._scape_word(
                card_info.sentence,
                word_forms=card_info.singular + card_info.plural,
                type="compound",
            )
            partial_sentence = self._scape_word(
                card_info.sentence,
                word_forms=card_info.singular + card_info.plural,
                type="simple",
            )

            word_forms = self._capitalize_text_array(
                card_info.singular + card_info.plural
            )

            images = self._scraper_service.get_image_url(
                {"query": word, "source": "google"}
            )

            sentence_path = await GoogleUtils.synthetize_text(
                text=card_info.sentence,
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
                        "url": images[0],
                        "word": word,
                        "source": self._env.anki.media,
                    }
                )
                or "",
                image_2=await ImageUtils.download_from_url(
                    {
                        "url": images[1],
                        "word": word,
                        "source": self._env.anki.media,
                    }
                )
                or "",
            )
            return new_word
        except Exception as e:
            self._logger.error(
                f"Error transforming card: {e}",
                file=self._file,
                method=method,
            )
            raise
