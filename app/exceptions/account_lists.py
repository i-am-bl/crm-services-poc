from ..constants.messages import ACCCOUNT_LIST_EXISTS, ACCCOUNT_LIST_NOT_EXIST
from .crm_exceptions import CRMExceptions


class AccListNotExist(CRMExceptions):
    def __init__(
        self, message: str = ACCCOUNT_LIST_NOT_EXIST, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)


class AccListExists(CRMExceptions):
    def __init__(
        self, message: str = ACCCOUNT_LIST_EXISTS, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)
