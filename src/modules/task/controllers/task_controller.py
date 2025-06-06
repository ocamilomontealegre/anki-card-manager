from injector import inject
from fastapi import APIRouter
from ..services.task_service import TaskService


class TaskController:
    @inject
    def __init__(self, task_service: TaskService) -> None:
        self._router = APIRouter()
        self._task_service = task_service
        self._register_routes()

    def _register_routes(self):
        @self._router.get("/{id}")
        async def get_task_by_id(id: str):
            return self._task_service.get_task_by_id(id)

    def get_router(self) -> APIRouter:
        return self._router
