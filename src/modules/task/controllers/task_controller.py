from injector import inject
from fastapi import APIRouter
from celery.result import AsyncResult


class TaskController:
    @inject
    def __init__(self) -> None:
        self.__router = APIRouter()
        self.__register_routes()

    def __register_routes(self):
        @self.__router.get("")
        async def get_task(task_id: str):
            return AsyncResult(id=task_id)

    def get_router(self) -> APIRouter:
        return self.__router
