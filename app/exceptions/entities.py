from app.exceptions.crm_exceptions import CRMExceptions
from ..constants.messages import (
    ENTITY_DATA_INVALID,
    ENTITY_EXISTS,
    ENTITY_INDIV_DATA_INVALID,
    ENTITY_NON_INDIV_DATA_INVALID,
    ENTITY_NOT_EXIST,
    ENTITY_TYPE_INVALID,
)


class EntityNotExist(CRMExceptions):
    """
    Custom exception raised when an entity does not exist in the system.

    Inherits from the base CRMExceptions class. The default message for this exception
    is specified by the constant `ENTITY_NOT_EXIST`. This exception is typically raised
    when an attempt is made to access or perform an operation on an entity that is not found.

    :param message: The error message to display when the exception is raised.
                    Defaults to the value of ENTITY_NOT_EXIST.
    :param args: Additional positional arguments to pass to the parent exception class.
    :param kwargs: Additional keyword arguments to pass to the parent exception class.
    """

    def __init__(
        self, message: str = ENTITY_NOT_EXIST, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)


class EntityExists(CRMExceptions):
    """
    Custom exception raised when an entity already exists in the system.

    Inherits from the base CRMExceptions class. The default message for this exception
    is specified by the constant `ENTITY_EXISTS`. This exception is typically raised
    when an attempt is made to create or register an entity that already exists in the system.

    :param message: The error message to display when the exception is raised.
                    Defaults to the value of ENTITY_EXISTS.
    :param args: Additional positional arguments to pass to the parent exception class.
    :param kwargs: Additional keyword arguments to pass to the parent exception class.
    """

    def __init__(self, message: str = ENTITY_EXISTS, *args: object, **kwargs) -> None:
        super().__init__(message, *args, **kwargs)


class EntityIndivDataInvalid(CRMExceptions):
    """
    Custom exception raised when individual entity data is invalid.

    Inherits from the base CRMExceptions class. The default message for this exception
    is specified by the constant `ENTITY_INDIV_DATA_INVALID`. This exception is typically
    raised when the data for an individual entity does not meet the expected format or validation.

    :param message: The error message to display when the exception is raised.
                    Defaults to the value of ENTITY_INDIV_DATA_INVALID.
    :param args: Additional positional arguments to pass to the parent exception class.
    :param kwargs: Additional keyword arguments to pass to the parent exception class.
    """

    def __init__(
        self, message: str = ENTITY_INDIV_DATA_INVALID, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)


class EntityNonIndivDataInvalid(CRMExceptions):
    """
    Custom exception raised when non-individual entity data is invalid.

    Inherits from the base CRMExceptions class. The default message for this exception
    is specified by the constant `ENTITY_NON_INDIV_DATA_INVALID`. This exception is typically
    raised when the data for a non-individual entity does not meet the expected format or validation.

    :param message: The error message to display when the exception is raised.
                    Defaults to the value of ENTITY_NON_INDIV_DATA_INVALID.
    :param args: Additional positional arguments to pass to the parent exception class.
    :param kwargs: Additional keyword arguments to pass to the parent exception class.
    """

    def __init__(
        self, message: str = ENTITY_NON_INDIV_DATA_INVALID, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)


class EntityDataInvalid(CRMExceptions):
    """
    Custom exception raised when entity data is invalid.

    Inherits from the base CRMExceptions class. The default message for this exception
    is specified by the constant `ENTITY_DATA_INVALID`. This exception is typically raised
    when the data for an entity does not meet the expected format or validation.

    :param message: The error message to display when the exception is raised.
                    Defaults to the value of ENTITY_DATA_INVALID.
    :param args: Additional positional arguments to pass to the parent exception class.
    :param kwargs: Additional keyword arguments to pass to the parent exception class.
    """

    def __init__(
        self, message: str = ENTITY_DATA_INVALID, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)


class EntityTypeInvalid(CRMExceptions):
    """
    Custom exception raised when the entity type is invalid.

    Inherits from the base CRMExceptions class. The default message for this exception
    is specified by the constant `ENTITY_TYPE_INVALID`. This exception is typically raised
    when the entity type provided does not match the expected or valid types in the system.

    :param message: The error message to display when the exception is raised.
                    Defaults to the value of ENTITY_TYPE_INVALID.
    :param args: Additional positional arguments to pass to the parent exception class.
    :param kwargs: Additional keyword arguments to pass to the parent exception class.
    """

    def __init__(
        self, message: str = ENTITY_TYPE_INVALID, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)
