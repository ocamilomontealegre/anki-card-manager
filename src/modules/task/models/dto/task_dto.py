from pydantic import BaseModel
from common.enums import MqTaskStatus


class TaskDto(BaseModel):
    id: str
    status: MqTaskStatus
