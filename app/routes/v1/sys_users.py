from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.database import get_db, transaction_manager
from ...exceptions import SysUserExists, SysUserNotExist
from ...handlers.handler import handle_exceptions
from ...schemas import sys_users as s_sys_user
from ...services.authetication import SessionService, TokenService
from ...services.sys_users import SysUsersServices
from ...utilities.logger import logger
from ...utilities.sys_users import SetSys

serv_sys_user_c = SysUsersServices.CreateService()
serv_sys_user_r = SysUsersServices.ReadService()
serv_sys_user_u = SysUsersServices.UpdateService()
serv_sys_user_d = SysUsersServices.DelService()
serv_session = SessionService()
serv_token = TokenService()
router = APIRouter()


@router.get(
    "/v1/system-management/users/{sys_user_uuid}/",
    response_model=s_sys_user.SysUsersResponse,
)
@serv_token.set_auth_cookie
@handle_exceptions([SysUserNotExist])
async def get_sys_user(
    response: Response,
    sys_user_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_sys_user.SysUsersResponse:
    """get one user"""

    async with transaction_manager(db=db):
        sys_user, token = user_token
        sys_user = await serv_sys_user_r.get_sys_user_by_uuid(
            sys_user_uuid=sys_user_uuid, db=db
        )
        return sys_user


@router.get(
    "/v1/system-management/users/",
    response_model=s_sys_user.SysUsersPagResponse,
)
@serv_token.set_auth_cookie
@handle_exceptions([SysUserNotExist])
async def get_sys_users(
    response: Response,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_sys_user.SysUsersPagResponse:
    """get many users"""

    async with transaction_manager(db=db):
        # TODO: Set offset with  utility
        offset = None
        total_count = await serv_sys_user_r.get_sys_users_ct(db=db)
        sys_users = await serv_sys_user_r.get_sys_users(
            limit=limit, offset=offset, db=db
        )
        return {
            "total": total_count,
            "page": page,
            "limit": limit,
            "has_more": total_count > (page * limit),
            "sys_users": sys_users,
        }


@router.post(
    "/v1/system-management/sign-up/",
    response_model=s_sys_user.SysUsersResponse,
    status_code=status.HTTP_201_CREATED,
)
@handle_exceptions([SysUserNotExist, SysUserExists])
async def create_sys_user(
    # request: Request,
    # response: Response,
    sys_user_data: s_sys_user.SysUsersCreate,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_sys_user.SysUsersResponse:
    """create one user"""

    async with transaction_manager(db=db):
        # TODO: decide on routing for user creation, need sign up flow hooked up
        # _ = await serv_session.validate_session(
        #     request=request, response=response, db=db
        # )
        sys_user = await serv_sys_user_c.create_sys_user(
            sys_user_data=sys_user_data, db=db
        )
        # await AuthUtils.set_cookie(
        #     response=response, token=token, sys_user_uuid=sys_user.uuid
        # )
    return sys_user


@router.put(
    "/v1/system-management/users/{sys_user_uuid}/",
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
    user_token: str = Depends(serv_session.validate_session),
) -> s_sys_user.SysUsersResponse:
    """update one user"""

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_updated_by(data=sys_user_data, sys_user=sys_user)
        sys_user = await serv_sys_user_u.update_sys_user(
            sys_user_uuid=sys_user_uuid, sys_user_data=sys_user_data, db=db
        )
        return sys_user


@router.put(
    "/v1/system-management/users/{sys_user_uuid}/disable/",
    response_model=s_sys_user.SysUsersResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([SysUserNotExist])
async def disable_sys_user(
    response: Response,
    sys_user_uuid: str,
    sys_user_data: s_sys_user.SysUsersDisable,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_sys_user.SysUsersResponse:
    """disable one user"""

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        sys_user = await serv_sys_user_u.disable_sys_user(
            sys_user_uuid=sys_user_uuid, sys_user_data=sys_user_data, db=db
        )
        return sys_user


@router.delete(
    "/v1/system-management/users/{sys_user_uuid}/",
    response_model=s_sys_user.SysUsersResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([SysUserNotExist])
async def del_sys_user(
    response: Response,
    sys_user_uuid: str,
    sys_user_data: s_sys_user.SysUsersDel,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_sys_user.SysUsersResponse:
    """soft delete one user"""

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_deleted_by(data=sys_user_data, sys_user=sys_user)
        sys_user = await serv_sys_user_d.soft_del_sys_user(
            sys_user_uuid=sys_user_uuid, sys_user_data=sys_user_data, db=db
        )
        return sys_user
