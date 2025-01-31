"""
Auth utilities for session validation and creation, assisting with dependency injection.
"""

from typing import Callable, Tuple
from fastapi import Depends, Cookie
from sqlalchemy.ext.asyncio import AsyncSession

from ..containers.auth import container as auth_container
from ..database.database import get_db
from ..services.token import TokenSrvc
from ..models.sys_users import SysUsers


async def get_validated_session(
    db: AsyncSession = Depends(get_db),
    jwt: str = Cookie(...),
) -> Callable[[], Tuple[SysUsers, str]]:
    """
    Returns a callable that validates a session. When invoked, this function returns a tuple containing
    a `SysUsers` object and a string representing the session status.

    :return: Callable[[], Tuple[SysUsers, str]]: A function that validates the session and returns a tuple
            consisting of a `SysUsers` object and a session status string.
    """
    token_srvc: TokenSrvc = auth_container["token_srvc"]()
    return await token_srvc.validate_session(db=db, jwt=jwt)
