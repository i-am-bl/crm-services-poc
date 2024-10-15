import select
from typing import List, Optional

from fastapi import APIRouter, Depends, status, Query
from pydantic import UUID4
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

import app.schemas.accounts as s_accounts
from app.database.database import Operations, get_db
from app.services.accounts import AccountsServices
import app.models.accounts as m_accounts
from app.service_utils import pagination_offset

serv_acc_r = AccountsServices.ReadService()
serv_acc_c = AccountsServices.CreateService()
serv_acc_u = AccountsServices.UpdateService()
serv_acc_d = AccountsServices.DelService()

router = APIRouter()


@router.get(
    "/v1/account-management/accounts/{account_uuid}/",
    response_model=s_accounts.AccountsResponse,
    status_code=status.HTTP_200_OK,
)
async def get_account(account_uuid: UUID4, db: AsyncSession = Depends(get_db)):
    """get one account by account_uuid"""
    async with db.begin():
        account = await serv_acc_r.get_account(account_uuid=account_uuid, db=db)
        return account


@router.get(
    "/v1/account-management/accounts/",
    response_model=s_accounts.AccountsPagResponse,
    status_code=status.HTTP_200_OK,
)
async def get_accounts(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """get all accounts"""
    offset = pagination_offset(page=page, limit=limit)

    async with db.begin():
        total_count = await serv_acc_r.get_account_ct(db=db)
        accounts = await serv_acc_r.get_accounts(db=db, offset=offset, limit=limit)
        return {
            "total": total_count,
            "page": page,
            "limit": limit,
            "has_more": total_count > (page * limit),
            "accounts": accounts,
        }


@router.post(
    "/v1/account-management/accounts/",
    # response_model=s_accounts.AccountsResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_account(
    account_data: s_accounts.AccountsCreate, db: AsyncSession = Depends(get_db)
):
    """create one account"""
    async with db.begin():
        account = await serv_acc_c.create_account(account_data=account_data, db=db)
        return account


@router.put(
    "/v1/account-management/accounts/{account_uuid}/",
    response_model=s_accounts.AccountsResponse,
    status_code=status.HTTP_200_OK,
)
async def update_account(
    account_uuid: UUID4,
    account_data: s_accounts.AccountsUpdate,
    db: AsyncSession = Depends(get_db),
):
    """update one account"""
    async with db.begin():
        account = await serv_acc_u.update_account(
            account_uuid=account_uuid, account_data=account_data, db=db
        )
        return account


@router.delete(
    "/v1/account-management/accounts/{account_uuid}/",
    response_model=s_accounts.AccountsDelResponse,
    status_code=status.HTTP_200_OK,
)
async def soft_del_account(
    account_uuid: UUID4,
    account_data: s_accounts.AccountsDel,
    db: AsyncSession = Depends(get_db),
):
    """soft del one account"""
    async with db.begin():
        account = await serv_acc_d.sof_del_account(
            account_uuid=account_uuid, account_data=account_data, db=db
        )
        return account
