from typing import Tuple

from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...containers.services import container as services_container
from ...database.database import get_db, transaction_manager
from ...exceptions import AccsNotExist
from ...handlers.handler import handle_exceptions
from ...models.sys_users import SysUsers
from ...schemas.accounts import (
    AccountsCreate,
    AccountsRes,
    AccountsPgRes,
    AccountsDel,
    AccountsUpdate,
)
from ...services.accounts import CreateSrvc, ReadSrvc, UpdateSrvc, DelSrvc
from ...services.authetication import SessionService, TokenService
from ...utilities import sys_values

serv_session = SessionService()
serv_token = TokenService()
router = APIRouter()


@router.get(
    "/{account_uuid}/",
    response_model=AccountsRes,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([AccsNotExist])
async def get_account(
    response: Response,
    account_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(serv_session.validate_session),
    accounts_read_srvc: ReadSrvc = Depends(services_container["accounts_read"]),
) -> AccountsRes:
    """
    Get one account by account_uuid.
    """

    async with transaction_manager(db=db):
        return await accounts_read_srvc.get_account(account_uuid=account_uuid, db=db)


@router.get(
    "/",
    response_model=AccountsPgRes,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([AccsNotExist])
async def get_accounts(
    response: Response,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(serv_session.validate_session),
    accounts_read_srvc: ReadSrvc = Depends(services_container["accounts_read"]),
) -> AccountsPgRes:
    """
    Get many accounts.
    """

    async with transaction_manager(db=db):
        return await accounts_read_srvc.paginated_accounts(
            page=page, limit=limit, db=db
        )


@router.post(
    "/",
    response_model=AccountsRes,
    status_code=status.HTTP_201_CREATED,
)
@serv_token.set_auth_cookie
@handle_exceptions([AccsNotExist])
async def create_account(
    response: Response,
    account_data: AccountsCreate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(serv_session.validate_session),
    accounts_create_srvc: CreateSrvc = Depends(services_container["accounts_create"]),
) -> AccountsRes:
    """
    Create one account.

    This is intended to create a link with an existing entity while opening a new account.
    Similar behavior can be achieved from the context of the entity.
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        sys_values.sys_created_by(data=account_data, sys_user=sys_user.uuid)
        return await accounts_create_srvc.create_account(
            account_data=account_data, db=db
        )


@router.put(
    "/{account_uuid}/",
    response_model=AccountsRes,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([AccsNotExist])
async def update_account(
    response: Response,
    account_uuid: UUID4,
    account_data: AccountsUpdate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(serv_session.validate_session),
    update_accounts_srvc: UpdateSrvc = Depends(services_container["accounts_update"]),
) -> AccountsRes:
    """
    Update one account.
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        sys_values.sys_updated_by(data=account_data, sys_user=sys_user.uuid)
        return await update_accounts_srvc.update_account(
            account_uuid=account_uuid, account_data=account_data, db=db
        )


@router.delete(
    "/{account_uuid}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
@serv_token.set_auth_cookie
@handle_exceptions([AccsNotExist])
async def soft_del_account(
    response: Response,
    account_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(serv_session.validate_session),
    accounts_delete_srvc: DelSrvc = Depends(services_container["accounts_delete"]),
) -> None:
    """
    Soft del one account.
    """

    async with transaction_manager(db=db):
        account_data = AccountsDel()
        sys_user, _ = user_token
        sys_values.sys_deleted_by(data=account_data, sys_user=sys_user.uuid)
        await accounts_delete_srvc.sof_del_account(
            account_uuid=account_uuid, account_data=account_data, db=db
        )
