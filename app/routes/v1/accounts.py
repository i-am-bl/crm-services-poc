from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.database import get_db, transaction_manager
from ...exceptions import AccsNotExist
from ...handlers.handler import handle_exceptions
from ...schemas import accounts as s_accounts
from ...services.accounts import AccountsServices
from ...services.authetication import SessionService, TokenService
from ...utilities.logger import logger
from ...utilities.sys_users import SetSys
from ...utilities.utilities import Pagination as pg

serv_acc_r = AccountsServices.ReadService()
serv_acc_c = AccountsServices.CreateService()
serv_acc_u = AccountsServices.UpdateService()
serv_acc_d = AccountsServices.DelService()
serv_session = SessionService()
serv_token = TokenService()

router = APIRouter()


@router.get(
    "/v1/account-management/accounts/{account_uuid}/",
    response_model=s_accounts.AccountsResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([AccsNotExist])
async def get_account(
    response: Response,
    account_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
):
    """get one account by account_uuid"""

    async with transaction_manager(db=db):
        account = await serv_acc_r.get_account(account_uuid=account_uuid, db=db)
        return account


@router.get(
    "/v1/account-management/accounts/",
    response_model=s_accounts.AccountsPagResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([AccsNotExist])
async def get_accounts(
    response: Response,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_accounts.AccountsPagResponse:
    """get all accounts"""

    async with transaction_manager(db=db):
        offset = pg.pagination_offset(page=page, limit=limit)
        total_count = await serv_acc_r.get_account_ct(db=db)
        accounts = await serv_acc_r.get_accounts(db=db, offset=offset, limit=limit)
        return {
            "total": total_count,
            "page": page,
            "limit": limit,
            "has_more": pg.has_more(total_count=total_count, page=page, limit=limit),
            "accounts": accounts,
        }


@router.post(
    "/v1/account-management/accounts/",
    response_model=s_accounts.AccountsResponse,
    status_code=status.HTTP_201_CREATED,
)
@serv_token.set_auth_cookie
@handle_exceptions([AccsNotExist])
async def create_account(
    response: Response,
    account_data: s_accounts.AccountsCreate,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_accounts.AccountsCreate:
    """create one account"""

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_created_by(data=account_data, sys_user=sys_user)
        account = await serv_acc_c.create_account(account_data=account_data, db=db)
        return account


@router.put(
    "/v1/account-management/accounts/{account_uuid}/",
    response_model=s_accounts.AccountsResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([AccsNotExist])
async def update_account(
    response: Response,
    account_uuid: UUID4,
    account_data: s_accounts.AccountsUpdate,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_accounts.AccountsUpdate:
    """update one account"""

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_updated_by(data=account_data, sys_user=sys_user)
        account = await serv_acc_u.update_account(
            account_uuid=account_uuid, account_data=account_data, db=db
        )
        return account


@router.delete(
    "/v1/account-management/accounts/{account_uuid}/",
    response_model=s_accounts.AccountsDelResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([AccsNotExist])
async def soft_del_account(
    response: Response,
    account_uuid: UUID4,
    account_data: s_accounts.AccountsDel,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_accounts.AccountsDel:
    """soft del one account"""

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_deleted_by(data=account_data, sys_user=sys_user)
        account = await serv_acc_d.sof_del_account(
            account_uuid=account_uuid, account_data=account_data, db=db
        )
        return account
