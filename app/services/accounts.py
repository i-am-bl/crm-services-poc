from abc import ABC, abstractmethod
from os import stat
from typing import Annotated, Literal

from fastapi import Depends, Query
from pydantic import UUID4
from sqlalchemy import Select, and_, update, select, func
from sqlalchemy.ext.asyncio import AsyncSession

import app.constants as cnst
import app.models.accounts as m_accounts
import app.schemas.accounts as s_accounts
from app.database.database import Operations, get_db
from app.services.utilities import DataUtils as di


class AccountsModels:
    accounts = m_accounts.Accounts


class AccountsStatements:
    pass

    class SelStatements:
        pass

        @staticmethod
        def sel_account_by_uuid(account_uuid: UUID4):
            accounts = AccountsModels.accounts
            statement = Select(accounts).where(accounts.uuid == account_uuid)
            return statement

        @staticmethod
        def sel_accounts(offset: int, limit: int):
            accounts = AccountsModels.accounts
            statement = (
                Select(accounts)
                .where(accounts.sys_deleted_at == None)
                .offset(offset=offset)
                .limit(limit=limit)
            )
            return statement

        @staticmethod
        def sel_count():
            accounts = AccountsModels.accounts
            statement = select(func.count()).select_from(m_accounts.Accounts)
            return statement

    class UpdateStatements:
        pass

        @staticmethod
        def update_account_by_uuid(account_uuid: UUID4, account_data: object):
            accounts = AccountsModels.accounts
            statement = (
                update(accounts)
                .where(accounts.uuid == account_uuid)
                .values(di.set_empty_strs_null(account_data))
                .returning(accounts)
            )
            return statement


class AccountsServices:
    pass

    class ReadService:
        def __init__(self) -> None:
            return

        async def get_account(
            self, account_uuid: UUID4, db: AsyncSession = Depends(get_db)
        ):
            statement = AccountsStatements.SelStatements.sel_account_by_uuid(
                account_uuid=account_uuid
            )
            account = await Operations.return_one_row(
                service=cnst.ACCOUNTS_READ_SERVICE, statement=statement, db=db
            )
            di.rec_not_exist_or_soft_del(account)
            return account

        async def get_accounts(
            self,
            offset: int,
            limit: int,
            db: AsyncSession = Depends(get_db),
        ):
            statement = AccountsStatements.SelStatements.sel_accounts(
                offset=offset, limit=limit
            )
            account = await Operations.return_all_rows(
                service=cnst.ACCOUNTS_READ_SERVICE, statement=statement, db=db
            )
            return account

        async def get_account_ct(self, db: AsyncSession = Depends(get_db)):
            statement = AccountsStatements.SelStatements.sel_count()
            total_count = await Operations.return_count(
                service=cnst.ACCOUNTS_READ_SERVICE,
                statement=statement,
                db=db,
            )
            return total_count

    class CreateService:
        def __init__(self) -> None:
            return

        async def create_account(
            self,
            account_data: s_accounts.AccountsCreate,
            db: AsyncSession = Depends(get_db),
        ):
            accounts = AccountsModels.accounts
            account = await Operations.add_instance(
                service=cnst.ACCOUNTS_CREATE_SERVICE,
                model=accounts,
                data=account_data,
                db=db,
            )
            di.record_not_exist(account)
            return account

    class UpdateService:
        def __init__(self) -> None:
            return

        async def update_account(
            self,
            account_uuid: UUID4,
            account_data: s_accounts.AccountsUpdate,
            db: AsyncSession = Depends(get_db),
        ):
            statement = AccountsStatements.UpdateStatements.update_account_by_uuid(
                account_uuid=account_uuid, account_data=account_data
            )
            account = await Operations.return_one_row(
                service=cnst.ACCOUNTS_UPDATE_SERVICE, statement=statement, db=db
            )
            di.rec_not_exist_or_soft_del(account)
            return account

    class DelService:
        def __init__(self) -> None:
            return

        async def sof_del_account(
            self,
            account_uuid: UUID4,
            account_data: s_accounts.AccountsDel,
            db: AsyncSession = Depends(get_db),
        ):
            statement = AccountsStatements.UpdateStatements.update_account_by_uuid(
                account_uuid=account_uuid, account_data=account_data
            )
            account = await Operations.return_one_row(
                service=cnst.ACCOUNTS_UPDATE_SERVICE, statement=statement, db=db
            )
            di.record_not_exist(account)
            return account
