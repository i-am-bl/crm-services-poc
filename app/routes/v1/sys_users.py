from fastapi import APIRouter, Depends, Query, Request, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...constants import messages as msg
from ...database.database import get_db
from ...schemas import sys_users as s_sys_user
from ...services.authetication import SessionService
from ...services.sys_users import SysUsersServices
from ...utilities.logger import logger
from ...utilities.set_values import SetField
from ...utilities.sys_users import SetSys
from ...exceptions import UnhandledException, SysUserExists, SysUserNotExist

router = APIRouter()

serv_sys_user_c = SysUsersServices.CreateService()
serv_sys_user_r = SysUsersServices.ReadService()
serv_sys_user_u = SysUsersServices.UpdateService()
serv_sys_user_d = SysUsersServices.DelService()
serv_session = SessionService()


@router.get(
    "/v1/system-management/users/{sys_user_uuid}/",
    response_model=s_sys_user.SysUsersResponse,
)
async def get_sys_user(
    request: Request,
    response: Response,
    sys_user_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
):
    """get one user"""
    try:
        async with db.begin():
            _ = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            sys_user = await serv_sys_user_r.get_sys_user_by_uuid(
                sys_user_uuid=sys_user_uuid, db=db
            )
        return sys_user
    except SysUserNotExist:
        raise SysUserNotExist()
    except Exception:
        raise UnhandledException()


@router.get(
    "/v1/system-management/users/",
    response_model=s_sys_user.SysUsersPagResponse,
)
async def get_sys_users(
    request: Request,
    response: Response,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """get many users"""
    try:
        async with db.begin():
            _ = await serv_session.validate_session(
                request=request, response=response, db=db
            )
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
    except SysUserNotExist:
        raise SysUserNotExist()
    except Exception:
        raise UnhandledException()


@router.post(
    "/v1/system-management/sign-up/",
    response_model=s_sys_user.SysUsersResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_sys_user(
    # request: Request,
    # response: Response,
    sys_user_data: s_sys_user.SysUsersCreate,
    db: AsyncSession = Depends(get_db),
):
    """create one user"""
    try:
        async with db.begin():
            # TODO: decide on routing for user creation, need sign up flow hooked up
            # _ = await serv_session.validate_session(
            #     request=request, response=response, db=db
            # )
            sys_user = await serv_sys_user_c.create_sys_user(
                sys_user_data=sys_user_data, db=db
            )
        return sys_user
    except SysUserExists:
        raise SysUserExists()
    except SysUserNotExist:
        raise SysUserNotExist()
    except Exception:
        raise UnhandledException()


@router.put(
    "/v1/system-management/users/{sys_user_uuid}/",
    response_model=s_sys_user.SysUsersResponse,
    status_code=status.HTTP_200_OK,
)
async def update_sys_user(
    request: Request,
    response: Response,
    sys_user_uuid: str,
    sys_user_data: s_sys_user.SysUsersUpdate,
    db: AsyncSession = Depends(get_db),
):
    """update one user"""
    try:
        async with db.begin():
            _sys_user = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            SetSys.sys_updated_by(data=sys_user_data, sys_user=_sys_user)
            sys_user = await serv_sys_user_u.update_sys_user(
                sys_user_uuid=sys_user_uuid, sys_user_data=sys_user_data, db=db
            )
        return sys_user
    except SysUserNotExist:
        raise SysUserNotExist()
    except Exception:
        raise UnhandledException()


@router.put(
    "/v1/system-management/users/{sys_user_uuid}/disable/",
    response_model=s_sys_user.SysUsersResponse,
    status_code=status.HTTP_200_OK,
)
async def disable_sys_user(
    request: Request,
    response: Response,
    sys_user_uuid: str,
    sys_user_data: s_sys_user.SysUsersDisable,
    db: AsyncSession = Depends(get_db),
):
    """disable one user"""
    try:
        async with db.begin():
            _ = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            sys_user = await serv_sys_user_u.disable_sys_user(
                sys_user_uuid=sys_user_uuid, sys_user_data=sys_user_data, db=db
            )
        return sys_user
    except SysUserNotExist:
        raise SysUserNotExist()
    except Exception:
        raise UnhandledException()


@router.delete(
    "/v1/system-management/users/{sys_user_uuid}/",
    response_model=s_sys_user.SysUsersResponse,
    status_code=status.HTTP_200_OK,
)
async def del_sys_user(
    request: Request,
    response: Response,
    sys_user_uuid: str,
    sys_user_data: s_sys_user.SysUsersDel,
    db: AsyncSession = Depends(get_db),
):
    """soft delete one user"""
    try:
        async with db.begin():
            _sys_user = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            SetSys.sys_deleted_by(data=sys_user_data, sys_user=_sys_user)
            sys_user = await serv_sys_user_d.soft_del_sys_user(
                sys_user_uuid=sys_user_uuid, sys_user_data=sys_user_data, db=db
            )
        return sys_user
    except SysUserNotExist:
        raise SysUserNotExist()
    except Exception:
        raise UnhandledException()
