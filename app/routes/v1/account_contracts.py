from typing import Tuple

from fastapi import APIRouter, Depends, Query, Request, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...containers.services import container as services_container
from ...database.database import get_db, transaction_manager
from ...exceptions import AccContractExists, AccContractNotExist
from ...handlers.handler import handle_exceptions
from ...models.sys_users import SysUsers
from ...schemas.account_contracts import (
    AccountContractsCreate,
    AccountContractsDel,
    AccountContractsInternalCreate,
    AccountContractsInternalUpdate,
    AccountContractsPgRes,
    AccountContractsRes,
    AccountContractsUpdate,
)
from ...services.account_contracts import ReadSrvc, CreateSrvc, UpdateSrvc, DelSrvc
from ...services.token import set_auth_cookie
from ...utilities import sys_values
from ...utilities.data import internal_schema_validation
from ...utilities.auth import get_validated_session

router = APIRouter()


@router.get(
    "/{account_uuid}/account-contracts/{account_contract_uuid}/",
    response_model=AccountContractsRes,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
@set_auth_cookie
@handle_exceptions([AccContractNotExist])
async def get_account_contract(
    response: Response,
    account_uuid: UUID4,
    account_contract_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    account_contract_read_srvc: ReadSrvc = Depends(
        services_container["account_contracts_read"]
    ),
) -> AccountContractsRes:
    """
    Fetch one account contract by account and account contract uuid.
    """

    async with transaction_manager(db=db):
        return await account_contract_read_srvc.get_account_contract(
            account_uuid=account_uuid,
            account_contract_uuid=account_contract_uuid,
            db=db,
        )


@router.get(
    "/{account_uuid}/account-contracts/",
    response_model=AccountContractsPgRes,
    status_code=status.HTTP_200_OK,
)
@set_auth_cookie
@handle_exceptions([AccContractNotExist])
async def get_account_contracts(
    response: Response,
    account_uuid: UUID4,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    account_contract_read_srvc: ReadSrvc = Depends(
        services_container["account_contracts_read"]
    ),
) -> AccountContractsPgRes:
    """
    Fetch all account contracts by account uuid.
    """

    async with transaction_manager(db=db):
        return await account_contract_read_srvc.paginated_account_contracts(
            account_uuid=account_uuid, page=page, limit=limit, db=db
        )


@router.post(
    "/{account_uuid}/account-contracts/",
    response_model=AccountContractsRes,
    status_code=status.HTTP_201_CREATED,
)
@set_auth_cookie
@handle_exceptions([AccContractNotExist, AccContractExists])
async def create_account_contract(
    response: Response,
    account_uuid: UUID4,
    account_contract_data: AccountContractsCreate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    account_contract_create_srvc: CreateSrvc = Depends(
        services_container["account_contracts_create"]
    ),
) -> AccountContractsCreate:
    """
    Create one account contract.
    """

    sys_user, _ = user_token
    _account_contract_data: AccountContractsInternalCreate = internal_schema_validation(
        data=account_contract_data,
        schema=AccountContractsInternalCreate,
        setter_method=sys_values.sys_created_by,
        sys_user_uuid=sys_user.uuid,
    )
    async with transaction_manager(db=db):
        return await account_contract_create_srvc.create_account_contract(
            account_uuid=account_uuid,
            account_contract_data=_account_contract_data,
            db=db,
        )


@router.put(
    "/{account_uuid}/account-contracts/{account_contract_uuid}/",
    response_model=AccountContractsRes,
    status_code=status.HTTP_200_OK,
)
@set_auth_cookie
@handle_exceptions([AccContractNotExist])
async def update_account_contract(
    response: Response,
    account_uuid: UUID4,
    account_contract_uuid: UUID4,
    account_contract_data: AccountContractsUpdate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    account_contract_update_srvc: UpdateSrvc = Depends(
        services_container["account_contracts_update"]
    ),
) -> AccountContractsRes:
    """
    Update one account contract.
    """

    sys_user, _ = user_token
    _account_contract_data: AccountContractsInternalUpdate = internal_schema_validation(
        schema=AccountContractsInternalUpdate,
        data=account_contract_data,
        setter_method=sys_values.sys_updated_by,
        sys_user_uuid=sys_user.uuid,
    )
    async with transaction_manager(db=db):

        return await account_contract_update_srvc.update_account_contract(
            account_uuid=account_uuid,
            account_contract_uuid=account_contract_uuid,
            account_contract_data=_account_contract_data,
            db=db,
        )


@router.delete(
    "/{account_uuid}/account-contracts/{account_contract_uuid}/",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
@set_auth_cookie
@handle_exceptions([AccContractNotExist])
async def soft_delete_account_contract(
    response: Response,
    account_uuid: UUID4,
    account_contract_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    account_contracts_delete_srvc: DelSrvc = Depends(
        services_container["account_contracts_delete"]
    ),
) -> None:
    """
    Soft delete one account contract.
    """

    sys_user, _ = user_token
    _account_contract_data: AccountContractsDel = internal_schema_validation(
        schema=AccountContractsDel,
        setter_method=sys_values.sys_deleted_by,
        sys_user_uuid=sys_user.uuid,
    )
    async with transaction_manager(db=db):

        await account_contracts_delete_srvc.soft_delete_account_contract(
            account_uuid=account_uuid,
            account_contract_uuid=account_contract_uuid,
            account_contract_data=_account_contract_data,
            db=db,
        )
