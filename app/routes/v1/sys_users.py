from modulefinder import AddPackagePath
from typing import Tuple

from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.database import get_db, transaction_manager
from ...exceptions import SysUserExists, SysUserNotExist
from ...handlers.handler import handle_exceptions
from ...schemas import sys_users as s_sys_user
from ...services.authetication import SessionService, TokenService
from ...services.sys_users import SysUsersServices
from ...utilities.set_values import SetSys
from ...utilities.utilities import Pagination as pg

serv_sys_user_c = SysUsersServices.CreateService()
serv_sys_user_r = SysUsersServices.ReadService()
serv_sys_user_u = SysUsersServices.UpdateService()
serv_sys_user_d = SysUsersServices.DelService()
serv_session = SessionService()
serv_token = TokenService()
router = APIRouter()


@router.get(
    "/{sys_user_uuid}/",
    response_model=s_sys_user.SysUsersResponse,
    include_in_schema=False,
)
@serv_token.set_auth_cookie
@handle_exceptions([SysUserNotExist])
async def get_sys_user(
    response: Response,
    sys_user_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_sys_user.SysUsersResponse:
    """get one user"""

    async with transaction_manager(db=db):
        return await serv_sys_user_r.get_sys_user_by_uuid(
            sys_user_uuid=sys_user_uuid, db=db
        )


@router.get(
    "/",
    response_model=s_sys_user.SysUsersPagResponse,
)
@serv_token.set_auth_cookie
@handle_exceptions([SysUserNotExist])
async def get_sys_users(
    response: Response,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_sys_user.SysUsersPagResponse:
    """
    Get many active system users.
    """

    async with transaction_manager(db=db):
        offset = pg.pagination_offset(page=page, limit=limit)
        total_count = await serv_sys_user_r.get_sys_users_ct(db=db)
        sys_users = await serv_sys_user_r.get_sys_users(
            limit=limit, offset=offset, db=db
        )
        has_more = pg.has_more(total_count=total_count, page=page, limit=limit)
        return s_sys_user.SysUsersPagResponse(
            total=total_count,
            page=page,
            limit=limit,
            has_more=has_more,
            sys_users=sys_users,
        )


@router.post(
    "/",
    response_model=s_sys_user.SysUsersResponse,
    status_code=status.HTTP_201_CREATED,
)
@serv_token.set_auth_cookie
@handle_exceptions([SysUserNotExist, SysUserExists])
async def create_sys_user(
    sys_user_data: s_sys_user.SysUsersCreate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_sys_user.SysUsersResponse:
    """
    create one system user on the behalf of another user.
    Intended for admin use only.
    """

    async with transaction_manager(db=db):
        return await serv_sys_user_c.create_sys_user(sys_user_data=sys_user_data, db=db)


@router.put(
    "/{sys_user_uuid}/",
    response_model=s_sys_user.SysUsersResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([SysUserNotExist])
async def update_sys_user(
    response: Response,
    sys_user_uuid: str,
    sys_user_data: s_sys_user.SysUsersUpdate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_sys_user.SysUsersResponse:
    """
    Update one system user.
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_updated_by(data=sys_user_data, sys_user=sys_user)
        return await serv_sys_user_u.update_sys_user(
            sys_user_uuid=sys_user_uuid, sys_user_data=sys_user_data, db=db
        )


@router.put(
    "/{sys_user_uuid}/disable/",
    response_model=s_sys_user.SysUsersResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([SysUserNotExist])
async def disable_sys_user(
    response: Response,
    sys_user_uuid: str,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_sys_user.SysUsersResponse:
    """disable one user"""

    async with transaction_manager(db=db):
        sys_user_data = s_sys_user.SysUsersDisable()
        sys_user, _ = user_token
        return await serv_sys_user_u.disable_sys_user(
            sys_user_uuid=sys_user_uuid, sys_user_data=sys_user_data, db=db
        )


@router.delete(
    "/{sys_user_uuid}/",
    response_model=s_sys_user.SysUsersResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([SysUserNotExist])
async def del_sys_user(
    response: Response,
    sys_user_uuid: str,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_sys_user.SysUsersResponse:
    """
    Soft delete one system user.
    """

    async with transaction_manager(db=db):
        sys_user_data = s_sys_user.SysUsersDel()
        sys_user, _ = user_token
        SetSys.sys_deleted_by(data=sys_user_data, sys_user=sys_user)
        return await serv_sys_user_d.soft_del_sys_user(
            sys_user_uuid=sys_user_uuid, sys_user_data=sys_user_data, db=db
        )
