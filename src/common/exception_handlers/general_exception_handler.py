from fastapi import Request
from fastapi.responses import JSONResponse
from common.loggers.app_logger import AppLogger
from common.utils import ExceptionUtils
from common.models import HTTPResponse
from common.constants import STATUS_MESSAGES


class GeneralExceptionHandler:
    @staticmethod
    async def handle_exception(
        request: Request, exc: Exception
    ) -> JSONResponse:
        file = GeneralExceptionHandler.__name__
        logger = AppLogger()

        exception_details = ExceptionUtils.extract_details(exc)

        response = HTTPResponse(
            status=500,
            success=False,
            message=STATUS_MESSAGES[500],
        )

        logger.error(
            f"[INCOMING REQUEST] METHOD: {request.method} | URL: {request.url.path} | HEADERS: {request.headers} "
            f"[OUTGOING RESPONSE] STATUS: {response.status} | RESPONSE_BODY: {response} | EXCEPTION: {exception_details}",
            file=file,
            method=GeneralExceptionHandler.handle_exception.__name__,
        )

        return JSONResponse(content=response.model_dump(), status_code=500)
