from ..constants.messages import (ACCCOUNT_CONTRACT_EXISTS,
                                  ACCCOUNT_CONTRACT_NOT_EXIST)
from .crm_exceptions import CRMExceptions


class AccContractNotExist(CRMExceptions):
    def __init__(
        self, message: str = ACCCOUNT_CONTRACT_NOT_EXIST, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)


class AccContractExists(CRMExceptions):
    def __init__(
        self, message: str = ACCCOUNT_CONTRACT_EXISTS, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)
