from fastapi import APIRouter, Depends, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...containers.services import container as service_container
from ...database.database import get_db, transaction_manager
from ...exceptions import SysUserExists, SysUserNotExist
from ...handlers.handler import handle_exceptions
from ...schemas.sys_users import SysUsersCreate, SysUsersRes
from ...services.sys_users import CreateSrvc

router = APIRouter()


@router.post(
    "/",
    response_model=SysUsersRes,
    status_code=status.HTTP_201_CREATED,
)
# @handle_exceptions([SysUserNotExist, SysUserExists])
async def create_sys_user(
    sys_user_data: SysUsersCreate,
    db: AsyncSession = Depends(get_db),
    sys_user_create_srvc: CreateSrvc = Depends(service_container["sys_users_create"]),
) -> SysUsersRes:
    """
    Create one system user.
    """
    print(">>>>", sys_user_create_srvc)

    async with transaction_manager(db=db):
        return await sys_user_create_srvc.create_sys_user(
            sys_user_data=sys_user_data, db=db
        )
