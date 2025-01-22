from typing import Callable, Tuple

from fastapi import APIRouter, Depends, Query, Request, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.database import Operations, get_db, transaction_manager
from ...exceptions import AccContractExists, AccContractNotExist
from ...handlers.handler import handle_exceptions
from ...models import (
    account_contracts as account_contract_mdls,
    sys_users as sys_user_mdl,
)
from ...schemas import account_contracts as account_contract_schms
from ...services import account_contracts as account_contract_srvcs
from ...services.authetication import SessionService, TokenService
from ...statements.account_contracts import (
    account_contract_stms,
    AccountContractStms,
)
from ...utilities import pagination
from ...utilities import sys_values

_account_contracts_stms: AccountContractStms = account_contract_stms(
    account_contracts_mdl=account_contract_mdls.AcccountContracts
)

# Service instances
srvc_create_account_contracts: account_contract_srvcs.CreateSrvc = (
    account_contract_srvcs.account_contract_create_srvc(
        operations=Operations, model=account_contract_mdls.AcccountContracts
    )
)
srvc_read_account_contracts: account_contract_srvcs.ReadSrvc = (
    account_contract_srvcs.account_contract_read_srvc(
        operations=Operations, statements=_account_contracts_stms
    )
)
srvc_update_account_contracts: account_contract_srvcs.UpdateSrvc = (
    account_contract_srvcs.account_contract_update_srvc(
        operations=Operations, statements=_account_contracts_stms
    )
)
srvc_delete_account_contracts: account_contract_srvcs.DeleteSrvc = (
    account_contract_srvcs.account_contract_delete_srvc(
        operations=Operations, statements=_account_contracts_stms
    )
)

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
        srvc_read_account_contracts
    ),
) -> account_contract_schms.AccountContractsReponse:
    """
    Fetch one account contract by account and account contract uuid.
    """

    async with transaction_manager(db=db):
        return await account_contract_read_srvc.get_acct_cntrct(
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
        srvc_read_account_contracts
    ),
) -> account_contract_schms.AccountContractsPagRepsone:
    """
    Fetch all account contracts by account uuid.
    """

    async with transaction_manager(db=db):
        offset = pagination.page_offset(page=page, limit=limit)
        total_count = await account_contract_read_srvc.get_account_contracts_count(
            account_uuid=account_uuid, db=db
        )
        account_contracts = await account_contract_read_srvc.get_account_contracts(
            account_uuid=account_uuid, limit=limit, offset=offset, db=db
        )
        has_more = pagination.has_more_items(
            total_count=total_count, page=page, limit=limit
        )
        return account_contract_schms.AccountContractsPagRepsone(
            total=total_count,
            page=page,
            limit=limit,
            has_more=has_more,
            account_contracts=account_contracts,
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
        srvc_create_account_contracts
    ),
) -> account_contract_schms.AccountContractsCreate:
    """
    Create one account contract.
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        sys_values.sys_created_by(data=account_contract_data, sys_user=sys_user)
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
        srvc_update_account_contracts
    ),
) -> account_contract_schms.AccountContractsUpdate:
    """
    Update one account contract.
    """

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        sys_values.sys_updated_by(data=account_contract_data, sys_user=sys_user)
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
        srvc_delete_account_contracts
    ),
) -> account_contract_schms.AccountContractsDel:
    """
    Soft delete one account contract.
    """

    async with transaction_manager(db=db):
        account_contract_data = account_contract_schms.AccountContractsDel()
        sys_user, _ = user_token
        sys_values.sys_deleted_by(data=account_contract_data, sys_user=sys_user)
        return await account_contracts_delete_srvc.soft_delete_account_contract(
            account_uuid=account_uuid,
            account_contract_uuid=account_contract_uuid,
            account_contract_data=account_contract_data,
            db=db,
        )
