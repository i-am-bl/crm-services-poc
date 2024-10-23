from app.exceptions.crm_exceptions import CRMExceptions

from ..constants.messages import (ENTITY_DATA_INVALID, ENTITY_EXISTS,
                                  ENTITY_INDIV_DATA_INVALID,
                                  ENTITY_NON_INDIV_DATA_INVALID,
                                  ENTITY_NOT_EXIST, ENTITY_TYPE_INVALID)


class EntityNotExist(CRMExceptions):
    def __init__(
        self, message: str = ENTITY_NOT_EXIST, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)


class EntityExists(CRMExceptions):
    def __init__(self, message: str = ENTITY_EXISTS, *args: object, **kwargs) -> None:
        super().__init__(message, *args, **kwargs)


class EntityIndivDataInvalid(CRMExceptions):
    def __init__(
        self, message: str = ENTITY_INDIV_DATA_INVALID, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)


class EntityNonIndivDataInvalid(CRMExceptions):
    def __init__(
        self, message: str = ENTITY_NON_INDIV_DATA_INVALID, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)


class EntityDataInvalid(CRMExceptions):
    def __init__(
        self, message: str = ENTITY_DATA_INVALID, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)


class EntityTypeInvalid(CRMExceptions):
    def __init__(
        self, message: str = ENTITY_TYPE_INVALID, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)
