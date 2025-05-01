from loguru import logger
from datetime import datetime


class Logger:
    @staticmethod
    def info(text: str):
        logger.info(f"{text}: {datetime.now()}")

    @staticmethod
    def error(error: Exception | str):
        logger.error(f"{error}: {datetime.now()}")
