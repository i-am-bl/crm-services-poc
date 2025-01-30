from typing import Tuple

from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...containers.services import container as services_container
from ...database.database import get_db, transaction_manager
from ...exceptions import SysUserExists, SysUserNotExist
from ...handlers.handler import handle_exceptions
from ...models.sys_users import SysUsers
from ...schemas.sys_users import (
    SysUsersCreate,
    SysUsersDel,
    SysUsersDisable,
    SysUsersPgRes,
    SysUsersRes,
    SysUsersUpdate,
)
from ...services.sys_users import ReadSrvc, CreateSrvc, UpdateSrvc, DelSrvc
from ...services.token import set_auth_cookie
from ...utilities import sys_values
from ...utilities.auth import get_validated_session

router = APIRouter()


@router.get(
    "/{sys_user_uuid}/",
    response_model=SysUsersRes,
    include_in_schema=False,
)
@set_auth_cookie
@handle_exceptions([SysUserNotExist])
async def get_sys_user(
    response: Response,
    sys_user_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    sys_users_read_srvc: ReadSrvc = Depends(services_container["sys_users_read"]),
) -> SysUsersRes:
    """get one user"""

    async with transaction_manager(db=db):
        return await sys_users_read_srvc.get_sys_user(
            sys_user_uuid=sys_user_uuid, db=db
        )


@router.get(
    "/",
    response_model=SysUsersPgRes,
)
@set_auth_cookie
@handle_exceptions([SysUserNotExist])
async def get_sys_users(
    response: Response,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    sys_users_read_srvc: ReadSrvc = Depends(services_container["sys_users_read"]),
) -> SysUsersPgRes:
    """
    Get many active system users.
    """

    async with transaction_manager(db=db):
        return await sys_users_read_srvc.paginated_users(page=page, limit=limit, db=db)


@router.post(
    "/",
    response_model=SysUsersRes,
    status_code=status.HTTP_201_CREATED,
)
@set_auth_cookie
@handle_exceptions([SysUserNotExist, SysUserExists])
async def create_sys_user(
    sys_user_data: SysUsersCreate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    sys_users_create_srvc: CreateSrvc = Depends(services_container["sys_users_create"]),
) -> SysUsersRes:
    """
    create one system user on the behalf of another user.
    Intended for admin use only.
    """

    async with transaction_manager(db=db):
        return await sys_users_create_srvc.create_sys_user(
            sys_user_data=sys_user_data, db=db
        )


@router.put(
    "/{sys_user_uuid}/",
    response_model=SysUsersRes,
    status_code=status.HTTP_200_OK,
)
@set_auth_cookie
@handle_exceptions([SysUserNotExist])
async def update_sys_user(
    response: Response,
    sys_user_uuid: str,
    sys_user_data: SysUsersUpdate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    sys_users_update_srvc: UpdateSrvc = Depends(services_container["sys_users_update"]),
) -> SysUsersRes:
    """
    Update one system user.
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        sys_values.sys_updated_by(data=sys_user_data, sys_user=sys_user.uuid)
        return await sys_users_update_srvc.update_sys_user(
            sys_user_uuid=sys_user_uuid, sys_user_data=sys_user_data, db=db
        )


@router.put(
    "/{sys_user_uuid}/disable/",
    response_model=SysUsersRes,
    status_code=status.HTTP_200_OK,
)
@set_auth_cookie
@handle_exceptions([SysUserNotExist])
async def disable_sys_user(
    response: Response,
    sys_user_uuid: str,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    sys_users_update_srvc: UpdateSrvc = Depends(services_container["sys_users_update"]),
) -> SysUsersRes:
    """disable one user"""

    async with transaction_manager(db=db):
        sys_user_data = SysUsersDisable()
        sys_user, _ = user_token
        return await sys_users_update_srvc.disable_sys_user(
            sys_user_uuid=sys_user_uuid, sys_user_data=sys_user_data, db=db
        )


@router.delete(
    "/{sys_user_uuid}/",
    response_model=SysUsersRes,
    status_code=status.HTTP_204_NO_CONTENT,
)
@set_auth_cookie
@handle_exceptions([SysUserNotExist])
async def del_sys_user(
    response: Response,
    sys_user_uuid: str,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    sys_users_delete_srvc: DelSrvc = Depends(services_container["sys_users_delete"]),
) -> None:
    """
    Soft delete one system user.
    """

    async with transaction_manager(db=db):
        sys_user_data = SysUsersDel()
        sys_user, _ = user_token
        sys_values.sys_deleted_by(data=sys_user_data, sys_user=sys_user.uuid)
        await sys_users_delete_srvc.soft_del_sys_user(
            sys_user_uuid=sys_user_uuid, sys_user_data=sys_user_data, db=db
        )
