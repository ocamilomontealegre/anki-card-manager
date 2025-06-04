from typing import Optional
from pydantic import BaseModel
from modules.language.models.enums import Language, WordCategory


class FindAllParams(BaseModel):
    limit: Optional[int] = None
    offset: Optional[int] = None
    sort: Optional[str] = None
    word: Optional[str] = None
    category: Optional[WordCategory] = None
    language: Optional[Language] = None
