from typing import Tuple

from fastapi import APIRouter, Depends, Query, Request, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...containers.services import container as services_container
from ...database.database import get_db, transaction_manager
from ...exceptions import (
    AccsExists,
    AccsNotExist,
    EntityAccExists,
    EntityAccNotExist,
    EntityNotExist,
)
from ...handlers.handler import handle_exceptions
from ...models.sys_users import SysUsers
from ...schemas.accounts import AccountsCreate
from ...schemas.entity_accounts import AccountEntityCreate, EntityAccountsCreate, EntityAccountsDel, EntityAccountsPgRes, EntityAccountsUpdate,EntityAccountsRes,  
from ...services import accounts as accounts_srvcs
from ...services.authetication import SessionService, TokenService
from ...services import entities as entities_srvcs
from ...services import entity_accounts as entity_accounts_srvcs  
from ...utilities import pagination
from ...utilities.set_values import SetField
from ...utilities import sys_values

serv_session = SessionService()
serv_token = TokenService()
router = APIRouter()


@router.get(
    "/{entity_uuid}/entity-accounts/{entity_account_uuid}/",
    response_model=EntityAccountsRes,
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
    user_token: Tuple[SysUsers, str] = Depends(serv_session.validate_session),
    entity_accounts_read_srvc:entity_accounts_srvcs.ReadSrvc=Depends(services_container["entity_accounts_read"])
) -> EntityAccountsRes:
    """get active account relationship"""

    async with transaction_manager(db=db):
        return await entity_accounts_read_srvc.get_entity_account(
            entity_uuid=entity_uuid, entity_account_uuid=entity_account_uuid, db=db
        )


@router.get(
    "/{entity_uuid}/entity-accounts/",
    response_model=EntityAccountsPgRes,
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
    user_token: Tuple[SysUsers, str] = Depends(serv_session.validate_session),
    entity_accounts_read_srvc:entity_accounts_srvcs.ReadSrvc=Depends(services_container["entity_accounts_read"]),
    accounts_read_srvc:accounts_srvcs.ReadSrvc=Depends(services_container["accounts_read"])
) -> EntityAccountsPgRes:
    """
    Get many active account relationships by entity.

    This will return a paginated result of accounts the entity is linked to.
    """

    async with transaction_manager(db=db):
        # TODO: need an orchestrator for this
        offset = pagination.page_offset(page=page, limit=limit)
        total_count = await entity_accounts_read_srvc.get_entity_accounts_ct(
            entity_uuid=entity_uuid, db=db
        )
        entity_accounts = await entity_accounts_read_srvc.get_entity_accounts(
            entity_uuid=entity_uuid, limit=limit, offset=offset, db=db
        )
        account_uuids = []
        for value in entity_accounts:
            account_uuids.append(value.account_uuid)
        accounts = await accounts_read_srvc.get_accounts_by_uuids(
            account_uuids=account_uuids, db=db
        )
        if not isinstance(accounts, list):
            accounts = [accounts]
        has_more = pagination.has_more_items(total_count=total_count, page=page, limit=limit)
        return EntityAccountsPgRes(
            total=total_count,
            page=page,
            limit=limit,
            has_more=has_more,
            accounts=accounts,
        )


@router.post(
    "/{entity_uuid}/entity-accounts/",
    response_model=EntityAccountsRes,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([EntityAccNotExist])
async def create_entity_account(
    response: Response,
    entity_uuid: UUID4,
    entity_account_data: EntityAccountsCreate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(serv_session.validate_session),
    entity_accounts_create_srvc:entity_accounts_srvcs.CreateSrvc=Depends(services_container["entity_accounts_create"])
) -> EntityAccountsRes:
    """
    create new account relationship with existing account.

    This adds an entity to an active account.
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        sys_values.sys_created_by(sys_user=sys_user, data=entity_account_data)
        return await entity_accounts_create_srvc.create_entity_account(
            entity_uuid=entity_uuid, entity_account_data=entity_account_data, db=db
        )


@router.post(
    "/{entity_uuid}/entity-accounts/new-account/",
    response_model=EntityAccountsRes,
    status_code=status.HTTP_201_CREATED,
)
@serv_token.set_auth_cookie
@handle_exceptions([AccsExists, EntityAccNotExist, EntityAccExists])
async def create_entity_account_account(
    response: Response,
    entity_uuid: UUID4,
    account_data: AccountsCreate,
    entity_account_data: AccountEntityCreate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(serv_session.validate_session),
    entity_accounts_create_srvc:entity_accounts_srvcs.CreateSrvc=Depends(services_container["entity_accounts_create"]),
    accounts_create_srvc:accounts_srvcs.CreateSrvc=Depends(services_container["accounts_create"])
) -> EntityAccountsRes:
    """
    Create new account relationship with no existing account.

    A new account can be created from the context of the entity.
    """

    async with transaction_manager(db=db):
        # TODO: need an orchestrator for this
        sys_user, token = user_token
        sys_values.sys_created_by(data=account_data, sys_user=sys_user.uuid)
        account = await accounts_create_srvc.create_account(account_data=account_data, db=db)
        await db.flush()

        sys_values.sys_created_by(data=entity_account_data, sys_user=sys_user.uuid)
        SetField.set_field_value(
            field="account_uuid", value=account.uuid, data=entity_account_data
        )
        entity_account = await entity_accounts_create_srvc.create_entity_account(
            entity_uuid=entity_uuid, entity_account_data=entity_account_data, db=db
        )
        await db.flush()
        return EntityAccountsRes(
            account=account, entity_account=entity_account
        )


@router.put(
    "/{entity_uuid}/entity-accounts/{entity_account_uuid}/",
    response_model=EntityAccountsRes,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([EntityAccNotExist])
async def update_entity_account(
    response: Response,
    entity_uuid: UUID4,
    entity_account_uuid: UUID4,
    entity_account_data: EntityAccountsUpdate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(serv_session.validate_session),
    entity_accounts_update_srvc:entity_accounts_srvcs.UpdateSrvc=Depends(services_container["entity_accounts_update"])
) -> EntityAccountsRes:
    """
    Update existing account relationship.
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        sys_values.sys_updated_by(data=entity_account_data, sys_user=sys_user.uuid)
        return await entity_accounts_update_srvc.update_entity_account(
            entity_uuid=entity_uuid,
            entity_account_uuid=entity_account_uuid,
            entity_account_data=entity_account_data,
            db=db,
        )


@router.delete(
    "/v1/entity-management/entities/{entity_uuid}/entity-accounts/{entity_account_uuid}/",
    response_model=None,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([EntityAccNotExist])
async def soft_del_entity_account(
    response: Response,
    entity_uuid: UUID4,
    entity_account_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(serv_session.validate_session),
    entity_accounts_update_srvc:entity_accounts_srvcs.DelSrvc=Depends(services_container["entity_accounts_update"])
) -> None:
    """
    Soft delete account relationship with entity.

    This will remove the entity from an active account.
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        entity_account_data = EntityAccountsDel()
        sys_values.sys_deleted_by(data=entity_account_data, sys_user=sys_user.uuid)
        return await entity_accounts_update_srvc.soft_del_entity_account(
            entity_uuid=entity_uuid,
            entity_account_uuid=entity_account_uuid,
            entity_account_data=entity_account_data,
            db=db,
        )
