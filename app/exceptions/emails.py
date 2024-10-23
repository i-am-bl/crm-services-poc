from ..constants.messages import EMAIL_EXISTS, EMAIL_NOT_EXIST
from .crm_exceptions import CRMExceptions


class EmailNotExist(CRMExceptions):
    def __init__(self, message: str = EMAIL_NOT_EXIST, *args: object, **kwargs) -> None:
        super().__init__(message, *args, **kwargs)


class EmailExists(CRMExceptions):
    def __init__(self, message: str = EMAIL_EXISTS, *args: object, **kwargs) -> None:
        super().__init__(message, *args, **kwargs)
