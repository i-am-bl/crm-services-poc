from typing import Tuple

from fastapi import APIRouter, Depends, Query, Request, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...containers.orchestrators import container as orchs_container
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
from ...orchestrators.entity_accounts import (
    EntityAccountsReadOrch,
    EntityAccountsCreateOrch,
)
from ...schemas.accounts import AccountsCreate, AccountsInternalCreate
from ...schemas.entity_accounts import (
    AccountEntityCreate,
    EntityAccountParentRes,
    EntityAccountsCreate,
    EntityAccountsDel,
    EntityAccountsInternalCreate,
    EntityAccountsInternalUpdate,
    EntityAccountsPgRes,
    EntityAccountsUpdate,
    EntityAccountsRes,
)
from ...services import entity_accounts as entity_accounts_srvcs
from ...services.token import set_auth_cookie
from ...utilities import sys_values
from ...utilities.auth import get_validated_session
from ...utilities.data import internal_schema_validation

router = APIRouter()


@router.get(
    "/{entity_uuid}/entity-accounts/{entity_account_uuid}/",
    response_model=EntityAccountsRes,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
@set_auth_cookie
@handle_exceptions([EntityAccNotExist])
async def get_entity_account(
    response: Response,
    entity_uuid: UUID4,
    entity_account_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    entity_accounts_read_srvc: entity_accounts_srvcs.ReadSrvc = Depends(
        services_container["entity_accounts_read"]
    ),
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
@set_auth_cookie
@handle_exceptions([EntityAccNotExist, EntityNotExist, AccsNotExist])
async def get_entity_accounts(
    response: Response,
    entity_uuid: UUID4,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    entity_accounts_read_orch: EntityAccountsReadOrch = Depends(
        orchs_container["entity_accounts_read_orch"]
    ),
) -> EntityAccountsPgRes:
    """
    Get many active account relationships by entity.

    This will return a paginated result of accounts the entity is linked to.
    """

    async with transaction_manager(db=db):
        return await entity_accounts_read_orch.paginated_entity_accounts(
            entity_uuid=entity_uuid, page=page, limit=limit, db=db
        )


@router.post(
    "/{entity_uuid}/entity-accounts/",
    response_model=EntityAccountsRes,
    status_code=status.HTTP_200_OK,
)
@set_auth_cookie
@handle_exceptions([EntityAccNotExist])
async def create_entity_account(
    response: Response,
    entity_uuid: UUID4,
    entity_account_data: EntityAccountsCreate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    entity_accounts_create_srvc: entity_accounts_srvcs.CreateSrvc = Depends(
        services_container["entity_accounts_create"]
    ),
) -> EntityAccountsRes:
    """
    create new account relationship with existing account.

    This adds an entity to an active account.
    """
    sys_user, _ = user_token
    _entity_account_data: EntityAccountsInternalCreate = internal_schema_validation(
        data=entity_account_data,
        schema=EntityAccountsInternalCreate,
        setter_method=sys_values.sys_created_by,
        sys_user_uuid=sys_user.uuid,
    )
    async with transaction_manager(db=db):
        return await entity_accounts_create_srvc.create_entity_account(
            entity_uuid=entity_uuid, entity_account_data=_entity_account_data, db=db
        )


@router.post(
    "/{entity_uuid}/entity-accounts/new-account/",
    response_model=EntityAccountsRes,
    status_code=status.HTTP_201_CREATED,
)
@set_auth_cookie
@handle_exceptions([AccsExists, EntityAccNotExist, EntityAccExists])
async def create_entity_account_account(
    response: Response,
    entity_uuid: UUID4,
    account_data: AccountsCreate,
    entity_account_data: AccountEntityCreate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    entity_accounts_read_orch: EntityAccountsCreateOrch = Depends(
        orchs_container["entity_accounts_create_orch"]
    ),
) -> EntityAccountsRes:
    """
    Create new account relationship with no existing account.

    A new account can be created from the context of the entity.
    """

    sys_user, _ = user_token
    _account_data: AccountsInternalCreate = internal_schema_validation(
        data=account_data,
        schema=AccountsInternalCreate,
        setter_method=sys_values.sys_created_by,
        sys_user_uuid=sys_user.uuid,
    )
    _entity_account_data: EntityAccountsInternalCreate = internal_schema_validation(
        data=entity_account_data,
        schema=EntityAccountsInternalCreate,
        setter_method=sys_values.sys_created_by,
        sys_user_uuid=sys_user.uuid,
    )
    async with transaction_manager(db=db):

        return await entity_accounts_read_orch.create_account(
            entity_uuid=entity_uuid,
            account_data=_account_data,
            entity_account_data=_entity_account_data,
            db=db,
        )


@router.put(
    "/{entity_uuid}/entity-accounts/{entity_account_uuid}/",
    response_model=EntityAccountsRes,
    status_code=status.HTTP_200_OK,
)
@set_auth_cookie
@handle_exceptions([EntityAccNotExist])
async def update_entity_account(
    response: Response,
    entity_uuid: UUID4,
    entity_account_uuid: UUID4,
    entity_account_data: EntityAccountsUpdate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    entity_accounts_update_srvc: entity_accounts_srvcs.UpdateSrvc = Depends(
        services_container["entity_accounts_update"]
    ),
) -> EntityAccountsRes:
    """
    Update existing account relationship.
    """

    sys_user, _ = user_token
    _entity_account_data: EntityAccountsInternalUpdate = internal_schema_validation(
        data=entity_account_data,
        schema=EntityAccountsInternalUpdate,
        setter_method=sys_values.sys_updated_by,
        sys_user_uuid=sys_user.uuid,
    )
    async with transaction_manager(db=db):

        return await entity_accounts_update_srvc.update_entity_account(
            entity_uuid=entity_uuid,
            entity_account_uuid=entity_account_uuid,
            entity_account_data=_entity_account_data,
            db=db,
        )


@router.delete(
    "/v1/entity-management/entities/{entity_uuid}/entity-accounts/{entity_account_uuid}/",
    response_model=None,
    status_code=status.HTTP_200_OK,
)
@set_auth_cookie
@handle_exceptions([EntityAccNotExist])
async def soft_del_entity_account(
    response: Response,
    entity_uuid: UUID4,
    entity_account_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    entity_accounts_update_srvc: entity_accounts_srvcs.DelSrvc = Depends(
        services_container["entity_accounts_update"]
    ),
) -> None:
    """
    Soft delete account relationship with entity.

    This will remove the entity from an active account.
    """
    sys_user, _ = user_token
    _entity_account_data: EntityAccountsDel = internal_schema_validation(
        schema=EntityAccountsDel,
        setter_method=sys_values.sys_deleted_by,
        sys_user_uuid=sys_user.uuid,
    )
    async with transaction_manager(db=db):

        return await entity_accounts_update_srvc.soft_del_entity_account(
            entity_uuid=entity_uuid,
            entity_account_uuid=entity_account_uuid,
            entity_account_data=_entity_account_data,
            db=db,
        )
