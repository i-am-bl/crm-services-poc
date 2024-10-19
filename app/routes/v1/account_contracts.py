from fastapi import APIRouter, Depends, Query, Request, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.database import get_db, transaction_manager
from ...exceptions import AccContractExists, AccContractNotExist
from ...handlers.handler import handle_exceptions
from ...schemas import account_contracts as s_account_contracts
from ...services.account_contracts import AccountContractsServices
from ...services.authetication import SessionService, TokenService
from ...utilities.sys_users import SetSys
from ...utilities.utilities import Pagination as pg

serv_acc_contr_r = AccountContractsServices.ReadService()
serv_acc_contr_c = AccountContractsServices.CreateService()
serv_acc_contr_u = AccountContractsServices.UpdateService()
serv_acc_contr_d = AccountContractsServices.DelService()
serv_session = SessionService()
serv_token = TokenService()
router = APIRouter()


@router.get(
    "/v1/account-management/accounts/{account_uuid}/account-contracts/{account_contract_uuid}/",
    response_model=s_account_contracts.AccountContractsReponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([AccContractNotExist])
async def get_account_contract(
    response: Response,
    account_uuid: UUID4,
    account_contract_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_account_contracts.AccountContractsReponse:
    """get one account contract"""

    async with transaction_manager(db=db):
        account_contract = await serv_acc_contr_r.get_account_contract(
            account_uuid=account_uuid,
            account_contract_uuid=account_contract_uuid,
            db=db,
        )
        return account_contract


@router.get(
    "/v1/account-management/accounts/{account_uuid}/account-contracts/",
    response_model=s_account_contracts.AccountContractsPagRepsone,
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
    user_token: str = Depends(serv_session.validate_session),
) -> s_account_contracts.AccountContractsPagRepsone:
    """get many account contracts by account"""

    async with transaction_manager(db=db):
        offset = pg.pagination_offset(page=page, limit=limit)
        total_count = await serv_acc_contr_r.get_account_contracts_ct(
            account_uuid=account_uuid, db=db
        )
        account_contracts = await serv_acc_contr_r.get_account_contracts(
            account_uuid=account_uuid, limit=limit, offset=offset, db=db
        )
        return {
            "total": total_count,
            "page": page,
            "limit": limit,
            "has_more": pg.has_more(total_count=total_count, page=page, limit=limit),
            "account_contracts": account_contracts,
        }


@router.post(
    "/v1/account-management/accounts/{account_uuid}/account-contracts/",
    response_model=s_account_contracts.AccountContractsReponse,
    status_code=status.HTTP_201_CREATED,
)
@serv_token.set_auth_cookie
@handle_exceptions([AccContractNotExist, AccContractExists])
async def create_account_contract(
    response: Response,
    account_uuid: UUID4,
    account_contract_data: s_account_contracts.AccountContractsCreate,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_account_contracts.AccountContractsCreate:
    """create one account contract"""

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_created_by(data=account_contract_data, sys_user=sys_user)
        account_contract = await serv_acc_contr_c.create_account_contract(
            account_uuid=account_uuid,
            account_contract_data=account_contract_data,
            db=db,
        )
        return account_contract


@router.put(
    "/v1/account-management/accounts/{account_uuid}/account-contracts/{account_contract_uuid}/",
    response_model=s_account_contracts.AccountContractsReponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([AccContractNotExist])
async def update_account_contract(
    response: Response,
    account_uuid: UUID4,
    account_contract_uuid: UUID4,
    account_contract_data: s_account_contracts.AccountContractsUpdate,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_account_contracts.AccountContractsUpdate:
    """update one account contract"""

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_updated_by(data=account_contract_data, sys_user=sys_user)
        account_contract = await serv_acc_contr_u.update_account_contract(
            account_uuid=account_uuid,
            account_contract_uuid=account_contract_uuid,
            account_contract_data=account_contract_data,
            db=db,
        )
        return account_contract


@router.delete(
    "/v1/account-management/accounts/{account_uuid}/account-contracts/{account_contract_uuid}/",
    response_model=s_account_contracts.AccountContractsDelRepsone,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([AccContractNotExist])
async def soft_del_account_contract(
    response: Response,
    account_uuid: UUID4,
    account_contract_uuid: UUID4,
    account_contract_data: s_account_contracts.AccountContractsDel,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_account_contracts.AccountContractsDel:
    """del one account contract"""

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_deleted_by(data=account_contract_data, sys_user=sys_user)
        account_contract = await serv_acc_contr_d.soft_del_account_contract(
            account_uuid=account_uuid,
            account_contract_uuid=account_contract_uuid,
            account_contract_data=account_contract_data,
            db=db,
        )
        return account_contract
