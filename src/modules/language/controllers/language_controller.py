from injector import inject
from pydantic import BaseModel

from common.enums import MqTaskStatus
from common.enums.language_enum import Language
from common.enums.word_category_enum import WordCategory
from common.models import TaskResponse
from modules.language.models.interfaces.row_interface import Row
from modules.language.services.language_service import LanguageService
from modules.language.tasks.language_task import process_csv_task


class ProcessRequest(BaseModel):
    file_path: str


class WordContextRequest(BaseModel):
    word: str
    language: Language


class CreateWord(BaseModel):
    word: str
    language: Language
    category: WordCategory | None = None
    context: str | None = None
    thense: str | None = None
    person: str | None = None


class LanguageController:
    @inject
    def __init__(self, language_service: LanguageService) -> None:
        self._language_service = language_service

    async def get_word_context(self, request: WordContextRequest):
        return await self._language_service.get_word_context(
            word=request.word, language=request.language
        )

    async def create_word_entry(self, request: CreateWord):
        word: Row = {
            "word": request.word,
            "language": request.language,
            "thense": request.thense,
            "person": request.person,
        }

        if request.category is not None:
            word["category"] = request.category

        if request.context is not None:
            word["context"] = request.context

        return await self._language_service.create_word_entry(word=word)

    async def process(self, request: ProcessRequest):
        task = process_csv_task.delay(file_path=request.file_path)  # type: ignore
        return TaskResponse(task_id=task.id, status=MqTaskStatus.PENDING)
