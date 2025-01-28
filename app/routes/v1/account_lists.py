from typing import Tuple

from fastapi import APIRouter, Depends, Query, Request, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...containers.orchestrators import container as orchs_container
from ...containers.services import container as service_container
from ...database.database import get_db, transaction_manager
from ...exceptions import AccListExists, AccListNotExist, ProductsNotExist
from ...handlers.handler import handle_exceptions
from ...models.sys_users import SysUsers
from ...orchestrators.account_lists import AccountListsReadOrch
from ...schemas.account_lists import (
    AccountListsCreate,
    AccountListsDelRes,
    AccountListsOrchPgRes,
    AccountListsUpdate,
    AccountListsRes,
    AccountListsDel,
)
from ...services.account_lists import ReadSrvc, CreateSrvc, UpdateSrvc, DelSrvc
from ...services.authetication import SessionService, TokenService

from ...utilities import sys_values

serv_session = SessionService()
serv_token = TokenService()

router = APIRouter()


@router.get(
    "/{account_uuid}/account-lists/{account_list_uuid}/",
    response_model=AccountListsRes,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
@serv_token.set_auth_cookie
@handle_exceptions([AccListNotExist])
async def get_account_list(
    account_uuid: UUID4,
    account_list_uuid: UUID4,
    response: Response,
    user_token: Tuple[SysUsers, str] = Depends(serv_session.validate_session),
    db: AsyncSession = Depends(get_db),
    account_lists_read_srvc: ReadSrvc = Depends(
        service_container["account_lists_read"]
    ),
) -> AccountListsRes:
    """
    Get one account list.
    """

    async with transaction_manager(db=db):
        return await account_lists_read_srvc.get_account_list(
            account_uuid=account_uuid, account_list_uuid=account_list_uuid, db=db
        )


@router.get(
    "/{account_uuid}/account-lists/",
    response_model=AccountListsOrchPgRes,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([AccListNotExist, ProductsNotExist])
async def get_account_lists(
    response: Response,
    account_uuid: UUID4,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(serv_session.validate_session),
    account_lists_read_orch: AccountListsReadOrch = Depends(
        orchs_container["accounts_lists_read_orch"]
    ),
) -> AccountListsOrchPgRes:
    """
    Get many account lists by account.

    This will return the list of product lists linked to the account.
    """

    async with transaction_manager(db=db):
        return await account_lists_read_orch.paginated_product_lists(
            account_uuid=account_uuid, page=page, limit=limit, db=db
        )


@router.post(
    "/{account_uuid}/account-lists/",
    response_model=AccountListsRes,
    status_code=status.HTTP_201_CREATED,
)
@serv_token.set_auth_cookie
@handle_exceptions([AccListNotExist, AccListExists])
async def create_account_list(
    response: Response,
    account_uuid: UUID4,
    account_list_data: AccountListsCreate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(serv_session.validate_session),
    account_lists_create_srvc: CreateSrvc = Depends(
        service_container["account_lists_create"]
    ),
) -> AccountListsRes:
    """
    Create one account list link to an existing product list..
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        sys_values.sys_created_by(data=account_list_data, sys_user=sys_user.uuid)
        return await account_lists_create_srvc.create_account_list(
            account_uuid=account_uuid, account_list_data=account_list_data, db=db
        )


@router.put(
    "/{account_uuid}/account-lists/{account_list_uuid}/",
    response_model=AccountListsRes,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([AccListNotExist])
async def update_account_list(
    response: Response,
    account_uuid: UUID4,
    account_list_uuid: UUID4,
    account_list_data: AccountListsUpdate,
    user_token: Tuple[SysUsers, str] = Depends(serv_session.validate_session),
    db: AsyncSession = Depends(get_db),
    account_lists_udpate_srvc: UpdateSrvc = Depends(
        service_container["account_lists_update"]
    ),
) -> AccountListsRes:
    """
    Update one account list link to a product list.
    """

    async with transaction_manager(db=db):
        sys_user, token = user_token
        sys_values.sys_updated_by(data=account_list_data, sys_user=sys_user.uuid)
        return await account_lists_udpate_srvc.update_account_list(
            account_uuid=account_uuid,
            account_list_uuid=account_list_uuid,
            account_list_data=account_list_data,
            db=db,
        )


@router.delete(
    "/{account_uuid}/account-lists/{account_list_uuid}/",
    response_model=AccountListsDelRes,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([AccListNotExist])
async def soft_del_account_list(
    request: Request,
    response: Response,
    account_uuid: UUID4,
    account_list_uuid: UUID4,
    user_token: Tuple[SysUsers, str] = Depends(serv_session.validate_session),
    db: AsyncSession = Depends(get_db),
    account_lists_delete_srvc: DelSrvc = Depends(
        service_container["account_lists_delete"]
    ),
) -> AccountListsDelRes:
    """
    Soft delete one account list link to a product list.
    """

    async with transaction_manager(db=db):
        account_list_data = AccountListsDel()
        sys_user, _ = user_token
        sys_values.sys_deleted_by(data=account_list_data, sys_user=sys_user.uuid)
        return await account_lists_delete_srvc.soft_del_account_list(
            account_uuid=account_uuid,
            account_list_uuid=account_list_uuid,
            account_list_data=account_list_data,
            db=db,
        )
