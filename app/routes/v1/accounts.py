from fastapi import APIRouter, Depends, Query, Request, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.database import get_db
from ...exceptions import AccsNotExist, UnhandledException
from ...schemas import accounts as s_accounts
from ...services.accounts import AccountsServices
from ...services.authetication import SessionService
from ...utilities.logger import logger
from ...utilities.service_utils import pagination_offset
from ...utilities.sys_users import SetSys

from ...exceptions import UnhandledException, AccsNotExist, AccsExists

serv_acc_r = AccountsServices.ReadService()
serv_acc_c = AccountsServices.CreateService()
serv_acc_u = AccountsServices.UpdateService()
serv_acc_d = AccountsServices.DelService()
serv_session = SessionService()

router = APIRouter()


@router.get(
    "/v1/account-management/accounts/{account_uuid}/",
    response_model=s_accounts.AccountsResponse,
    status_code=status.HTTP_200_OK,
)
async def get_account(
    request: Request,
    response: Response,
    account_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
):
    """get one account by account_uuid"""
    try:
        async with db.begin():
            _ = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            account = await serv_acc_r.get_account(account_uuid=account_uuid, db=db)
            return account
    except AccsNotExist:
        raise AccsNotExist()
    except Exception:
        raise UnhandledException()


@router.get(
    "/v1/account-management/accounts/",
    response_model=s_accounts.AccountsPagResponse,
    status_code=status.HTTP_200_OK,
)
async def get_accounts(
    request: Request,
    response: Response,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """get all accounts"""
    try:
        async with db.begin():
            offset = pagination_offset(page=page, limit=limit)
            _ = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            total_count = await serv_acc_r.get_account_ct(db=db)
            accounts = await serv_acc_r.get_accounts(db=db, offset=offset, limit=limit)
            return {
                "total": total_count,
                "page": page,
                "limit": limit,
                "has_more": total_count > (page * limit),
                "accounts": accounts,
            }
    except AccsNotExist:
        raise AccsNotExist()
    except Exception:
        raise UnhandledException()


@router.post(
    "/v1/account-management/accounts/",
    response_model=s_accounts.AccountsResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_account(
    request: Request,
    response: Response,
    account_data: s_accounts.AccountsCreate,
    db: AsyncSession = Depends(get_db),
):
    """create one account"""
    try:
        async with db.begin():
            sys_user = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            SetSys.sys_created_by(data=account_data, sys_user=sys_user)
            account = await serv_acc_c.create_account(account_data=account_data, db=db)
            return account
    except Exception:
        raise UnhandledException()


@router.put(
    "/v1/account-management/accounts/{account_uuid}/",
    response_model=s_accounts.AccountsResponse,
    status_code=status.HTTP_200_OK,
)
async def update_account(
    request: Request,
    response: Response,
    account_uuid: UUID4,
    account_data: s_accounts.AccountsUpdate,
    db: AsyncSession = Depends(get_db),
):
    """update one account"""
    try:
        async with db.begin():
            sys_user = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            SetSys.sys_updated_by(data=account_data, sys_user=sys_user)
            account = await serv_acc_u.update_account(
                account_uuid=account_uuid, account_data=account_data, db=db
            )
            return account
    except AccsNotExist:
        raise AccsNotExist()
    except Exception:
        raise UnhandledException()


@router.delete(
    "/v1/account-management/accounts/{account_uuid}/",
    response_model=s_accounts.AccountsDelResponse,
    status_code=status.HTTP_200_OK,
)
async def soft_del_account(
    request: Request,
    response: Response,
    account_uuid: UUID4,
    account_data: s_accounts.AccountsDel,
    db: AsyncSession = Depends(get_db),
):
    """soft del one account"""
    try:
        async with db.begin():
            sys_user = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            SetSys.sys_deleted_by(data=account_data, sys_user=sys_user)
            account = await serv_acc_d.sof_del_account(
                account_uuid=account_uuid, account_data=account_data, db=db
            )
            return account
    except AccsNotExist:
        raise AccsNotExist()
    except Exception:
        raise UnhandledException()
