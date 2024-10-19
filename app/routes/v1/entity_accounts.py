from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, Query, Request, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.database import get_db, transaction_manager
from ...exceptions import AccsNotExist, EntityAccExists, EntityAccNotExist
from ...handlers.handler import handle_exceptions
from ...schemas import accounts as s_accounts
from ...schemas import entity_accounts as s_entity_accounts
from ...services.accounts import AccountsServices
from ...services.authetication import SessionService, TokenService
from ...services.entity_accounts import EntityAccountsServices
from ...utilities.logger import logger
from ...utilities.set_values import SetField
from ...utilities.sys_users import SetSys
from ...utilities.utilities import Pagination as pg

serv_entity_accounts_r = EntityAccountsServices.ReadService()
serv_entity_accounts_c = EntityAccountsServices.CreateService()
serv_entity_accounts_u = EntityAccountsServices.UpdateService()
serv_entity_accounts_d = EntityAccountsServices.DelService()
serv_session = SessionService()
serv_token = TokenService()

serv_accounts_c = AccountsServices.CreateService()

router = APIRouter()


@router.get(
    "/v1/entity-management/entities/{entity_uuid}/entity-accounts/{entity_account_uuid}",
    response_model=s_entity_accounts.EntityAccountsResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([EntityAccNotExist])
async def get_entity_account(
    response: Response,
    entity_uuid: UUID4,
    entity_account_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_entity_accounts.EntityAccountsResponse:
    """get active account relationship"""

    async with transaction_manager(db=db):
        entity_accounts = await serv_entity_accounts_r.get_entity_account(
            entity_uuid=entity_uuid, entity_account_uuid=entity_account_uuid, db=db
        )
        return entity_accounts


@router.get(
    "/v1/entity-management/entities/{entity_uuid}/entity-accounts/",
    response_model=s_entity_accounts.EntityAccountsPagResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([EntityAccNotExist])
async def get_entity_accounts(
    response: Response,
    entity_uuid: UUID4,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_entity_accounts.EntityAccountsPagResponse:
    """get all active account relationships by entity"""

    async with transaction_manager(db=db):
        offset = pg.pagination_offset(page=page, limit=limit)
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
            "has_more": pg.has_more(total_count=total_count, page=page, limit=limit),
            "entity_accounts": entity_accounts,
        }


@router.post(
    "/v1/entity-management/entities/{entity_uuid}/entity-accounts/",
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
    user_token: str = Depends(serv_session.validate_session),
) -> s_entity_accounts.EntityAccountsResponse:
    """create new account relationship with existing account"""

    # TODO: Debug this...
    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_created_by(sys_user=sys_user, data=entity_account_data)
        entity_account = await serv_entity_accounts_c.create_entity_account(
            entity_uuid=entity_uuid, entity_account_data=entity_account_data, db=db
        )
        return entity_account


@router.post(
    "/v1/entity-management/entities/{entity_uuid}/entity-accounts/new-account/",
    response_model=s_entity_accounts.EntityAccountsResponse,
    status_code=status.HTTP_201_CREATED,
)
@serv_token.set_auth_cookie
# @handle_exceptions([AccsNotExist, EntityAccNotExist, EntityAccExists])
async def create_entity_account_account(
    response: Response,
    entity_uuid: UUID4,
    account_data: s_accounts.AccountsCreate,
    entity_account_data: s_entity_accounts.EntityAccountsAccountCreate,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_entity_accounts.EntityAccountsResponse:
    """create new account relationship with no existing account"""

    # TODO: Debug this to see why it is failing at the database operation layer
    async with transaction_manager(db=db):
        sys_user, token = user_token
        SetSys.sys_created_by(data=entity_account_data, sys_user=sys_user)
        account = await serv_accounts_c.create_account(account_data=account_data, db=db)
        account_resp = s_accounts.AccountsResponse.model_validate(obj=account)
        await db.flush()

        SetField.set_field(
            old_value=account_data.sys_created_by, new_value=sys_user.uuid
        )

        entity_account = await serv_entity_accounts_c.create_entity_account(
            entity_uuid=entity_uuid, entity_account_data=entity_account_data, db=db
        )
        entity_account_resp = s_entity_accounts.EntityAccountsResponse.model_validate(
            entity_account
        )
        await db.flush()
        return {
            "account": account_resp,
            "entity_account": entity_account_resp,
        }


@router.put(
    "/v1/entity-management/entities/{entity_uuid}/entity-accounts/{entity_account_uuid}/",
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
    user_token: str = Depends(serv_session.validate_session),
) -> s_entity_accounts.EntityAccountsResponse:
    """update existing account relationship"""

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_updated_by(data=entity_account_data, sys_user=sys_user)
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
@serv_token.set_auth_cookie
@handle_exceptions([EntityAccNotExist])
async def soft_del_entity_account(
    response: Response,
    entity_uuid: UUID4,
    entity_account_uuid: UUID4,
    entity_account_data: s_entity_accounts.EntityAccountsDel,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_entity_accounts.EntityAccountsDelResponse:
    """soft delete account relationship"""

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_deleted_by(data=entity_account_data, sys_user=sys_user)
        entity_accounts = await serv_entity_accounts_d.soft_del_entity_account(
            entity_uuid=entity_uuid,
            entity_account_uuid=entity_account_uuid,
            entity_account_data=entity_account_data,
            db=db,
        )
        return entity_accounts
