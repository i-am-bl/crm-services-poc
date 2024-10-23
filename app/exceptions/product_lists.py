from ..constants.messages import PRODUCT_LIST_EXISTS, PRODUCT_LIST_NOT_EXIST
from .crm_exceptions import CRMExceptions


class ProductListNotExist(CRMExceptions):
    def __init__(
        self, message: str = PRODUCT_LIST_NOT_EXIST, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)


class ProductListExists(CRMExceptions):
    def __init__(
        self, message: str = PRODUCT_LIST_EXISTS, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)
