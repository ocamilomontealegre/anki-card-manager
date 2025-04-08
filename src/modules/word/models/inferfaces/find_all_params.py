from typing import Optional
from pydantic import BaseModel
from modules.language.models.enums.language_enum import Language


class FindAllParams(BaseModel):
    word: Optional[str] = None
    category: Optional[str] = None
    language: Optional[Language] = None
