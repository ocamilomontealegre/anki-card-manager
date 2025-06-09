from injector import inject
from fastapi import APIRouter
from common.enums import AppEndpoints
from health.models.abstracts.health_service_abstract import HealthService
from health.models.dto.health_message_dto import HealthMessageDto


class HealthController:
    @inject
    def __init__(self, health_service: HealthService):
        self._health_service = health_service
        self._router = APIRouter(
            prefix=AppEndpoints.HEALTH.value, tags=["Health"]
        )
        self._register_routes()

    def _register_routes(self):

        @self._router.get(
            "",
            response_model=HealthMessageDto,
            summary="Check application status",
            description="Check the availability of the server",
        )
        async def check():
            return HealthMessageDto(message=self._health_service.check())

    def get_router(self) -> APIRouter:
        return self._router
