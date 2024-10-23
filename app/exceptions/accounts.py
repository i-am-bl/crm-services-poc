from ..constants.messages import ACCCOUNT_EXISTS, ACCCOUNT_NOT_EXIST
from .crm_exceptions import CRMExceptions


class AccsNotExist(CRMExceptions):
    def __init__(
        self, message: str = ACCCOUNT_NOT_EXIST, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)


class AccsExists(CRMExceptions):
    def __init__(self, message: str = ACCCOUNT_EXISTS, *args: object, **kwargs) -> None:
        super().__init__(message, *args, **kwargs)
