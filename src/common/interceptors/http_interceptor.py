from collections.abc import AsyncIterable, Awaitable, Callable
from json import loads

from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response
from starlette.types import ASGIApp

from common.exception_handlers import (
    GeneralExceptionHandler,
    HTTPExceptionHandler,
)
from common.loggers.app_logger import AppLogger
from common.models import HTTPResponse
from common.utils import get_status_message


class HTTPInterceptor(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self._logger = AppLogger(log_level="INFO")

    async def _format_response(
        self, body_iterator: AsyncIterable[bytes], status_code: int
    ) -> HTTPResponse:
        response_body = []
        async for section in body_iterator:
            response_body.append(section)
        response_body_str = b"".join(response_body).decode("utf-8")

        data = loads(response_body_str)
        message = get_status_message(status_code)

        return HTTPResponse(
            message=message,
            data=data,
        )

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        if request.url.path in ["/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        try:
            response = await call_next(request)

            if response.status_code < 400:
                formated_response = await self._format_response(
                    response.body_iterator,  # type: ignore
                    response.status_code,  # type: ignore
                )

                self._logger.info(
                    f"[INCOMING REQUEST] METHOD: {request.method} | URL: {request.url.path} | "
                    f"[OUTGOING RESPONSE] STATUS: {response.status_code} | RESPONSE_BODY: {formated_response.data}",
                    file=HTTPInterceptor.__name__,
                    method=self.dispatch.__name__,
                )

                return JSONResponse(
                    content=formated_response.model_dump(),
                    status_code=response.status_code,
                )

            return response
        except HTTPException as exc:
            return await HTTPExceptionHandler.handle_exception(request, exc)
        except Exception as exc:
            return await GeneralExceptionHandler.handle_exception(request, exc)
