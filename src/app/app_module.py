from injector import Binder, Module
from health.health_module import HealthModule


class AppModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.install(HealthModule())
