from injector import inject
from fastapi import APIRouter
from pydantic import BaseModel
from src.common.enums import AppEndpoints, MqTaskStatus
from src.common.models import TaskResponse
from ..tasks.language_task import process_csv_task


class FileRequest(BaseModel):
    file_path: str


class LanguageController:
    @inject
    def __init__(self) -> None:
        self._router = APIRouter(prefix=AppEndpoints.LANGUAGE.value, tags=["Languages"])
        self._register_routes()

    def _register_routes(self) -> None:
        @self._router.post("/process", response_model=TaskResponse)
        async def process(request: FileRequest):
            task = process_csv_task.delay(file_path=request.file_path)  # type: ignore
            return TaskResponse(task_id=task.id, status=MqTaskStatus.PENDING)

    def get_router(self) -> APIRouter:
        return self._router
