from typing import Callable, Tuple

from ..containers.auth import container as auth_container
from ..models.sys_users import SysUsers

"""
Auth utilities for session validation and creation, assisting with dependency injection.
"""


def get_validated_session() -> Callable[[], Tuple[SysUsers, str]]:
    """
    Returns a callable that validates a session. When invoked, this function returns a tuple containing
    a `SysUsers` object and a string representing the session status.

    :return: Callable[[], Tuple[SysUsers, str]]: A function that validates the session and returns a tuple
            consisting of a `SysUsers` object and a session status string.
    """
    return auth_container["token_srvc"].validate_session
