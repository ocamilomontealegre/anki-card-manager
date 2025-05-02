from injector import Module, Binder, singleton
from .services.cache_service import CacheService


class CacheModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(CacheService, to=CacheService, scope=singleton)
