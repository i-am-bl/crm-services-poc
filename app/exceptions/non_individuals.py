from ..constants.messages import (NON_INDIVIDUAL_EXISTS,
                                  NON_INDIVIDUAL_NOT_EXIST)
from .crm_exceptions import CRMExceptions


class NonIndividualNotExist(CRMExceptions):
    def __init__(
        self, message: str = NON_INDIVIDUAL_NOT_EXIST, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)


class NonIndividualExists(CRMExceptions):
    def __init__(
        self, message: str = NON_INDIVIDUAL_EXISTS, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)
