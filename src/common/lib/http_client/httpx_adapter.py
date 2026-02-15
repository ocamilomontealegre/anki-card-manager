from typing import TypeVar

from httpx import AsyncClient

from common.lib.http_client.http_client_adapter import HttpClientAdapter, HttpOptions

T = TypeVar("T")


class HttpxAdapter(HttpClientAdapter):
    async def request(
        self,
        url: str,
        *,
        http_options: HttpOptions,
        response_model: type[T] | None = None,
    ) -> T:
        async with AsyncClient() as client:
            response = await client.request(
                http_options.method,
                url,
                params=http_options.query_params,
                headers=http_options.headers,
                timeout=http_options.timeout,
            )

            response.raise_for_status()

            data = response.json()

            if response_model:
                return response_model(**data[0])

            return data