from ..constants.messages import ORDER_ITEM_EXISTS, ORDER_ITEM_NOT_EXIST
from .crm_exceptions import CRMExceptions


class OrderItemNotExist(CRMExceptions):
    def __init__(
        self, message: str = ORDER_ITEM_NOT_EXIST, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)


class OrderItemExists(CRMExceptions):
    def __init__(
        self, message: str = ORDER_ITEM_EXISTS, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)
