from celery.result import AsyncResult

from common.mq.celery import celery_app

from ..models.dto.task_dto import TaskDto


class TaskService:
    def get_task_by_id(self, id: str):
        result = AsyncResult(id=id, app=celery_app)

        if not result.id:
            raise ValueError(f"Task[{id}] not found")

        return TaskDto(id=result.id, status=result.status)
