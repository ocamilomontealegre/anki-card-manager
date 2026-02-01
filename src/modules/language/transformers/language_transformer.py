from pathlib import Path
from re import IGNORECASE, escape, sub
from typing import Literal

from injector import inject

from common.enums.language_enum import Language
from common.enums.word_category_enum import WordCategory
from common.env.env_config import EnvVariables
from common.loggers.models.abstracts.logger_abstract import Logger
from common.utils import GoogleUtils
from modules.scraper.services.scraper_service import ScraperService
from modules.word.models.entities.word_entity import Word

from ..models.interfaces.card_response_interfaces.card_response_interface import (
    CardResponseBase,
)


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

        valid_word_forms = [word for word in text if word != ""]
        if len(valid_word_forms) == 0:
            return ""

        first_word = valid_word_forms[0].capitalize()
        if len(valid_word_forms) == 1:
            return first_word

        return ", ".join([first_word] + valid_word_forms[1:])

    def _get_audio_path(
        self, word: str, prefix: Literal["", "plural", "singular", "conjugations"] = ""
    ) -> str:
        full_prefix = f"{prefix}_" if prefix else ""

        return f"{self._env.anki.media}/{full_prefix}{word}.mp3"

    def _check_word_forms(self, base_word: str, word_forms: str | None) -> str:
        if word_forms and word_forms != ", " and word_forms != "":
            return word_forms[:-1] if word_forms[-1] == "," else word_forms
        else:
            return f"{base_word[0].upper()}{base_word[1:]}"

    def _escape_word(
        self,
        text: str,
        *,
        word_forms: list[str],
        type: Literal["simple", "compound"],
    ) -> str:
        cleaned_word_forms = [
            word[3:] if word.startswith("to ") else word for word in word_forms
        ]

        filtered_words = [w for w in cleaned_word_forms if w and w.strip()]
        if not filtered_words:
            return text
        sorted_words = sorted(filtered_words, key=len, reverse=True)

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

    def __get_word_forms(self, card_info: CardResponseBase):
        if (
            card_info.category.value == WordCategory.VERB.value
            and card_info.language.value == Language.ENGLISH.value
            and card_info.conjugations
        ):
            return card_info.conjugations

        if card_info.category.value == WordCategory.VERB.value:
            return [card_info.word]

        word_forms = [
            w
            for w in (
                list(card_info.forms.model_dump().values() if card_info.forms else [])
            )
            if w and w.strip()
        ]
        return word_forms

    async def to_entity(self, card_info: CardResponseBase):
        method = self.to_entity.__name__

        self._logger.debug(
            f"Transforming word[{card_info.word}]",
            file=self._file,
            method=method,
        )

        word_forms = self.__get_word_forms(card_info)

        if not word_forms:
            word_forms = [card_info.word]

        try:
            word = card_info.word
            language = card_info.language
            singular = self._capitalize_text_array(
                [
                    card_info.forms.singular_masculine,
                    card_info.forms.singular_feminine,
                ]
                if card_info.forms
                else []
            )
            plural = self._capitalize_text_array(
                [
                    card_info.forms.plural_masculine,
                    card_info.forms.plural_feminine,
                ]
                if card_info.forms
                else []
            )

            conjugations = self._capitalize_text_array(card_info.conjugations or [])
            self._logger.debug(f"{conjugations}", file="LANGUAGE_TRANSFORMER")

            word_forms = self._capitalize_text_array(word_forms)

            # images = self._scraper_service.get_image_url(
            #     {"query": word, "source": "google"}
            # )

            sentence_path = await GoogleUtils.synthetize_text(
                text=card_info.sentence.replace("[", "").replace("]", ""),
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

            conjugations_audio_path = ""
            if len(conjugations) > 0:
                conjugations_audio_path = await GoogleUtils.synthetize_text(
                    text=conjugations,
                    language=language,
                    output_file=Path(
                        self._get_audio_path(word=word, prefix="conjugations")
                    ),
                )

            new_word = Word(
                word=self._check_word_forms(word, word_forms),
                language=language.value,
                category=card_info.category.value,
                usage=card_info.usage.value,
                frequency_rank=card_info.frequency_rank,
                definition=card_info.definition.capitalize().rstrip(),
                sentence=card_info.sentence,
                phonetics=card_info.sentence_phonetics.replace("[", "")
                .replace("]", "")
                .rstrip(),
                sentence_audio=sentence_path,
                partial_sentence=card_info.partial_sentence.rstrip(),
                singular=singular,
                singular_audio=singular_audio_path,
                plural=plural,
                plural_audio=plural_audio_path,
                conjugations=self._capitalize_text_array(card_info.conjugations or []),
                conjugations_audio=conjugations_audio_path,
                image="",
            )
            return new_word
        except Exception as e:
            self._logger.error(
                f"Error transforming card: {e}",
                file=self._file,
                method=method,
            )
            raise
