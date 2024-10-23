from ..constants.messages import NUMBER_EXISTS, NUMBER_NOT_EXIST
from .crm_exceptions import CRMExceptions


class NumbersNotExist(CRMExceptions):
    def __init__(
        self, message: str = NUMBER_NOT_EXIST, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)


class NumberExists(CRMExceptions):
    def __init__(self, message: str = NUMBER_EXISTS, *args: object, **kwargs) -> None:
        super().__init__(message, *args, **kwargs)
