from typing import Optional
from pydantic import BaseModel
from modules.language.models.enums.language_enum import Language


class FindAllParams(BaseModel):
    limit: Optional[int] = None
    offset: Optional[int] = None
    sort: Optional[str] = None
    word: Optional[str] = None
    category: Optional[str] = None
    language: Optional[Language] = None
