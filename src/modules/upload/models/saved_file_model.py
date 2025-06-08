from typing import Union
from pydantic import BaseModel


class SavedFile(BaseModel):
    name: str
    file_path: str
    size: Union[int, None]
    content_type: Union[str, None]
