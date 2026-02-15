from injector import inject

from ..models.dto.task_dto import TaskDto
from ..services.task_service import TaskService


class TaskController:
    @inject
    def __init__(self, task_service: TaskService) -> None:
        self._task_service = task_service

    def get_task_by_id(self, id: str) -> TaskDto:
        return self._task_service.get_task_by_id(id)
