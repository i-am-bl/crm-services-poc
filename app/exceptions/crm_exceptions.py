from typing import Optional

from ..utilities.logger import logger


class CRMExceptions(Exception):
    """Base class for all exceptions"""

    def __init__(self, message: Optional[str] = None, *args: object, **kwargs) -> None:
        super().__init__(message, *args, **kwargs)
        if message:
            self.log_exception(message=message)

    def log_exception(self, message):
        logger.warning(f"{self.__class__.__name__}: {message}")
