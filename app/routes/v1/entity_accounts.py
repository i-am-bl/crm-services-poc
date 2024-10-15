from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

import app.schemas.accounts as s_accounts
import app.schemas.entity_accounts as s_entity_accounts
from app.database.database import Operations, get_db
from app.logger import logger
from app.services.accounts import AccountsServices
from app.services.entity_accounts import EntityAccountsServices
from app.service_utils import pagination_offset

serv_entity_accounts_r = EntityAccountsServices.ReadService()
serv_entity_accounts_c = EntityAccountsServices.CreateService()
serv_entity_accounts_u = EntityAccountsServices.UpdateService()
serv_entity_accounts_d = EntityAccountsServices.DelService()

serv_accounts_c = AccountsServices.CreateService()

router = APIRouter()


@router.get(
    "/v1/entity-management/entities/{entity_uuid}/entity-accounts/{entity_account_uuid}",
    response_model=s_entity_accounts.EntityAccountsResponse,
    status_code=status.HTTP_200_OK,
)
async def get_entity_account(
    entity_uuid: UUID4, entity_account_uuid: UUID4, db: AsyncSession = Depends(get_db)
):
    """get active account relationship"""
    async with db.begin():
        entity_accounts = await serv_entity_accounts_r.get_entity_account(
            entity_uuid=entity_uuid, entity_account_uuid=entity_account_uuid, db=db
        )
        return entity_accounts


@router.get(
    "/v1/entity-management/entities/{entity_uuid}/entity-accounts/",
    response_model=s_entity_accounts.EntityAccountsPagResponse,
    status_code=status.HTTP_200_OK,
)
async def get_entity_accounts(
    entity_uuid: UUID4,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """get all active account relationships by entity"""
    async with db.begin():
        offset = pagination_offset(page=page, limit=limit)
        total_count = await serv_entity_accounts_r.get_entity_accounts_ct(
            entity_uuid=entity_uuid, db=db
        )
        entity_accounts = await serv_entity_accounts_r.get_entity_accounts(
            entity_uuid=entity_uuid, limit=limit, offset=offset, db=db
        )
        return {
            "total": total_count,
            "page": page,
            "limit": limit,
            "has_more": total_count > (page * limit),
            "entity_accounts": entity_accounts,
        }


@router.post(
    "/v1/entity-management/entities/{entity_uuid}/entity-accounts/",
    response_model=s_entity_accounts.EntityAccountsResponse,
    status_code=status.HTTP_200_OK,
)
async def create_entity_account(
    entity_uuid: UUID4,
    entity_account_data: s_entity_accounts.EntityAccountsCreate,
    db: AsyncSession = Depends(get_db),
):
    """create new account relationship with existing account"""

    async with db.begin():
        entity_account = await serv_entity_accounts_c.create_entity_account(
            entity_uuid=entity_uuid, entity_account_data=entity_account_data, db=db
        )
        return entity_account


@router.post(
    "/v1/entity-management/entities/{entity_uuid}/entity-accounts/new-account/",
    response_model=s_entity_accounts.EntityAccountsResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_entity_account_account(
    entity_uuid: UUID4,
    account_data: s_accounts.AccountsCreate,
    entity_account_data: s_entity_accounts.EntityAccountsAccountCreate,
    db: AsyncSession = Depends(get_db),
):
    """create new account relationship with no existing account"""
    async with db.begin():
        account = await serv_accounts_c.create_account(account_data=account_data, db=db)
        await db.flush()

        account_respone = s_accounts.AccountsResponse.model_validate(obj=account)
        entity_account_data.account_id = account.id
        entity_account_data.account_uuid = account.uuid

        entity_account = await serv_entity_accounts_c.create_entity_account(
            entity_uuid=entity_uuid, entity_account_data=entity_account_data, db=db
        )

        await db.flush()
        entity_account_response = (
            s_entity_accounts.EntityAccountsResponse.model_validate(entity_account)
        )

        return {"account": account_respone, "entity_account": entity_account_response}


@router.put(
    "/v1/entity-management/entities/{entity_uuid}/entity-accounts/{entity_account_uuid}/",
    response_model=s_entity_accounts.EntityAccountsResponse,
    status_code=status.HTTP_200_OK,
)
async def update_entity_account(
    entity_uuid: UUID4,
    entity_account_uuid: UUID4,
    entity_account_data: s_entity_accounts.EntityAccountsUpdate,
    db: AsyncSession = Depends(get_db),
):
    """update existing account relationship"""
    async with db.begin():
        entity_account = await serv_entity_accounts_u.update_entity_account(
            entity_uuid=entity_uuid,
            entity_account_uuid=entity_account_uuid,
            entity_account_data=entity_account_data,
            db=db,
        )
        return entity_account


@router.delete(
    "/v1/entity-management/entities/{entity_uuid}/entity-accounts/{entity_account_uuid}/",
    response_model=s_entity_accounts.EntityAccountsDelResponse,
    status_code=status.HTTP_200_OK,
)
async def soft_del_entity_account(
    entity_uuid: UUID4,
    entity_account_uuid: UUID4,
    entity_account_data: s_entity_accounts.EntityAccountsDel,
    db: AsyncSession = Depends(get_db),
):
    """soft delete account relationship"""
    async with db.begin():
        entity_accounts = await serv_entity_accounts_d.soft_del_entity_account(
            entity_uuid=entity_uuid,
            entity_account_uuid=entity_account_uuid,
            entity_account_data=entity_account_data,
            db=db,
        )
        return entity_accounts
