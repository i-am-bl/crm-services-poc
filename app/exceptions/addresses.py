from ..constants.messages import ADDRESSES_EXISTS, ADDRESSES_NOT_EXIST
from .crm_exceptions import CRMExceptions


class AddressNotExist(CRMExceptions):
    def __init__(
        self, message: str = ADDRESSES_NOT_EXIST, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)


class AddressExists(CRMExceptions):
    def __init__(
        self, message: str = ADDRESSES_EXISTS, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)
