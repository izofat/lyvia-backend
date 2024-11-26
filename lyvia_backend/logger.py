import logging
import sys
import traceback
from typing import Optional


class Logger:
    logger = logging.getLogger(__name__)
    logger.propagate = False

    if not logger.handlers:
        formatter = logging.Formatter("%(asctime)s - %(message)s")
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        logger.setLevel(logging.INFO)

    @classmethod
    def info(cls, message: str, *args) -> None:
        cls.logger.info(message, *args)

    @classmethod
    def warning(cls, message: str, *args) -> None:
        cls.logger.warning(message, *args)

    @classmethod
    def debug(cls, message: str, *args) -> None:
        cls.logger.debug(message, *args)

    @classmethod
    def critical(cls, message: str, *args) -> None:
        cls.logger.critical(message, *args)

    @classmethod
    def error(cls, exception: Exception, message: Optional[str] = None) -> None:
        error_traceback = traceback.format_exc()
        error_message = f"{message}: {str(exception)}" if message else str(exception)
        cls.logger.error(
            "Exception occurred: %s\nTraceback: %s", error_message, error_traceback
        )
