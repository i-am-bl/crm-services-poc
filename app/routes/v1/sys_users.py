from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

import app.constants as cnst
import app.messages as msg
import app.schemas.sys_users as s_sys_user
from app.services.sys_users import SysUsersServices, SysUserAuthService
from app.database.database import get_db
from app.logger import logger

router = APIRouter()

serv_sys_user_c = SysUsersServices.CreateService()
serv_sys_user_r = SysUsersServices.ReadService()
serv_sys_user_u = SysUsersServices.UpdateService()
serv_sys_user_d = SysUsersServices.DelService()
serv_auth = SysUserAuthService()


@router.get(
    "/v1/system-management/users/{sys_user_uuid}",
    response_model=s_sys_user.SysUsersResponse,
)
async def get_sys_user(sys_user_uuid: UUID4, db: AsyncSession = Depends(get_db)):
    """get one user"""
    async with db.begin():
        sys_user = await serv_sys_user_r.get_sys_user_by_uuid(
            sys_user_uuid=sys_user_uuid, db=db
        )
    return sys_user


@router.get(
    "/v1/system-management/users/",
    response_model=s_sys_user.SysUsersPagResponse,
)
async def get_sys_users(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """get many users"""
    async with db.begin():
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
async def create_sys_user(
    sys_user_data: s_sys_user.SysUsersCreate,
    db: AsyncSession = Depends(get_db),
):
    """create one user"""
    async with db.begin():
        sys_user = await serv_sys_user_c.create_sys_user(
            sys_user_data=sys_user_data, db=db
        )
    return sys_user


@router.post("/v1/system-management/login/")
async def sys_user_login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    """user login"""
    athenticated_user = await serv_auth.authenticate_sys_user(
        form_data=form_data, db=db
    )
    if not athenticated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=msg.USER_INVALID_CREDENTIALS
        )
    encoded_jwt = await serv_auth.gen_sys_session(form_data=form_data, db=db)

    return s_sys_user.Token(access_token=encoded_jwt, token_type="bearer")


@router.put(
    "/v1/system-management/users/{sys_user_uuid}",
    response_model=s_sys_user.SysUsersResponse,
    status_code=status.HTTP_200_OK,
)
async def update_sys_user(
    sys_user_uuid: str,
    sys_user_data: s_sys_user.SysUsersUpdate,
    db: AsyncSession = Depends(get_db),
):
    """update one user"""
    async with db.begin():
        sys_user = await serv_sys_user_u.update_sys_user(
            sys_user_uuid=sys_user_uuid, sys_user_data=sys_user_data, db=db
        )
    return sys_user


@router.put(
    "/v1/system-management/users/{sys_user_uuid}/disable",
    response_model=s_sys_user.SysUsersResponse,
    status_code=status.HTTP_200_OK,
)
async def disable_sys_user(
    sys_user_uuid: str,
    sys_user_data: s_sys_user.SysUsersDisable,
    db: AsyncSession = Depends(get_db),
):
    """disable one user"""
    async with db.begin():
        sys_user = await serv_sys_user_u.disable_sys_user(
            sys_user_uuid=sys_user_uuid, sys_user_data=sys_user_data, db=db
        )
    return sys_user


@router.delete(
    "/v1/system-management/users/{sys_user_uuid}",
    response_model=s_sys_user.SysUsersResponse,
    status_code=status.HTTP_200_OK,
)
async def del_sys_user(
    sys_user_uuid: str,
    sys_user_data: s_sys_user.SysUsersDel,
    db: AsyncSession = Depends(get_db),
):
    """soft delete one user"""
    async with db.begin():
        sys_user = await serv_sys_user_d.soft_del_sys_user(
            sys_user_uuid=sys_user_uuid, sys_user_data=sys_user_data, db=db
        )
    return sys_user
