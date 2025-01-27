from typing import Tuple

from fastapi import APIRouter, Depends, Query, Request, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...containers.services import container as services_container
from ...database.database import get_db, transaction_manager
from ...exceptions import AccContractExists, AccContractNotExist
from ...handlers.handler import handle_exceptions
from ...models import (
    sys_users as sys_user_mdl,
)
from ...schemas import account_contracts as account_contract_schms
from ...services import account_contracts as account_contract_srvcs
from ...services.authetication import SessionService, TokenService
from ...utilities import sys_values

serv_session = SessionService()
serv_token = TokenService()
router = APIRouter()


@router.get(
    "/{account_uuid}/account-contracts/{account_contract_uuid}/",
    response_model=account_contract_schms.AccountContractsReponse,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
@serv_token.set_auth_cookie
@handle_exceptions([AccContractNotExist])
async def get_account_contract(
    response: Response,
    account_uuid: UUID4,
    account_contract_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[sys_user_mdl.SysUsers, str] = Depends(
        serv_session.validate_session
    ),
    account_contract_read_srvc: account_contract_srvcs.ReadSrvc = Depends(
        services_container["account_contracts_read"]
    ),
) -> account_contract_schms.AccountContractsReponse:
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
    response_model=account_contract_schms.AccountContractsPagRepsone,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([AccContractNotExist])
async def get_account_contracts(
    response: Response,
    account_uuid: UUID4,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[sys_user_mdl.SysUsers, str] = Depends(
        serv_session.validate_session
    ),
    account_contract_read_srvc: account_contract_srvcs.ReadSrvc = Depends(
        services_container["account_contracts_read"]
    ),
) -> account_contract_schms.AccountContractsPagRepsone:
    """
    Fetch all account contracts by account uuid.
    """

    async with transaction_manager(db=db):
        return await account_contract_read_srvc.paginated_account_contracts(
            account_uuid=account_uuid, page=page, limit=limit, db=db
        )


@router.post(
    "/{account_uuid}/account-contracts/",
    response_model=account_contract_schms.AccountContractsReponse,
    status_code=status.HTTP_201_CREATED,
)
@serv_token.set_auth_cookie
@handle_exceptions([AccContractNotExist, AccContractExists])
async def create_account_contract(
    response: Response,
    account_uuid: UUID4,
    account_contract_data: account_contract_schms.AccountContractsCreate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[sys_user_mdl.SysUsers, str] = Depends(
        serv_session.validate_session
    ),
    account_contract_create_srvc: account_contract_srvcs.CreateSrvc = Depends(
        services_container["account_contracts_create"]
    ),
    set_sys_created_by: sys_values.SysFieldSetter = Depends(sys_values.sys_created_by),
) -> account_contract_schms.AccountContractsCreate:
    """
    Create one account contract.
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        set_sys_created_by(data=account_contract_data, sys_user=sys_user.uuid)
        return await account_contract_create_srvc.create_account_contract(
            account_uuid=account_uuid,
            account_contract_data=account_contract_data,
            db=db,
        )


@router.put(
    "/{account_uuid}/account-contracts/{account_contract_uuid}/",
    response_model=account_contract_schms.AccountContractsReponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([AccContractNotExist])
async def update_account_contract(
    response: Response,
    account_uuid: UUID4,
    account_contract_uuid: UUID4,
    account_contract_data: account_contract_schms.AccountContractsUpdate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[sys_user_mdl.SysUsers, str] = Depends(
        serv_session.validate_session
    ),
    account_contract_update_srvc: account_contract_srvcs.UpdateSrvc = Depends(
        services_container["account_contracts_update"]
    ),
    set_sys_updated_by: sys_values.SysFieldSetter = Depends(sys_values.sys_updated_by),
) -> account_contract_schms.AccountContractsUpdate:
    """
    Update one account contract.
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        set_sys_updated_by(data=account_contract_data, sys_user=sys_user.uuid)
        return await account_contract_update_srvc.update_account_contract(
            account_uuid=account_uuid,
            account_contract_uuid=account_contract_uuid,
            account_contract_data=account_contract_data,
            db=db,
        )


@router.delete(
    "/{account_uuid}/account-contracts/{account_contract_uuid}/",
    response_model=account_contract_schms.AccountContractsDelRepsone,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([AccContractNotExist])
async def soft_delete_account_contract(
    response: Response,
    account_uuid: UUID4,
    account_contract_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[sys_user_mdl.SysUsers, str] = Depends(
        serv_session.validate_session
    ),
    account_contracts_delete_srvc: account_contract_srvcs.DeleteSrvc = Depends(
        services_container["account_contracts_delete"]
    ),
    set_sys_deleted_by: sys_values.SysFieldSetter = Depends(sys_values.sys_deleted_by),
) -> account_contract_schms.AccountContractsDel:
    """
    Soft delete one account contract.
    """

    async with transaction_manager(db=db):
        account_contract_data = account_contract_schms.AccountContractsDel()
        sys_user, _ = user_token
        set_sys_deleted_by(data=account_contract_data, sys_user=sys_user.uuid)
        return await account_contracts_delete_srvc.soft_delete_account_contract(
            account_uuid=account_uuid,
            account_contract_uuid=account_contract_uuid,
            account_contract_data=account_contract_data,
            db=db,
        )
