from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, Query, Request, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.database import get_db
from ...schemas import accounts as s_accounts
from ...schemas import entity_accounts as s_entity_accounts
from ...services.accounts import AccountsServices
from ...services.authetication import SessionService
from ...services.entity_accounts import EntityAccountsServices
from ...utilities.logger import logger
from ...utilities.service_utils import pagination_offset
from ...utilities.sys_users import SetSys
from ...utilities.set_values import SetField
from ...exceptions import UnhandledException, EntityAccNotExist, EntityAccExists

serv_entity_accounts_r = EntityAccountsServices.ReadService()
serv_entity_accounts_c = EntityAccountsServices.CreateService()
serv_entity_accounts_u = EntityAccountsServices.UpdateService()
serv_entity_accounts_d = EntityAccountsServices.DelService()
serv_session = SessionService()

serv_accounts_c = AccountsServices.CreateService()

router = APIRouter()


@router.get(
    "/v1/entity-management/entities/{entity_uuid}/entity-accounts/{entity_account_uuid}",
    response_model=s_entity_accounts.EntityAccountsResponse,
    status_code=status.HTTP_200_OK,
)
async def get_entity_account(
    request: Request,
    response: Response,
    entity_uuid: UUID4,
    entity_account_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
):
    """get active account relationship"""
    try:
        async with db.begin():
            _ = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            entity_accounts = await serv_entity_accounts_r.get_entity_account(
                entity_uuid=entity_uuid, entity_account_uuid=entity_account_uuid, db=db
            )
            return entity_accounts
    except EntityAccNotExist:
        raise EntityAccNotExist()
    except Exception:
        raise UnhandledException()


@router.get(
    "/v1/entity-management/entities/{entity_uuid}/entity-accounts/",
    response_model=s_entity_accounts.EntityAccountsPagResponse,
    status_code=status.HTTP_200_OK,
)
async def get_entity_accounts(
    request: Request,
    response: Response,
    entity_uuid: UUID4,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """get all active account relationships by entity"""
    try:
        async with db.begin():
            _ = await serv_session.validate_session(
                request=request, response=response, db=db
            )
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
    except EntityAccNotExist:
        raise EntityAccNotExist()
    except Exception:
        raise UnhandledException()


@router.post(
    "/v1/entity-management/entities/{entity_uuid}/entity-accounts/",
    response_model=s_entity_accounts.EntityAccountsResponse,
    status_code=status.HTTP_200_OK,
)
async def create_entity_account(
    request: Request,
    response: Response,
    entity_uuid: UUID4,
    entity_account_data: s_entity_accounts.EntityAccountsCreate,
    db: AsyncSession = Depends(get_db),
):
    """create new account relationship with existing account"""

    try:
        async with db.begin():
            entity_account = await serv_entity_accounts_c.create_entity_account(
                entity_uuid=entity_uuid, entity_account_data=entity_account_data, db=db
            )
            return entity_account
    except EntityAccExists:
        raise EntityAccExists()
    except Exception:
        raise UnhandledException()


@router.post(
    "/v1/entity-management/entities/{entity_uuid}/entity-accounts/new-account/",
    response_model=s_entity_accounts.EntityAccountsResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_entity_account_account(
    request: Request,
    response: Response,
    entity_uuid: UUID4,
    account_data: s_accounts.AccountsCreate,
    entity_account_data: s_entity_accounts.EntityAccountsAccountCreate,
    db: AsyncSession = Depends(get_db),
):
    """create new account relationship with no existing account"""
    try:
        async with db.begin():
            sys_user = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            SetSys.sys_created_by(data=entity_account_data, sys_user=sys_user)
            account = await serv_accounts_c.create_account(
                account_data=account_data, db=db
            )
            await db.flush()

            account_respone = s_accounts.AccountsResponse.model_validate(obj=account)

            SetField.set_field(
                old_value=entity_account_data.account_uuid, new_value=account.uuid
            )

            entity_account = await serv_entity_accounts_c.create_entity_account(
                entity_uuid=entity_uuid, entity_account_data=entity_account_data, db=db
            )

            await db.flush()
            entity_account_response = (
                s_entity_accounts.EntityAccountsResponse.model_validate(entity_account)
            )

            return {
                "account": account_respone,
                "entity_account": entity_account_response,
            }
    except EntityAccNotExist:
        raise EntityAccNotExist()
    except EntityAccExists:
        raise EntityAccExists()
    except Exception:
        raise UnhandledException()


@router.put(
    "/v1/entity-management/entities/{entity_uuid}/entity-accounts/{entity_account_uuid}/",
    response_model=s_entity_accounts.EntityAccountsResponse,
    status_code=status.HTTP_200_OK,
)
async def update_entity_account(
    request: Request,
    response: Response,
    entity_uuid: UUID4,
    entity_account_uuid: UUID4,
    entity_account_data: s_entity_accounts.EntityAccountsUpdate,
    db: AsyncSession = Depends(get_db),
):
    """update existing account relationship"""
    try:
        async with db.begin():
            sys_user = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            SetSys.sys_updated_by(data=entity_account_data, sys_user=sys_user)
            entity_account = await serv_entity_accounts_u.update_entity_account(
                entity_uuid=entity_uuid,
                entity_account_uuid=entity_account_uuid,
                entity_account_data=entity_account_data,
                db=db,
            )
            return entity_account
    except EntityAccNotExist:
        raise EntityAccNotExist()
    except Exception:
        raise UnhandledException()


@router.delete(
    "/v1/entity-management/entities/{entity_uuid}/entity-accounts/{entity_account_uuid}/",
    response_model=s_entity_accounts.EntityAccountsDelResponse,
    status_code=status.HTTP_200_OK,
)
async def soft_del_entity_account(
    request: Request,
    response: Response,
    entity_uuid: UUID4,
    entity_account_uuid: UUID4,
    entity_account_data: s_entity_accounts.EntityAccountsDel,
    db: AsyncSession = Depends(get_db),
):
    """soft delete account relationship"""
    try:
        async with db.begin():
            sys_user = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            SetSys.sys_deleted_by(data=entity_account_data, sys_user=sys_user)
            entity_accounts = await serv_entity_accounts_d.soft_del_entity_account(
                entity_uuid=entity_uuid,
                entity_account_uuid=entity_account_uuid,
                entity_account_data=entity_account_data,
                db=db,
            )
            return entity_accounts
    except EntityAccNotExist:
        raise EntityAccNotExist()
    except Exception:
        raise UnhandledException()
