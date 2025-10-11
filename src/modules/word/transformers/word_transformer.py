from os import path
from typing import Optional
from datetime import datetime

from pydantic import BaseModel
from injector import inject

from common.enums import WordCategory
from ..models.entities.word_entity import Word


class WordSchema(BaseModel):
    id: str
    word: str
    category: str
    definition: str
    sentence: str
    phonetics: str
    sentence_audio: str
    partial_sentence: str
    singular: Optional[str] = None
    singular_audio: Optional[str] = None
    plural: Optional[str] = None
    plural_audio: Optional[str] = None
    synonyms: Optional[str] = None
    image: str
    image_2: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

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
            category=WordCategory(word_dict.category.lower()).value.capitalize(),
            definition=word_dict.definition,
            sentence=word_dict.sentence,
            sentence_audio=self._format_audio_path(word_dict.sentence_audio),
            phonetics=f"/{word_dict.phonetics}/",
            partial_sentence=word_dict.partial_sentence,
            singular=word_dict.singular or "",
            singular_audio=self._format_audio_path(word_dict.singular_audio or ""),
            plural=word_dict.plural or "",
            plural_audio=self._format_audio_path(word_dict.plural_audio or ""),
            synonyms=word_dict.synonyms or "",
            image=path.basename(word_dict.image),
            image_2=path.basename(word_dict.image_2 or ""),
        )
