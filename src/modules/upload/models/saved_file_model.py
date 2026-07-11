from pydantic import BaseModel


class SavedFile(BaseModel):
    name: str
    file_path: str
    size: int | None
    content_type: str | None
