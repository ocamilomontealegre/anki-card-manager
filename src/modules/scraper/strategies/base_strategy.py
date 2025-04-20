from abc import ABC, abstractmethod


class BaseStrategy(ABC):
    @abstractmethod
    def get_image_url(self, query: str) -> str:
        pass
