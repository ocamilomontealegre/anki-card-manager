import sys
from os import getpid
from typing import Optional, Dict, Literal

from loguru import logger

from common.decorators.singleton_decorator import singleton
from .models.abstracts.logger_abstract import Logger
from .models.enums.ansi_colors_enum import ANSIColors


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
                "<level>{level}</level>: <level>{message}</level>"
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
        self, file: str, method: Optional[str] = None
    ) -> Dict[str, str]:
        return {
            "file": str(file),
            "method": str(method) if method else "App",
        }

    def debug(
        self,
        message: str,
        *,
        file: str,
        method: Optional[str] = None,
    ) -> None:
        extra = self._format_context(file, method)
        self._logger.bind(**extra).debug(message)

    def info(
        self,
        message: str,
        *,
        file: str,
        method: Optional[str] = None,
    ) -> None:
        extra = self._format_context(file, method)
        self._logger.bind(**extra).info(message)

    def warning(
        self,
        message: str,
        *,
        file: str,
        method: Optional[str] = None,
    ) -> None:
        extra = self._format_context(file, method)
        self._logger.bind(**extra).warning(message)

    def error(
        self,
        message: str,
        *,
        file: str,
        method: Optional[str] = None,
    ) -> None:
        extra = self._format_context(file, method)
        self._logger.bind(**extra).error(message)

    def critical(
        self,
        message: str,
        *,
        file: str,
        method: Optional[str] = None,
    ) -> None:
        extra = self._format_context(file, method)
        self._logger.bind(**extra).critical(message)
