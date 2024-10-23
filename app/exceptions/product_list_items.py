from ..constants.messages import PRODUCT_LIST_EXISTS, PRODUCT_LIST_ITEM_EXISTS
from .crm_exceptions import CRMExceptions


class ProductListItemNotExist(CRMExceptions):
    def __init__(
        self, message: str = PRODUCT_LIST_EXISTS, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)


class ProductListItemExists(CRMExceptions):
    def __init__(
        self, message: str = PRODUCT_LIST_ITEM_EXISTS, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)
