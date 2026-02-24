from injector import inject

from common.enums import MqTaskStatus
from common.models import TaskResponse
from modules.anki.tasks.anki_task import process_anki_cards
from modules.word.models.interfaces.list_params import ListParams


class AnkiController:
    @inject
    async def process(self, params: ListParams):
        task = process_anki_cards.delay(params=params.model_dump())  # type: ignore
        return TaskResponse(task_id=task.id, status=MqTaskStatus.PENDING)
