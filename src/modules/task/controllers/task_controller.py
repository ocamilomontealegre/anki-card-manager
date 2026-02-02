from fastapi import APIRouter
from injector import inject

from common.enums import AppEndpoints

from ..models.dto.task_dto import TaskDto
from ..services.task_service import TaskService


class TaskController:
    @inject
    def __init__(self, task_service: TaskService) -> None:
        self._router = APIRouter(prefix=AppEndpoints.TASK.value, tags=["Task"])
        self._task_service = task_service
        self._register_routes()

    def _register_routes(self):
        @self._router.get("/{id}", response_model=TaskDto)
        async def get_task_by_id(id: str):
            return self._task_service.get_task_by_id(id)

    def get_router(self) -> APIRouter:
        return self._router
