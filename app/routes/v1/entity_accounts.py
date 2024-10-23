from typing import Tuple

from fastapi import APIRouter, Depends, Query, Request, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.database import get_db, transaction_manager
from ...exceptions import (AccsExists, AccsNotExist, EntityAccExists,
                           EntityAccNotExist, EntityNotExist)
from ...handlers.handler import handle_exceptions
from ...schemas import accounts as s_accounts
from ...schemas import entity_accounts as s_entity_accounts
from ...services.accounts import AccountsServices
from ...services.authetication import SessionService, TokenService
from ...services.entities import EntitiesServices
from ...services.entity_accounts import EntityAccountsServices
from ...utilities.logger import logger
from ...utilities.set_values import SetField, SetSys
from ...utilities.utilities import Pagination as pg

serv_entity_accounts_r = EntityAccountsServices.ReadService()
serv_entity_accounts_c = EntityAccountsServices.CreateService()
serv_entity_accounts_u = EntityAccountsServices.UpdateService()
serv_entity_accounts_d = EntityAccountsServices.DelService()
serv_accounts_c = AccountsServices.CreateService()
serv_accounts_r = AccountsServices.ReadService()
serv_session = SessionService()
serv_token = TokenService()
router = APIRouter()


@router.get(
    "/{entity_uuid}/entity-accounts/{entity_account_uuid}/",
    response_model=s_entity_accounts.EntityAccountsResponse,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
@serv_token.set_auth_cookie
@handle_exceptions([EntityAccNotExist])
async def get_entity_account(
    response: Response,
    entity_uuid: UUID4,
    entity_account_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_entity_accounts.EntityAccountsResponse:
    """get active account relationship"""

    async with transaction_manager(db=db):
        return await serv_entity_accounts_r.get_entity_account(
            entity_uuid=entity_uuid, entity_account_uuid=entity_account_uuid, db=db
        )


@router.get(
    "/{entity_uuid}/entity-accounts/",
    response_model=s_entity_accounts.EntityAccountsPagResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([EntityAccNotExist, EntityNotExist, AccsNotExist])
async def get_entity_accounts(
    response: Response,
    entity_uuid: UUID4,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_entity_accounts.EntityAccountsPagResponse:
    """
    Get many active account relationships by entity.

    This will return a paginated result of accounts the entity is linked to.
    """

    async with transaction_manager(db=db):
        offset = pg.pagination_offset(page=page, limit=limit)
        total_count = await serv_entity_accounts_r.get_entity_accounts_ct(
            entity_uuid=entity_uuid, db=db
        )
        entity_accounts = await serv_entity_accounts_r.get_entity_accounts(
            entity_uuid=entity_uuid, limit=limit, offset=offset, db=db
        )
        account_uuids = []
        for value in entity_accounts:
            account_uuids.append(value.account_uuid)
        accounts = await serv_accounts_r.get_accounts_by_uuids(
            account_uuids=account_uuids, db=db
        )
        if not isinstance(accounts, list):
            accounts = [accounts]
        has_more = pg.has_more(total_count=total_count, page=page, limit=limit)
        return s_entity_accounts.EntityAccountsPagResponse(
            total=total_count,
            page=page,
            limit=limit,
            has_more=has_more,
            accounts=accounts,
        )


@router.post(
    "/{entity_uuid}/entity-accounts/",
    response_model=s_entity_accounts.EntityAccountsResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([EntityAccNotExist])
async def create_entity_account(
    response: Response,
    entity_uuid: UUID4,
    entity_account_data: s_entity_accounts.EntityAccountsCreate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_entity_accounts.EntityAccountsResponse:
    """
    create new account relationship with existing account.

    This adds an entity to an active account.
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_created_by(sys_user=sys_user, data=entity_account_data)
        return await serv_entity_accounts_c.create_entity_account(
            entity_uuid=entity_uuid, entity_account_data=entity_account_data, db=db
        )


@router.post(
    "/{entity_uuid}/entity-accounts/new-account/",
    response_model=s_entity_accounts.EntityAccountAccountRespone,
    status_code=status.HTTP_201_CREATED,
)
@serv_token.set_auth_cookie
@handle_exceptions([AccsExists, EntityAccNotExist, EntityAccExists])
async def create_entity_account_account(
    response: Response,
    entity_uuid: UUID4,
    account_data: s_accounts.AccountsCreate,
    entity_account_data: s_entity_accounts.EntityAccountsAccountCreate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_entity_accounts.EntityAccountAccountRespone:
    """
    Create new account relationship with no existing account.

    A new account can be created from the context of the entity.
    """

    async with transaction_manager(db=db):
        sys_user, token = user_token
        SetSys.sys_created_by(data=account_data, sys_user=sys_user)
        account = await serv_accounts_c.create_account(account_data=account_data, db=db)
        await db.flush()

        SetSys.sys_created_by(data=entity_account_data, sys_user=sys_user)
        SetField.set_field_value(
            field="account_uuid", value=account.uuid, data=entity_account_data
        )
        entity_account = await serv_entity_accounts_c.create_entity_account(
            entity_uuid=entity_uuid, entity_account_data=entity_account_data, db=db
        )
        await db.flush()
        return s_entity_accounts.EntityAccountAccountRespone(
            account=account, entity_account=entity_account
        )


@router.put(
    "/{entity_uuid}/entity-accounts/{entity_account_uuid}/",
    response_model=s_entity_accounts.EntityAccountsResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([EntityAccNotExist])
async def update_entity_account(
    response: Response,
    entity_uuid: UUID4,
    entity_account_uuid: UUID4,
    entity_account_data: s_entity_accounts.EntityAccountsUpdate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_entity_accounts.EntityAccountsResponse:
    """
    Update existing account relationship.
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_updated_by(data=entity_account_data, sys_user=sys_user)
        return await serv_entity_accounts_u.update_entity_account(
            entity_uuid=entity_uuid,
            entity_account_uuid=entity_account_uuid,
            entity_account_data=entity_account_data,
            db=db,
        )


@router.delete(
    "/v1/entity-management/entities/{entity_uuid}/entity-accounts/{entity_account_uuid}/",
    response_model=s_entity_accounts.EntityAccountsDelResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([EntityAccNotExist])
async def soft_del_entity_account(
    response: Response,
    entity_uuid: UUID4,
    entity_account_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_entity_accounts.EntityAccountsDelResponse:
    """
    Soft delete account relationship with entity.

    This will remove the entity from an active account.
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        entity_account_data = s_entity_accounts.EntityAccountsDel()
        SetSys.sys_deleted_by(data=entity_account_data, sys_user=sys_user)
        return await serv_entity_accounts_d.soft_del_entity_account(
            entity_uuid=entity_uuid,
            entity_account_uuid=entity_account_uuid,
            entity_account_data=entity_account_data,
            db=db,
        )
