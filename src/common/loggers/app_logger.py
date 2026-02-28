import sys
from inspect import currentframe
from os import getpid
from typing import Literal

from loguru import logger

from common.decorators.singleton_decorator import singleton

from .models.abstracts.logger_abstract import Logger
from .models.enums.ansi_colors_enum import ANSIColors


def add_file_context(log_func):
    def wrapper(self, message: str, *args, **kwargs):
        frame = currentframe()
        if frame is not None and frame.f_back is not None:
            frame = frame.f_back
            file = frame.f_code.co_filename.split("/")[-1]
            method = frame.f_code.co_name
        else:
            file = "Unknown"
            method = "Unknown"
        return log_func(self, message, file=file, method=method, *args, **kwargs)

    return wrapper


@singleton
class AppLogger(Logger):
    def __init__(self, log_level="DEBUG", label="App"):
        self._configure_logger(log_level)

    def _configure_logger(self, log_level):
        logger.remove()
        self._logger = logger.bind(pid=getpid())
        self._set_console_logging(log_level=log_level)
        self._set_file_logging()

    def _format_log(self, record, type: Literal["console", "file"]):
        extra = record["extra"]
        pid = extra.get("pid")
        file = extra.get("file", "App")
        method = extra.get("method", "App")
        time = record["time"].strftime("%b-%d-%y %H:%M:%S")

        if type == "console":
            return (
                f"{ANSIColors.YELLOW.value}[FastAPI] {pid} | {ANSIColors.RESET.value}"
                f"{ANSIColors.WHITE.value}{time}{ANSIColors.RESET.value}"
                f"{ANSIColors.YELLOW.value} | [{file}:{method}] | {ANSIColors.RESET.value}"
                "<level>{level}</level>: <level>{message}</level>\n"
            )
        else:
            return (
                f"[FastAPI] {pid} | {time} | [{file}:{method}] "
                "<level>{level}</level>: <level>{message}</level>"
            )

    def _set_console_logging(self, log_level):
        """Configure console logging."""

        logger.add(
            sys.stderr,
            format=lambda record: self._format_log(record, type="console"),
            colorize=True,
            level=log_level,
            enqueue=True,
        )

    def _set_file_logging(self):
        """Configure file logging with rotation, retention, and compression."""
        logger.add(
            "logs/app.log",
            rotation="1 MB",
            retention="5 days",
            compression="zip",
            format=lambda record: self._format_log(record, type="file"),
            enqueue=True,
            catch=True,
        )

    def _format_context(
        self, file: str | None = None, method: str | None = None
    ) -> dict[str, str]:
        return {
            "file": str(file) if file else "Unknown",
            "method": str(method) if method else "App",
        }

    @add_file_context
    def debug(
        self,
        message: str,
        *,
        file: str | None = None,
        method: str | None = None,
    ) -> None:
        extra = self._format_context(file, method)
        self._logger.bind(**extra).debug(message)

    @add_file_context
    def info(
        self,
        message: str,
        *,
        file: str | None = None,
        method: str | None = None,
    ) -> None:
        extra = self._format_context(file, method)
        self._logger.bind(**extra).info(message)

    @add_file_context
    def warning(
        self,
        message: str,
        *,
        file: str | None = None,
        method: str | None = None,
    ) -> None:
        extra = self._format_context(file, method)
        self._logger.bind(**extra).warning(message)

    @add_file_context
    def error(
        self,
        message: str,
        *,
        file: str | None = None,
        method: str | None = None,
    ) -> None:
        extra = self._format_context(file, method)
        self._logger.bind(**extra).error(message)

    @add_file_context
    def critical(
        self,
        message: str,
        *,
        file: str | None = None,
        method: str | None = None,
    ) -> None:
        extra = self._format_context(file, method)
        self._logger.bind(**extra).exception(message)
