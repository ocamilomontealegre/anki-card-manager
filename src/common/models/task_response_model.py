from pydantic import BaseModel
from src.common.enums import MqTaskStatus


class TaskResponse(BaseModel):
    task_id: str
    status: MqTaskStatus
