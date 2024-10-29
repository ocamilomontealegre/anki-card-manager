from injector import Module, Binder, singleton
from health.controllers.health_controller import HealthController
from health.services.health_service import HealthService


class HealthModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(HealthController, to=HealthController, scope=singleton)
        binder.bind(HealthService, to=HealthService, scope=singleton)
