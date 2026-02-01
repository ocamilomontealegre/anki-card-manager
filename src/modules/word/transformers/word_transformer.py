from datetime import datetime
from os import path

from injector import inject
from pydantic import BaseModel

from common.enums import Language, Usage, WordCategory

from ..models.entities.word_entity import Word


class WordSchema(BaseModel):
    id: str
    word: str
    language: str
    category: str
    usage: str
    frequency_rank: int | str
    definition: str
    sentence: str
    phonetics: str
    sentence_audio: str
    partial_sentence: str
    singular: str | None = None
    singular_audio: str | None = None
    plural: str | None = None
    plural_audio: str | None = None
    conjugations: str | None = None
    conjugations_audio: str | None = None
    image: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}


class WordTransformer:
    @inject
    def __init__(self):
        # This constructor is intentionally left empty because
        pass

    def _format_audio_path(self, audio_path: str) -> str:
        return f"[sound:{path.basename(audio_path)}]" if audio_path else ""

    def transform(self, word: Word) -> WordSchema:
        word_dict = WordSchema.model_validate(word)

        return WordSchema(
            id=word_dict.id,
            word=word_dict.word,
            language=Language(word_dict.language).value.capitalize(),
            category=WordCategory(word_dict.category.lower()).value.capitalize(),
            usage=Usage(word_dict.usage).value,
            frequency_rank=str(word_dict.frequency_rank),
            definition=word_dict.definition,
            sentence=word_dict.sentence,
            sentence_audio=self._format_audio_path(word_dict.sentence_audio),
            phonetics=f"/{word_dict.phonetics}/",
            partial_sentence=word_dict.partial_sentence,
            singular=word_dict.singular or "",
            singular_audio=self._format_audio_path(word_dict.singular_audio or ""),
            plural=word_dict.plural or "",
            plural_audio=self._format_audio_path(word_dict.plural_audio or ""),
            conjugations=word_dict.conjugations,
            conjugations_audio=self._format_audio_path(
                word_dict.conjugations_audio or ""
            ),
            image=path.basename(word_dict.image),
        )
