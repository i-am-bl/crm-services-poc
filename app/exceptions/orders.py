from ..constants.messages import ORDER_EXISTS, ORDER_NOT_EXIST
from .crm_exceptions import CRMExceptions


class OrderNotExist(CRMExceptions):
    def __init__(self, message: str = ORDER_NOT_EXIST, *args: object, **kwargs) -> None:
        super().__init__(message, *args, **kwargs)


class OrderExists(CRMExceptions):
    def __init__(self, message: str = ORDER_EXISTS, *args: object, **kwargs) -> None:
        super().__init__(message, *args, **kwargs)
