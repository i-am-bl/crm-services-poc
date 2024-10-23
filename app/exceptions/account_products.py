from ..constants.messages import (ACCCOUNT_PRODUCTS_EXISTS,
                                  ACCCOUNT_PRODUCTS_NOT_EXIST)
from .crm_exceptions import CRMExceptions


class AccProductstNotExist(CRMExceptions):
    def __init__(
        self, message: str = ACCCOUNT_PRODUCTS_NOT_EXIST, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)


class AccProductsExists(CRMExceptions):
    def __init__(
        self, message: str = ACCCOUNT_PRODUCTS_EXISTS, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)
