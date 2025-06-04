from injector import inject
from fastapi import APIRouter
from pydantic import BaseModel
from ..tasks.language_task import process_csv_task


class FileRequest(BaseModel):
    file_path: str


class LanguageController:
    @inject
    def __init__(self) -> None:
        self._router = APIRouter()
        self._register_routes()

    def _register_routes(self) -> None:

        @self._router.post("/process")
        async def process_file(request: FileRequest):
            result = process_csv_task.delay(file_path=request.file_path)  # type: ignore
            return {"task_id": result.id}

    def get_router(self) -> APIRouter:
        return self._router
