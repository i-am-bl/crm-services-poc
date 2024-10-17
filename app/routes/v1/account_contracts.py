from fastapi import APIRouter, Depends, Query, Request, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.database import get_db
from ...schemas import account_contracts as s_account_contracts
from ...services.account_contracts import AccountContractsServices
from ...services.authetication import SessionService
from ...utilities.service_utils import pagination_offset
from ...utilities.sys_users import SetSys
from ...exceptions import UnhandledException, AccContractNotExist, AccContractExists

serv_acc_contr_r = AccountContractsServices.ReadService()
serv_acc_contr_c = AccountContractsServices.CreateService()
serv_acc_contr_u = AccountContractsServices.UpdateService()
serv_acc_contr_d = AccountContractsServices.DelService()
serv_session = SessionService()

router = APIRouter()


@router.get(
    "/v1/account-management/accounts/{account_uuid}/account-contracts/{account_contract_uuid}/",
    response_model=s_account_contracts.AccountContractsRepsone,
    status_code=status.HTTP_200_OK,
)
async def get_account_contract(
    request: Request,
    response: Response,
    account_uuid: UUID4,
    account_contract_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
):
    """get one account contract"""
    try:
        async with db.begin():
            _ = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            account_contract = await serv_acc_contr_r.get_account_contract(
                account_uuid=account_uuid,
                account_contract_uuid=account_contract_uuid,
                db=db,
            )
            return account_contract
    except AccContractNotExist:
        raise AccContractNotExist()
    except Exception:
        raise UnhandledException()


@router.get(
    "/v1/account-management/accounts/{account_uuid}/account-contracts/",
    response_model=s_account_contracts.AccountContractsPagRepsone,
    status_code=status.HTTP_200_OK,
)
async def get_account_contracts(
    request: Request,
    response: Response,
    account_uuid: UUID4,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """get many account contracts by account"""
    try:
        async with db.begin():
            _ = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            offset = pagination_offset(page=page, limit=limit)
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
                "has_more": total_count > (page * limit),
                "account_contracts": account_contracts,
            }
    except AccContractNotExist:
        raise AccContractNotExist()
    except Exception:
        raise UnhandledException()


@router.post(
    "/v1/account-management/accounts/{account_uuid}/account-contracts/",
    response_model=s_account_contracts.AccountContractsRepsone,
    status_code=status.HTTP_201_CREATED,
)
async def create_account_contract(
    request: Request,
    response: Response,
    account_uuid: UUID4,
    account_contract_data: s_account_contracts.AccountContractsCreate,
    db: AsyncSession = Depends(get_db),
):
    """create one account contract"""
    try:
        async with db.begin():
            sys_user = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            SetSys.sys_created_by(data=account_contract_data, sys_user=sys_user)
            account_contract = await serv_acc_contr_c.create_account_contract(
                account_uuid=account_uuid,
                account_contract_data=account_contract_data,
                db=db,
            )
            return account_contract
    except AccContractNotExist:
        raise AccContractNotExist()
    except AccContractExists:
        raise AccContractExists()
    except Exception:
        raise UnhandledException()


@router.put(
    "/v1/account-management/accounts/{account_uuid}/account-contracts/{account_contract_uuid}/",
    response_model=s_account_contracts.AccountContractsRepsone,
    status_code=status.HTTP_200_OK,
)
async def update_account_contract(
    request: Request,
    response: Response,
    account_uuid: UUID4,
    account_contract_uuid: UUID4,
    account_contract_data: s_account_contracts.AccountContractsUpdate,
    db: AsyncSession = Depends(get_db),
):
    """update one account contract"""
    try:
        async with db.begin():
            sys_user = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            SetSys.sys_updated_by(data=account_contract_data, sys_user=sys_user)
            account_contract = await serv_acc_contr_u.update_account_contract(
                account_uuid=account_uuid,
                account_contract_uuid=account_contract_uuid,
                account_contract_data=account_contract_data,
                db=db,
            )
            return account_contract
    except AccContractNotExist:
        raise AccContractNotExist()
    except Exception:
        raise UnhandledException()


@router.delete(
    "/v1/account-management/accounts/{account_uuid}/account-contracts/{account_contract_uuid}/",
    response_model=s_account_contracts.AccountContractsDelRepsone,
    status_code=status.HTTP_200_OK,
)
async def soft_del_account_contract(
    request: Request,
    response: Response,
    account_uuid: UUID4,
    account_contract_uuid: UUID4,
    account_contract_data: s_account_contracts.AccountContractsDel,
    db: AsyncSession = Depends(get_db),
):
    """del one account contract"""
    try:
        async with db.begin():
            sys_user = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            SetSys.sys_deleted_by(data=account_contract_data, sys_user=sys_user)
            account_contract = await serv_acc_contr_d.soft_del_account_contract(
                account_uuid=account_uuid,
                account_contract_uuid=account_contract_uuid,
                account_contract_data=account_contract_data,
                db=db,
            )
            return account_contract
    except AccContractNotExist:
        raise AccContractNotExist()
    except Exception:
        raise UnhandledException()
