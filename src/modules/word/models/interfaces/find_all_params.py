from pydantic import BaseModel

from common.enums import Language, WordCategory


class FindAllParams(BaseModel):
    limit: None | int = None
    offset: None | int = None
    sort: None | str = None
    word: None | str = None
    category: None | WordCategory = None
    language: None | Language = None

    class Config:
        use_enum_values = True
