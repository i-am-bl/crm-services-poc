from ..constants.messages import INDIVIDUAL_EXISTS, INDIVIDUAL_NOT_EXIST
from .crm_exceptions import CRMExceptions


class IndividualNotExist(CRMExceptions):
    """
    Custom exception raised when an individual does not exist in the system.

    Inherits from the base CRMExceptions class. The default message for this exception
    is specified by the constant `INDIVIDUAL_NOT_EXIST`. This exception is typically raised
    when an attempt is made to access or perform an operation on an individual that does not exist.

    :param message: The error message to display when the exception is raised.
                    Defaults to the value of INDIVIDUAL_NOT_EXIST.
    :param args: Additional positional arguments to pass to the parent exception class.
    :param kwargs: Additional keyword arguments to pass to the parent exception class.
    """

    def __init__(
        self, message: str = INDIVIDUAL_NOT_EXIST, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)


class IndividualExists(CRMExceptions):
    """
    Custom exception raised when an individual already exists in the system.

    Inherits from the base CRMExceptions class. The default message for this exception
    is specified by the constant `INDIVIDUAL_EXISTS`. This exception is typically raised
    when an attempt is made to create or register an individual that already exists.

    :param message: The error message to display when the exception is raised.
                    Defaults to the value of INDIVIDUAL_EXISTS.
    :param args: Additional positional arguments to pass to the parent exception class.
    :param kwargs: Additional keyword arguments to pass to the parent exception class.
    """

    def __init__(
        self, message: str = INDIVIDUAL_EXISTS, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)
