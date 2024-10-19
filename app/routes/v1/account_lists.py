from typing import Annotated, List

from fastapi import APIRouter, Depends, Query, Request, Response, status
from httpx import Auth
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.database import get_db, transaction_manager
from ...exceptions import (AccListExists, AccListNotExist, SysUserNotExist,
                           UnhandledException)
from ...handlers.handler import handle_exceptions
from ...schemas import account_lists as s_account_lists
from ...services.account_lists import AccountListsServices
from ...services.authetication import SessionService, TokenService
from ...utilities.sys_users import SetSys
from ...utilities.utilities import Pagination as pg

serv_acc_ls_r = AccountListsServices.ReadService()
serv_acc_ls_c = AccountListsServices.CreateService()
serv_acc_ls_u = AccountListsServices.UpdateService()
serv_acc_ls_d = AccountListsServices.DelService()
serv_session = SessionService()
serv_token = TokenService()

router = APIRouter()


@router.get(
    "/v1/account-management/accounts/{account_uuid}/account-lists/{account_list_uuid}/",
    response_model=s_account_lists.AccountListsResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([AccListNotExist])
async def get_account_list(
    account_uuid: UUID4,
    account_list_uuid: UUID4,
    response: Response,
    user_token: str = Depends(serv_session.validate_session),
    db: AsyncSession = Depends(get_db),
) -> s_account_lists.AccountListsResponse:
    """get one account list"""

    async with transaction_manager(db=db):
        account_list = await serv_acc_ls_r.get_account_list(
            account_uuid=account_uuid, account_list_uuid=account_list_uuid, db=db
        )
        return account_list


@router.get(
    "/v1/account-management/accounts/{account_uuid}/account-lists/",
    response_model=s_account_lists.AccountListsPagResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([AccListNotExist])
async def get_account_lists(
    response: Response,
    account_uuid: UUID4,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_account_lists.AccountListsPagResponse:
    """get all account lists by account"""

    async with transaction_manager(db=db):
        offset = pg.pagination_offset(page=page, limit=limit)
        total_count = await serv_acc_ls_r.get_account_list_ct(
            account_uuid=account_uuid, db=db
        )
        account_lists = await serv_acc_ls_r.get_account_lists(
            account_uuid=account_uuid, limit=limit, offset=offset, db=db
        )
        return {
            "total": total_count,
            "page": page,
            "limit": limit,
            "has_more": pg.has_more(total_count=total_count, page=page, limit=limit),
            "account_lists": account_lists,
        }


@router.post(
    "/v1/account-management/accounts/{account_uuid}/account-lists/",
    response_model=s_account_lists.AccountListsResponse,
    status_code=status.HTTP_201_CREATED,
)
@serv_token.set_auth_cookie
@handle_exceptions([AccListNotExist, AccListExists])
async def create_account_list(
    response: Response,
    account_uuid: UUID4,
    account_list_data: s_account_lists.AccountListsCreate,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_account_lists.AccountListsResponse:
    """create one account list"""

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_created_by(data=account_list_data, sys_user=sys_user)
        account_list = await serv_acc_ls_c.create_account_list(
            account_uuid=account_uuid, account_list_data=account_list_data, db=db
        )
        return account_list


@router.put(
    "/v1/account-management/accounts/{account_uuid}/account-lists/{account_list_uuid}/",
    response_model=s_account_lists.AccountListsResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([AccListNotExist])
async def update_account_list(
    response: Response,
    account_uuid: UUID4,
    account_list_uuid: UUID4,
    account_list_data: s_account_lists.AccountListsUpdate,
    user_token: str = Depends(serv_session.validate_session),
    db: AsyncSession = Depends(get_db),
) -> s_account_lists.AccountListsResponse:
    """update one account list"""

    async with transaction_manager(db=db):
        sys_user, token = user_token
        SetSys.sys_updated_by(data=account_list_data, sys_user=sys_user)
        account_list = await serv_acc_ls_u.update_account_list(
            account_uuid=account_uuid,
            account_list_uuid=account_list_uuid,
            account_list_data=account_list_data,
            db=db,
        )
        return account_list


@router.delete(
    "/v1/account-management/accounts/{account_uuid}/account-lists/{account_list_uuid}/",
    response_model=s_account_lists.AccountListsDelResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([AccListNotExist])
async def soft_del_account_list(
    request: Request,
    response: Response,
    account_uuid: UUID4,
    account_list_uuid: UUID4,
    account_list_data: s_account_lists.AccountListsDel,
    user_token: str = Depends(serv_session.validate_session),
    db: AsyncSession = Depends(get_db),
) -> s_account_lists.AccountListsDelResponse:
    """soft delete one account list"""

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_deleted_by(data=account_list_data, sys_user=sys_user)
        account_list = await serv_acc_ls_d.soft_del_account_list(
            account_uuid=account_uuid,
            account_list_uuid=account_list_uuid,
            account_list_data=account_list_data,
            db=db,
        )
        return account_list
