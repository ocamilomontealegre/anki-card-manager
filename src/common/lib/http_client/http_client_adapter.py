from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Literal, TypeVar

T = TypeVar("T")

HttpMethod = Literal["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]

@dataclass
class HttpOptions:
    method: HttpMethod
    headers: dict[str, str] | None = None
    body: dict[str, object] | None = None
    query_params: dict[str, str] | None = None
    timeout: float | None = None


class HttpClientAdapter(ABC):
    @abstractmethod
    async def request(
        self, url: str, *, http_options: HttpOptions, response_model: type[T] | None = None
    ) -> T:
        pass
