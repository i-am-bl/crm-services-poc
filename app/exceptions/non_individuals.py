from ..constants.messages import NON_INDIVIDUAL_EXISTS, NON_INDIVIDUAL_NOT_EXIST
from .crm_exceptions import CRMExceptions


class NonIndividualNotExist(CRMExceptions):
    """
    Custom exception raised when a non-individual entity does not exist in the system.

    Inherits from the base CRMExceptions class. The default message for this exception
    is specified by the constant `NON_INDIVIDUAL_NOT_EXIST`. This exception is typically raised
    when an attempt is made to access or perform an operation on a non-individual entity that does not exist.

    :param message: The error message to display when the exception is raised.
                    Defaults to the value of NON_INDIVIDUAL_NOT_EXIST.
    :param args: Additional positional arguments to pass to the parent exception class.
    :param kwargs: Additional keyword arguments to pass to the parent exception class.
    """

    def __init__(
        self, message: str = NON_INDIVIDUAL_NOT_EXIST, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)


class NonIndividualExists(CRMExceptions):
    """
    Custom exception raised when a non-individual entity already exists in the system.

    Inherits from the base CRMExceptions class. The default message for this exception
    is specified by the constant `NON_INDIVIDUAL_EXISTS`. This exception is typically raised
    when an attempt is made to create or register a non-individual entity that already exists.

    :param message: The error message to display when the exception is raised.
                    Defaults to the value of NON_INDIVIDUAL_EXISTS.
    :param args: Additional positional arguments to pass to the parent exception class.
    :param kwargs: Additional keyword arguments to pass to the parent exception class.
    """

    def __init__(
        self, message: str = NON_INDIVIDUAL_EXISTS, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)
