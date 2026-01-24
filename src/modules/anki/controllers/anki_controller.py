from injector import inject
from fastapi import APIRouter
from common.enums import AppEndpoints, MqTaskStatus
from common.models import TaskResponse
from modules.word.models.interfaces.find_all_params import FindAllParams
from ..tasks.anki_task import process_anki_cards


class AnkiController:
    @inject
    def __init__(self) -> None:
        self._router = APIRouter(prefix=AppEndpoints.ANKI.value, tags=["Anki"])
        self._register_routes()

    def _register_routes(self):
        @self._router.post("", response_model=TaskResponse)
        async def process(body: FindAllParams):
            task = process_anki_cards.delay(filters=body.model_dump())  # type: ignore
            return TaskResponse(task_id=task.id, status=MqTaskStatus.PENDING)

    def get_router(self) -> APIRouter:
        return self._router
