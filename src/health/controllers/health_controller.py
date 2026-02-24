from injector import inject

from health.models.abstracts.health_service_abstract import HealthService
from health.models.dto.health_message_dto import HealthMessageDto


class HealthController:
    @inject
    def __init__(self, health_service: HealthService):
        self._health_service = health_service

    async def check(self):
        return HealthMessageDto(message=self._health_service.check())
