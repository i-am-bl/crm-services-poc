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
    AccountsInternalCreate,
    AccountsRes,
    AccountsPgRes,
    AccountsDel,
    AccountsUpdate,
)
from ...services.accounts import CreateSrvc, ReadSrvc, UpdateSrvc, DelSrvc
from ...services.token import set_auth_cookie
from ...utilities import sys_values
from ...utilities.auth import get_validated_session
from ...utilities.data import internal_schema_validation

router = APIRouter()


@router.get(
    "/{account_uuid}/",
    response_model=AccountsRes,
    status_code=status.HTTP_200_OK,
)
@set_auth_cookie
@handle_exceptions([AccsNotExist])
async def get_account(
    response: Response,
    account_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
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
@set_auth_cookie
@handle_exceptions([AccsNotExist])
async def get_accounts(
    response: Response,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
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
@set_auth_cookie
@handle_exceptions([AccsNotExist])
async def create_account(
    response: Response,
    account_data: AccountsCreate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    accounts_create_srvc: CreateSrvc = Depends(services_container["accounts_create"]),
) -> AccountsRes:
    """
    Create one account.

    This is intended to create a link with an existing entity while opening a new account.
    Similar behavior can be achieved from the context of the entity.
    """

    sys_user, _ = user_token
    _account_data: AccountsInternalCreate = internal_schema_validation(
        data=account_data,
        schema=AccountsInternalCreate,
        setter_method=sys_values.sys_created_by,
        sys_user_uuid=sys_user.uuid,
    )

    async with transaction_manager(db=db):

        return await accounts_create_srvc.create_account(
            account_data=_account_data, db=db
        )


# There is no need for this at this time.
# TODO: Remove is not needed at some point.
@router.put(
    "/{account_uuid}/",
    response_model=AccountsRes,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
    deprecated=True,
)
@set_auth_cookie
@handle_exceptions([AccsNotExist])
async def update_account(
    response: Response,
    account_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    update_accounts_srvc: UpdateSrvc = Depends(services_container["accounts_update"]),
) -> AccountsRes:
    """
    Update one account.
    """
    sys_user, _ = user_token
    _account_data: AccountsUpdate = internal_schema_validation(
        schema=AccountsUpdate,
        setter_method=sys_values.sys_updated_by,
        sys_user_uuid=sys_user.uuid,
    )

    async with transaction_manager(db=db):
        return await update_accounts_srvc.update_account(
            account_uuid=account_uuid, account_data=_account_data, db=db
        )


@router.delete(
    "/{account_uuid}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
@set_auth_cookie
@handle_exceptions([AccsNotExist])
async def soft_del_account(
    response: Response,
    account_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    accounts_delete_srvc: DelSrvc = Depends(services_container["accounts_delete"]),
) -> None:
    """
    Soft del one account.
    """
    sys_user, _ = user_token
    _account_data: AccountsDel = internal_schema_validation(
        schema=AccountsDel,
        setter_method=sys_values.sys_updated_by,
        sys_user_uuid=sys_user.uuid,
    )
    async with transaction_manager(db=db):
        await accounts_delete_srvc.sof_del_account(
            account_uuid=account_uuid, account_data=_account_data, db=db
        )
