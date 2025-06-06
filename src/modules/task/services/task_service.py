from injector import inject
from celery.result import AsyncResult
from common.mq.celery import celery_app


class TaskService:
    @inject
    def __init__(self) -> None:
        pass

    def get_task_by_id(self, id: str):
        result = AsyncResult(id=id, app=celery_app)

        return {
            "id": id,
            "status": result.status,
            "result": result.result if result.ready() else None,
        }
