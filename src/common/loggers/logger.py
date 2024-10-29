import sys
from os import getpid
from loguru import logger
from .enums.ansi_colors_enum import ANSIColors


class AppLogger:
    def __init__(self, log_level="DEBUG", label="App"):
        self.logger = logger.bind(label=label)
        self._configure_logger(log_level)

    def _configure_logger(self, log_level):
        logger.remove()
        self._set_console_logging(log_level=log_level)
        self._set_file_logging()
        self.logger = self.logger.bind(pid=getpid())

    def _set_console_logging(self, log_level):
        """Configure console logging."""
        logger.add(
            sys.stderr,
            format=(
                f"{ANSIColors.YELLOW.value}[FastAPI] {{extra[pid]}} | {ANSIColors.RESET.value}"
                f"{ANSIColors.WHITE.value}{{time:MMM-DD-YY HH:mm:ss}} | {ANSIColors.RESET.value}"
                f"{ANSIColors.YELLOW.value}[{{extra[label]}}] | {ANSIColors.RESET.value}"
                "<level>{level}</level>: <level>{message}</level>"
            ),
            colorize=True,
            level=log_level,
        )

    def _set_file_logging(self):
        """Configure file logging with rotation, retention, and compression."""
        logger.add(
            "logs/app.log",
            rotation="1 MB",
            retention="5 days",
            compression="zip",
            format=(
                "[FastAPI] {extra[pid]} | {time:MMM-DD-YY HH:mm:ss} | [{extra[label]}] | "
                "<level>{level}</level>: <level>{message}</level>"
            ),
        )

    def debug(self, message):
        self.logger.debug(f"🐛 {message}")

    def info(self, message):
        self.logger.info(f"📄 {message}")

    def warning(self, message):
        self.logger.warning(f"⚠️ {message}")

    def error(self, message):
        self.logger.error(f"❌ {message}")

    def critical(self, message):
        self.logger.critical(f"💥 {message}")

    def set_level(self, level):
        self._configure_logger(level)
