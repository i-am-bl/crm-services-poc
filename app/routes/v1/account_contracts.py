from typing import List

from fastapi import APIRouter, Depends, status, Query
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import Operations, get_db
from app.services.account_contracts import AccountContractsServices
from app.service_utils import pagination_offset


serv_acc_contr_r = AccountContractsServices.ReadService()
serv_acc_contr_c = AccountContractsServices.CreateService()
serv_acc_contr_u = AccountContractsServices.UpdateService()
serv_acc_contr_d = AccountContractsServices.DelService()

import app.schemas.account_contracts as s_account_contracts

router = APIRouter()


@router.get(
    "/v1/account-management/accounts/{account_uuid}/account-contracts/{account_contract_uuid}/",
    response_model=s_account_contracts.AccountContractsRepsone,
    status_code=status.HTTP_200_OK,
)
async def get_account_contract(
    account_uuid: UUID4,
    account_contract_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
):
    """get one account contract"""
    async with db.begin():
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
async def get_account_contracts(
    account_uuid: UUID4,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """get many account contracts by account"""
    async with db.begin():
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


@router.post(
    "/v1/account-management/accounts/{account_uuid}/account-contracts/",
    response_model=s_account_contracts.AccountContractsRepsone,
    status_code=status.HTTP_201_CREATED,
)
async def create_account_contract(
    account_uuid: UUID4,
    account_contract_data: s_account_contracts.AccountContractsCreate,
    db: AsyncSession = Depends(get_db),
):
    """create one account contract"""
    async with db.begin():
        account_contract = await serv_acc_contr_c.create_account_contract(
            account_uuid=account_uuid,
            account_contract_data=account_contract_data,
            db=db,
        )
        return account_contract


@router.put(
    "/v1/account-management/accounts/{account_uuid}/account-contracts/{account_contract_uuid}/",
    response_model=s_account_contracts.AccountContractsRepsone,
    status_code=status.HTTP_200_OK,
)
async def update_account_contract(
    account_uuid: UUID4,
    account_contract_uuid: UUID4,
    account_contract_data: s_account_contracts.AccountContractsUpdate,
    db: AsyncSession = Depends(get_db),
):
    """update one account contract"""
    async with db.begin():
        account_contract = await serv_acc_contr_u.update_account_contract(
            account_uuid=account_uuid,
            account_contract_uuid=account_contract_uuid,
            account_contract_data=account_contract_data,
            db=db,
        )
        return account_contract


""" del one account contract """


@router.delete(
    "/v1/account-management/accounts/{account_uuid}/account-contracts/{account_contract_uuid}/",
    response_model=s_account_contracts.AccountContractsDelRepsone,
    status_code=status.HTTP_200_OK,
)
async def soft_del_account_contract(
    account_uuid: UUID4,
    account_contract_uuid: UUID4,
    account_contract_data: s_account_contracts.AccountContractsDel,
    db: AsyncSession = Depends(get_db),
):
    async with db.begin():
        account_contract = await serv_acc_contr_d.soft_del_account_contract(
            account_uuid=account_uuid,
            account_contract_uuid=account_contract_uuid,
            db=db,
        )
        return account_contract
