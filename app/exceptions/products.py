from ..constants.messages import PRODUCT_EXISTS, PRODUCT_NOT_EXIST
from .crm_exceptions import CRMExceptions


class ProductsNotExist(CRMExceptions):
    def __init__(
        self, message: str = PRODUCT_NOT_EXIST, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)


class ProductsExists(CRMExceptions):
    def __init__(self, message: str = PRODUCT_EXISTS, *args: object, **kwargs) -> None:
        super().__init__(message, *args, **kwargs)
