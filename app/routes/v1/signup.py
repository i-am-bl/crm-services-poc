from typing import Tuple

from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.database import get_db, transaction_manager
from ...exceptions import SysUserExists, SysUserNotExist
from ...handlers.handler import handle_exceptions
from ...schemas import sys_users as s_sys_user
from ...services.authetication import TokenService
from ...services.sys_users import SysUsersServices
from ...utilities.utilities import Pagination as pg

serv_sys_user_c = SysUsersServices.CreateService()
serv_token = TokenService()
router = APIRouter()


@router.post(
    "/",
    response_model=s_sys_user.SysUsersResponse,
    status_code=status.HTTP_201_CREATED,
)
@handle_exceptions([SysUserNotExist, SysUserExists])
async def create_sys_user(
    sys_user_data: s_sys_user.SysUsersCreate,
    db: AsyncSession = Depends(get_db),
) -> s_sys_user.SysUsersResponse:
    """
    Create one system user.
    """

    async with transaction_manager(db=db):
        return await serv_sys_user_c.create_sys_user(sys_user_data=sys_user_data, db=db)
