from injector import Module, Binder, singleton
from .strategies.mq_strategy import MqStrategy
from .strategies.celery_strategy import CeleryStrategy


class MqModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(MqStrategy, to=CeleryStrategy, scope=singleton)
