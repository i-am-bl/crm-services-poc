from ..constants.messages import (ENTITY_ACCOUNT_EXISTS,
                                  ENTITY_ACCOUNT_NOT_EXIST)
from .crm_exceptions import CRMExceptions


class EntityAccNotExist(CRMExceptions):
    def __init__(
        self, message: str = ENTITY_ACCOUNT_NOT_EXIST, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)


class EntityAccExists(CRMExceptions):
    def __init__(
        self, message: str = ENTITY_ACCOUNT_EXISTS, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)
