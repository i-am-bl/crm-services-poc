from fastapi import Depends
from pydantic import UUID4
from sqlalchemy import Select, and_, func, update
from sqlalchemy.ext.asyncio import AsyncSession

import app.models.account_contracts as m_account_contracts
import app.schemas.account_contracts as s_account_contracts

from ..constants import constants as cnst
from ..database.database import Operations, get_db
from ..exceptions import AccContractExists, AccContractNotExist
from ..utilities.utilities import DataUtils as di


class AccContractsModels:
    account_contracts = m_account_contracts.AcccountContracts


class AccContractsStms:
    pass

    class SelStatements:

        pass

        @staticmethod
        def sel_acc_contr_by_uuid(account_uuid: UUID4, account_contract_uuid: UUID4):
            account_contracts = AccContractsModels.account_contracts
            statement = Select(account_contracts).where(
                account_contracts.account_uuid == account_uuid,
                account_contracts.uuid == account_contract_uuid,
                account_contracts.sys_deleted_at == None,
            )
            return statement

        @staticmethod
        def sel_acc_contr_by_acc(account_uuid: UUID4, limit: int, offset: int):
            account_contracts = AccContractsModels.account_contracts
            statement = (
                Select(account_contracts)
                .where(
                    account_contracts.account_uuid == account_uuid,
                    account_contracts.sys_deleted_at == None,
                )
                .offset(offset=offset)
                .limit(limit=limit)
            )
            return statement

        @staticmethod
        def sel_acc_contr_ct(account_uuid: UUID4):
            account_contracts = AccContractsModels.account_contracts
            statement = (
                Select(func.count())
                .select_from(account_contracts)
                .where(
                    account_contracts.account_uuid == account_uuid,
                    account_contracts.sys_deleted_at == None,
                    account_contracts.sys_deleted_at == None,
                )
            )
            return statement

    class UpdateStatements:
        pass

        @staticmethod
        def update_acc_contr_by_uuid(
            account_uuid: UUID4,
            account_contract_uuid: UUID4,
            account_contract_data: object,
        ):
            account_contracts = AccContractsModels.account_contracts
            statement = (
                update(account_contracts)
                .where(
                    and_(
                        account_contracts.account_uuid == account_uuid,
                        account_contracts.uuid == account_contract_uuid,
                        account_contracts.sys_deleted_at == None,
                    )
                )
                .values(di.set_empty_strs_null(values=account_contract_data))
                .returning(account_contracts)
            )
            return statement


class AccountContractsServices:
    pass

    class ReadService:
        def __init__(self) -> None:
            pass

        async def get_account_contract(
            self,
            account_uuid: UUID4,
            account_contract_uuid: UUID4,
            db: AsyncSession = Depends(get_db),
        ):
            statement = AccContractsStms.SelStatements.sel_acc_contr_by_uuid(
                account_uuid=account_uuid, account_contract_uuid=account_contract_uuid
            )
            account_contract = await Operations.return_one_row(
                service=cnst.ACCOUNTS_CONTRACTS_READ_SERVICE, statement=statement, db=db
            )
            di.record_not_exist(
                instance=account_contract, exception=AccContractNotExist
            )
            return account_contract

        async def get_account_contracts(
            self,
            account_uuid: UUID4,
            limit: int,
            offset: int,
            db: AsyncSession = Depends(get_db),
        ):
            statement = AccContractsStms.SelStatements.sel_acc_contr_by_acc(
                account_uuid=account_uuid,
                limit=limit,
                offset=offset,
            )
            account_contracts = await Operations.return_all_rows(
                service=cnst.ACCOUNTS_CONTRACTS_READ_SERVICE, statement=statement, db=db
            )
            di.record_not_exist(
                instance=account_contracts, exception=AccContractNotExist
            )
            return account_contracts

        async def get_account_contracts_ct(
            self,
            account_uuid: UUID4,
            db: AsyncSession = Depends(get_db),
        ):
            statement = AccContractsStms.SelStatements.sel_acc_contr_ct(
                account_uuid=account_uuid
            )
            total_count = await Operations.return_count(
                service=cnst.ACCOUNTS_CONTRACTS_READ_SERVICE, statement=statement, db=db
            )

            return total_count

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
            di.record_not_exist(
                instance=account_contract, exception=AccContractNotExist
            )
            return account_contract

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
            statement = AccContractsStms.UpdateStatements.update_acc_contr_by_uuid(
                account_uuid=account_uuid,
                account_contract_uuid=account_contract_uuid,
                account_contract_data=account_contract_data,
            )
            account_contract = await Operations.return_one_row(
                service=cnst.ACCOUNTS_CONTRACTS_UPDATE_SERVICE,
                statement=statement,
                db=db,
            )
            di.record_not_exist(
                instance=account_contract, exception=AccContractNotExist
            )
            return account_contract

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
            statement = AccContractsStms.UpdateStatements.update_acc_contr_by_uuid(
                account_uuid=account_uuid,
                account_contract_uuid=account_contract_uuid,
                account_contract_data=account_contract_data,
            )
            account_contract = await Operations.return_one_row(
                service=cnst.ACCOUNTS_CONTRACTS_UPDATE_SERVICE,
                statement=statement,
                db=db,
            )
            di.record_not_exist(
                instance=account_contract, exception=AccContractNotExist
            )
            return account_contract
