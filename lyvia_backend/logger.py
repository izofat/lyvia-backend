import logging
import sys
import traceback


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
    def error(cls, message: str, error: Exception) -> None:
        error_traceback = "".join(
            traceback.format_exception(type(error), error, error.__traceback__)
        )
        error_message = f"{message}: {str(error)}"
        cls.logger.error(
            "Traceback: %s \nException occurred: %s", error_traceback, error_message
        )
