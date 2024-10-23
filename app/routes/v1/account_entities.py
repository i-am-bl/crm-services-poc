from typing import Tuple

from fastapi import APIRouter, Depends, Query, Request, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.database import get_db, transaction_manager
from ...exceptions import AccsNotExist, EntityAccNotExist, EntityNotExist
from ...handlers.handler import handle_exceptions
from ...schemas import entity_accounts as s_entity_accounts
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
serv_entities_r = EntitiesServices.ReadService()
serv_session = SessionService()
serv_token = TokenService()
router = APIRouter()


@router.get(
    "/{account_uuid}/account-entities/{entity_account_uuid}/",
    response_model=s_entity_accounts.EntityAccountsResponse,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
@serv_token.set_auth_cookie
@handle_exceptions([EntityAccNotExist])
async def get_account_entity(
    response: Response,
    account_uuid: UUID4,
    entity_account_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_entity_accounts.EntityAccountsResponse:
    """get active account relationship"""

    async with transaction_manager(db=db):
        return await serv_entity_accounts_r.get_account_entity(
            account_uuid=account_uuid, entity_account_uuid=entity_account_uuid, db=db
        )


@router.get(
    "/{account_uuid}/account-entities/",
    response_model=s_entity_accounts.EntityAccountsPagResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([EntityAccNotExist, EntityNotExist, AccsNotExist])
async def get_account_entities(
    response: Response,
    account_uuid: UUID4,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_entity_accounts.EntityAccountsPagResponse:
    """
    Get many entities that are active on the account.
    """

    async with transaction_manager(db=db):
        offset = pg.pagination_offset(page=page, limit=limit)
        total_count = await serv_entity_accounts_r.get_account_entities_ct(
            account_uuid=account_uuid, db=db
        )
        entity_accounts = await serv_entity_accounts_r.get_account_entities(
            account_uuid=account_uuid, limit=limit, offset=offset, db=db
        )
        entity_uuids = []
        for value in entity_accounts:
            entity_uuids.append(value.entity_uuid)
        entities = await serv_entities_r.get_entities_by_uuids(
            entity_uuids=entity_uuids, db=db
        )
        if not isinstance(entities, list):
            entities = [entities]

        has_more = pg.has_more(total_count=total_count, page=page, limit=limit)
        return s_entity_accounts.EntityAccountsPagResponse(
            total=total_count,
            page=page,
            limit=limit,
            has_more=has_more,
            entities=entities,
        )


@router.post(
    "/{account_uuid}/account-entities/",
    response_model=s_entity_accounts.EntityAccountsResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([EntityAccNotExist])
async def create_account_entity(
    response: Response,
    account_uuid: UUID4,
    entity_account_data: s_entity_accounts.EntityAccountsCreate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_entity_accounts.EntityAccountsResponse:
    """
    Create new account relationship with existing entity.

    This will link an existing entity to the account.
    This does not create a new entity.
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_created_by(sys_user=sys_user, data=entity_account_data)
        return await serv_entity_accounts_c.create_account_entity(
            account_uuid=account_uuid, entity_account_data=entity_account_data, db=db
        )


@router.put(
    "/{account_uuid}/account-entities/{entity_account_uuid}/",
    response_model=s_entity_accounts.EntityAccountsResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([EntityAccNotExist])
async def update_account_entity(
    response: Response,
    account_uuid: UUID4,
    entity_account_uuid: UUID4,
    entity_account_data: s_entity_accounts.EntityAccountsUpdate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_entity_accounts.EntityAccountsResponse:
    """
    Update existing account entity relationship.
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_updated_by(data=entity_account_data, sys_user=sys_user)
        return await serv_entity_accounts_u.update_account_entity(
            account_uuid=account_uuid,
            entity_account_uuid=entity_account_uuid,
            entity_account_data=entity_account_data,
            db=db,
        )


@router.delete(
    "/{account_uuid}/account-entities/{entity_account_uuid}/",
    response_model=s_entity_accounts.EntityAccountsDelResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([EntityAccNotExist])
async def soft_del_account_entity(
    response: Response,
    account_uuid: UUID4,
    entity_account_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_entity_accounts.EntityAccountsDelResponse:
    """
    Soft del account relationship.

    This will remove an entity from the account.
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        entity_account_data = s_entity_accounts.EntityAccountsDel()
        SetSys.sys_deleted_by(data=entity_account_data, sys_user=sys_user)
        return await serv_entity_accounts_d.soft_del_account_entity(
            account_uuid=account_uuid,
            entity_account_uuid=entity_account_uuid,
            entity_account_data=entity_account_data,
            db=db,
        )
