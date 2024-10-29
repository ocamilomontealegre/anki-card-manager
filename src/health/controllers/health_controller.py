from fastapi import APIRouter
from injector import inject
from health.services.health_service import HealthService
from health.models.health_message_model import HealthMessage


class HealthController:
    @inject
    def __init__(self, health_service: HealthService):
        self._health_service = health_service
        self._router = APIRouter()
        self._register_routes()

    def _register_routes(self):
        @self._router.get(
            "",
            response_model=HealthMessage,
            tags=["Health"],
            summary="Check application status",
            description="Check the availability of the server",
        )
        async def check() -> HealthMessage:
            return self._health_service.check()

    def get_router(self) -> APIRouter:
        return self._router
