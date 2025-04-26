from typing import Optional
from dataclasses import dataclass
from modules.language.models.enums import Language, WordCategory


@dataclass
class CreateCards:
    limit: Optional[int]
    offset: Optional[int]
    sort: Optional[str]
    word: Optional[str]
    category: Optional[WordCategory]
    language: Optional[Language]
