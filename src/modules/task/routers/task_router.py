from fastapi import APIRouter
from injector import inject

from common.enums.app_endpoints_enum import AppEndpoints
from modules.task.controllers.task_controller import TaskController
from modules.task.models.dto.task_dto import TaskDto


class TaskRouter:
    @inject
    def __init__(self, task_controller: TaskController):
        self._router = APIRouter(prefix=AppEndpoints.TASK.value, tags=["Task"])
        self._task_controller = task_controller
        self._register_routes()

    @property
    def router(self) -> APIRouter:
        return self._router

    def _register_routes(self) -> None:
        self._router.add_api_route(
            "/{id}",
            self._task_controller.get_task_by_id,
            methods=["GET"],
            response_model=TaskDto,
        )
