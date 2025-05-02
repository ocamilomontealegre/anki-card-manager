from injector import Module, Binder, singleton
from .strategies.cache_strategy import CacheStrategy
from .strategies.redis_strategy import RedisStrategy


class CacheModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(CacheStrategy, to=RedisStrategy, scope=singleton)
