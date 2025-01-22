from fastapi import Depends
from pydantic import UUID4
from sqlalchemy import Select, and_, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Callable

import app.models.account_contracts as m_account_contracts
import app.schemas.account_contracts as s_account_contracts

from ..constants import constants as cnst
from ..database.database import Operations, get_db
from ..exceptions import AccContractNotExist

from ..statements import AcctContractStms, acct_cntrct_stms
from ..utilities.utilities import DataUtils as di


class AccContractsModels:
    account_contracts = m_account_contracts.AcccountContracts


class ReadService:
    def __init__(
        self, statement_factory: Callable[[], AcctContractStms] = acct_cntrct_stms
    ) -> None:
        self.statement_factory = statement_factory

    async def get_account_contract(
        self,
        account_uuid: UUID4,
        account_contract_uuid: UUID4,
        db: AsyncSession = Depends(get_db),
    ):
        statement = self.statement_factory()

        statement.sel_acc_contr_by_uuid(
            account_uuid=account_uuid, account_contract_uuid=account_contract_uuid
        )
        account_contract = await Operations.return_one_row(
            service=cnst.ACCOUNTS_CONTRACTS_READ_SERVICE, statement=statement, db=db
        )
        return di.record_not_exist(
            instance=account_contract, exception=AccContractNotExist
        )

    async def get_account_contracts(
        self,
        account_uuid: UUID4,
        limit: int,
        offset: int,
        db: AsyncSession = Depends(get_db),
    ):
        statement = acct_cntrct_stms()
        statement.sel_acc_contr_by_acc(
            account_uuid=account_uuid,
            limit=limit,
            offset=offset,
        )
        account_contracts = await Operations.return_all_rows(
            service=cnst.ACCOUNTS_CONTRACTS_READ_SERVICE, statement=statement, db=db
        )
        return di.record_not_exist(
            instance=account_contracts, exception=AccContractNotExist
        )

    async def get_account_contracts_ct(
        self,
        account_uuid: UUID4,
        db: AsyncSession = Depends(get_db),
    ):
        statement = acct_cntrct_stms()
        statement.sel_acc_contr_ct(account_uuid=account_uuid)
        return await Operations.return_count(
            service=cnst.ACCOUNTS_CONTRACTS_READ_SERVICE, statement=statement, db=db
        )


class CreateService:
    def __init__(self) -> None:
        pass

    async def create_account_contract(
        self,
        account_uuid: UUID4,
        account_contract_data: s_account_contracts.AccountContractsCreate,
        db: AsyncSession = Depends(get_db),
    ):
        account_contracts = AccContractsModels.account_contracts
        account_contract = await Operations.add_instance(
            service=cnst.ACCOUNTS_CONTRACTS_CREATE_SERVICE,
            model=account_contracts,
            data=account_contract_data,
            db=db,
        )
        return di.record_not_exist(
            instance=account_contract, exception=AccContractNotExist
        )


class UpdateService:
    def __init__(self) -> None:
        pass

    async def update_account_contract(
        self,
        account_uuid: UUID4,
        account_contract_uuid: UUID4,
        account_contract_data: s_account_contracts.AccountContractsUpdate,
        db: AsyncSession = Depends(get_db),
    ):
        statement = acct_cntrct_stms()
        statement.update_acc_contr_by_uuid(
            account_uuid=account_uuid,
            account_contract_uuid=account_contract_uuid,
            account_contract_data=account_contract_data,
        )
        account_contract = await Operations.return_one_row(
            service=cnst.ACCOUNTS_CONTRACTS_UPDATE_SERVICE,
            statement=statement,
            db=db,
        )
        return di.record_not_exist(
            instance=account_contract, exception=AccContractNotExist
        )


class DelService:
    def __init__(self) -> None:
        pass

    async def soft_del_account_contract(
        self,
        account_uuid: UUID4,
        account_contract_uuid: UUID4,
        account_contract_data: s_account_contracts.AccountContractsDel,
        db: AsyncSession = Depends(get_db),
    ):
        statement = acct_cntrct_stms()
        statement.update_acc_contr_by_uuid(
            account_uuid=account_uuid,
            account_contract_uuid=account_contract_uuid,
            account_contract_data=account_contract_data,
        )
        account_contract = await Operations.return_one_row(
            service=cnst.ACCOUNTS_CONTRACTS_UPDATE_SERVICE,
            statement=statement,
            db=db,
        )
        return di.record_not_exist(
            instance=account_contract, exception=AccContractNotExist
        )


def read_factory():
    statements = acct_cntrct_stms()
    return ReadService(acct_cntrct_stms=statements)
