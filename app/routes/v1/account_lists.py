from typing import List

from fastapi import APIRouter, Depends, status, Query
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

import app.schemas.account_lists as s_account_lists
from app.database.database import Operations, get_db
from app.services.account_lists import AccountListsServices
from app.service_utils import pagination_offset

serv_acc_ls_r = AccountListsServices.ReadService()
serv_acc_ls_c = AccountListsServices.CreateService()
serv_acc_ls_u = AccountListsServices.UpdateService()
serv_acc_ls_d = AccountListsServices.DelService()

router = APIRouter()


@router.get(
    "/v1/account-management/accounts/{account_uuid}/account-lists/{account_list_uuid}/",
    response_model=s_account_lists.AccountListsResponse,
    status_code=status.HTTP_200_OK,
)
async def get_account_list(
    account_uuid: UUID4, account_list_uuid: UUID4, db: AsyncSession = Depends(get_db)
):
    """get one account list"""
    async with db.begin():
        account_list = await serv_acc_ls_r.get_account_list(
            account_uuid=account_uuid, account_list_uuid=account_list_uuid, db=db
        )
        return account_list


@router.get(
    "/v1/account-management/accounts/{account_uuid}/account-lists/",
    response_model=s_account_lists.AccountListsPagResponse,
    status_code=status.HTTP_200_OK,
)
async def get_account_lists(
    account_uuid: UUID4,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """get all account lists by account"""
    async with db.begin():
        offset = pagination_offset(page=page, limit=limit)
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
            "has_more": total_count > (page * limit),
            "account_lists": account_lists,
        }


@router.post(
    "/v1/account-management/accounts/{account_uuid}/account-lists/",
    response_model=s_account_lists.AccountListsResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_account_list(
    account_uuid: UUID4,
    account_list_data: s_account_lists.AccountListsCreate,
    db: AsyncSession = Depends(get_db),
):
    """create one account list"""
    async with db.begin():
        account_list = await serv_acc_ls_c.create_account_list(
            account_uuid=account_uuid, account_list_data=account_list_data, db=db
        )
        return account_list


@router.put(
    "/v1/account-management/accounts/{account_uuid}/account-lists/{account_list_uuid}/",
    response_model=s_account_lists.AccountListsResponse,
    status_code=status.HTTP_200_OK,
)
async def update_account_list(
    account_uuid: UUID4,
    account_list_uuid: UUID4,
    account_list_data: s_account_lists.AccountListsUpdate,
    db: AsyncSession = Depends(get_db),
):
    """update one account list"""
    async with db.begin():
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
async def soft_del_account_list(
    account_uuid: UUID4,
    account_list_uuid: UUID4,
    account_list_data: s_account_lists.AccountListsDel,
    db: AsyncSession = Depends(get_db),
):
    """soft delete one account list"""
    async with db.begin():
        account_list = await serv_acc_ls_d.soft_del_account_list(
            account_uuid=account_uuid,
            account_list_uuid=account_list_uuid,
            account_list_data=account_list_data,
            db=db,
        )
        return account_list
