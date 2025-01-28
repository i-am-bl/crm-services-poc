from typing import Tuple

from fastapi import APIRouter, Depends, Query, Request, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...containers.services import container as services_container
from ...database.database import get_db, transaction_manager
from ...exceptions import AccsNotExist, EntityAccNotExist, EntityNotExist
from ...handlers.handler import handle_exceptions
from ...models.sys_users import SysUsers
from ...schemas.entity_accounts import (
    AccountEntityCreate,
    EntityAccountsCreate,
    EntityAccountsDel,
    AccountEntitiesPgRes,
    EntityAccountsPgRes,
    EntityAccountsUpdate,
    EntityAccountsRes,
)
from ...services.authetication import SessionService, TokenService
from ...services import entities as entities_srvcs
from ...services import entity_accounts as entity_accounts_srvcs
from ...utilities import sys_values
from ...utilities import pagination

serv_session = SessionService()
serv_token = TokenService()
router = APIRouter()


@router.get(
    "/{account_uuid}/account-entities/{entity_account_uuid}/",
    response_model=EntityAccountsRes,
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
    user_token: Tuple[SysUsers, str] = Depends(serv_session.validate_session),
    entity_account_read_srvc: entity_accounts_srvcs.ReadSrvc = Depends(
        services_container["entity_accounts_read"]
    ),
) -> EntityAccountsRes:
    """get active account relationship"""

    async with transaction_manager(db=db):
        return await entity_account_read_srvc.get_account_entity(
            account_uuid=account_uuid, entity_account_uuid=entity_account_uuid, db=db
        )


@router.get(
    "/{account_uuid}/account-entities/",
    response_model=EntityAccountsPgRes,
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
    user_token: Tuple[SysUsers, str] = Depends(serv_session.validate_session),
    entity_account_read_srvc: entity_accounts_srvcs.ReadSrvc = Depends(
        services_container["entity_accounts_read"]
    ),
    entities_read_srvc: entities_srvcs.ReadSrvc = Depends(
        services_container["entities_read"]
    ),
) -> EntityAccountsPgRes:
    """
    Get many entities that are active on the account.
    """
    # TODO: Need an orchestrator for this
    async with transaction_manager(db=db):
        offset = pagination.page_offset(page=page, limit=limit)
        total_count = await entity_account_read_srvc.get_account_entities_ct(
            account_uuid=account_uuid, db=db
        )
        entity_accounts = await entity_account_read_srvc.get_account_entities(
            account_uuid=account_uuid, limit=limit, offset=offset, db=db
        )
        entity_uuids = []
        for value in entity_accounts:
            entity_uuids.append(value.entity_uuid)
        entities = await entities_read_srvc.get_entities_by_uuids(
            entity_uuids=entity_uuids, db=db
        )
        if not isinstance(entities, list):
            entities = [entities]

        has_more = pagination.has_more_items(
            total_count=total_count, page=page, limit=limit
        )
        return EntityAccountsPgRes(
            total=total_count,
            page=page,
            limit=limit,
            has_more=has_more,
            entities=entities,
        )


@router.post(
    "/{account_uuid}/account-entities/",
    response_model=EntityAccountsRes,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([EntityAccNotExist])
async def create_account_entity(
    response: Response,
    account_uuid: UUID4,
    entity_account_data: EntityAccountsCreate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(serv_session.validate_session),
    entity_account_create_srvc: entity_accounts_srvcs.CreateSrvc = Depends(
        services_container["entity_accounts_create"]
    ),
) -> EntityAccountsRes:
    """
    Create new account relationship with existing entity.

    This will link an existing entity to the account.
    This does not create a new entity.
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        sys_values.sys_created_by(sys_user=sys_user.uuid, data=entity_account_data)
        return await entity_account_create_srvc.create_account_entity(
            account_uuid=account_uuid, entity_account_data=entity_account_data, db=db
        )


@router.put(
    "/{account_uuid}/account-entities/{entity_account_uuid}/",
    response_model=EntityAccountsRes,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([EntityAccNotExist])
async def update_account_entity(
    response: Response,
    account_uuid: UUID4,
    entity_account_uuid: UUID4,
    entity_account_data: EntityAccountsUpdate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(serv_session.validate_session),
    entity_account_update_srvc: entity_accounts_srvcs.UpdateSrvc = Depends(
        services_container["entity_accounts_update"]
    ),
) -> EntityAccountsRes:
    """
    Update existing account entity relationship.
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        sys_values.sys_updated_by(data=entity_account_data, sys_user=sys_user.uuid)
        return await entity_account_update_srvc.update_account_entity(
            account_uuid=account_uuid,
            entity_account_uuid=entity_account_uuid,
            entity_account_data=entity_account_data,
            db=db,
        )


@router.delete(
    "/{account_uuid}/account-entities/{entity_account_uuid}/",
    response_model=None,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([EntityAccNotExist])
async def soft_del_account_entity(
    response: Response,
    account_uuid: UUID4,
    entity_account_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(serv_session.validate_session),
    entity_account_delete_srvc: entity_accounts_srvcs.DelSrvc = Depends(
        services_container["entity_accounts_delete"]
    ),
) -> None:
    """
    Soft del account relationship.

    This will remove an entity from the account.
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        entity_account_data = EntityAccountsDel()
        sys_values.sys_deleted_by(data=entity_account_data, sys_user=sys_user.uuid)
        return await entity_account_delete_srvc.soft_del_account_entity(
            account_uuid=account_uuid,
            entity_account_uuid=entity_account_uuid,
            entity_account_data=entity_account_data,
            db=db,
        )
