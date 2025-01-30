from typing import Callable, Tuple

from ..containers.auth import container as auth_container
from ..models.sys_users import SysUsers


def get_validated_session() -> Callable[[], Tuple[SysUsers, str]]:
    return auth_container["token_srvc"].validate_session


def get_create_session():
    return auth_container["token_srvc"].create_session
