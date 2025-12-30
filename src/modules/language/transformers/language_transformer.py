from pathlib import Path
from re import IGNORECASE, escape, sub
from typing import Literal

from injector import inject

from common.env.env_config import EnvVariables
from common.loggers.models.abstracts.logger_abstract import Logger
from common.utils import GoogleUtils
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

    def _capitalize_text_array(self, text: list[str]) -> str:
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

    def _check_word_forms(self, base_word: str, word_forms: str | None) -> str:
        if word_forms and word_forms != ", ":
            return word_forms[:-1] if word_forms[-1] == "," else word_forms
        else:
            return f"{base_word[0].upper()}{base_word[1:]}"

    def _scape_word(
        self,
        text: str,
        *,
        word_forms: list[str],
        type: Literal["simple", "compound"],
    ) -> str:
        sorted_words = sorted(word_forms, key=len, reverse=True)

        pattern = r"(^|\W)(" + "|".join(escape(w) for w in sorted_words) + r")(\W|$)"

        if type == "simple":
            return sub(
                pattern,
                lambda m: f"{m.group(1)}{{...}}{m.group(3)}",
                text,
                flags=IGNORECASE,
            )
        else:
            return sub(
                pattern,
                lambda m: f"{m.group(1)}[{m.group(2)}]{m.group(3)}",
                text,
                flags=IGNORECASE,
            )

    async def to_entity(self, card_info: CardResponse):
        method = self.to_entity.__name__

        self._logger.debug(
            f"Transforming word[{card_info.word}]",
            file=self._file,
            method=method,
        )

        word_forms = [
            w for w in (card_info.singular + card_info.plural) if w and w.strip()
        ]

        if not word_forms:
            word_forms = [card_info.word]

        try:
            word = card_info.word
            language = card_info.language
            plural = self._capitalize_text_array(card_info.plural)
            singular = self._capitalize_text_array(card_info.singular)
            synonyms = self._capitalize_text_array(card_info.synonyms)

            sentence = self._scape_word(
                card_info.sentence,
                word_forms=word_forms,
                type="compound",
            )
            partial_sentence = self._scape_word(
                card_info.sentence,
                word_forms=word_forms,
                type="simple",
            )

            word_forms = self._capitalize_text_array(word_forms)

            # images = self._scraper_service.get_image_url(
            #     {"query": word, "source": "google"}
            # )

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
                    output_file=Path(self._get_audio_path(word=word, prefix="plural")),
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
                image="",
                image_2="",
            )
            return new_word
        except Exception as e:
            self._logger.error(
                f"Error transforming card: {e}",
                file=self._file,
                method=method,
            )
            raise
