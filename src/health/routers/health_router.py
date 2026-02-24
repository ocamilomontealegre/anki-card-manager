from fastapi import APIRouter

from health.controllers.health_controller import HealthController


class HealthRouter:
    def __init__(self, health_controller: HealthController):
        self._health_controller = health_controller

        self._router = APIRouter()
        self._register_routes()

    @property
    def router(self) -> APIRouter:
        return self._router

    def _register_routes(self) -> None:
        self._router.add_api_route(
            "/",
            self._health_controller.check,
            methods=["GET"],
        )