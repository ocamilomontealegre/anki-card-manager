from pydantic import BaseModel
from ..enums.language_enum import Language


class Row(BaseModel):
    language: str
    word: Language
