from pydantic import BaseModel
from common.enums import MqTaskStatus


class TaskResponse(BaseModel):
    task_id: str
    status: MqTaskStatus
