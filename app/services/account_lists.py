from typing import List

from fastapi import Depends
from pydantic import UUID4
from sqlalchemy import Select, and_, func, update, values
from sqlalchemy.ext.asyncio import AsyncSession

import app.models.account_lists as m_account_lists
import app.schemas.account_lists as s_account_lists

from ..constants import constants as cnst
from ..database.database import Operations, get_db
from ..exceptions import AccListExists, AccListNotExist
from ..utilities.utilities import DataUtils as di


class AccountListsModels:
    account_lists = m_account_lists.AccountLists


class AccountListsStatements:
    pass

    class SelStatements:
        pass

        @staticmethod
        def sel_acc_ls_by_uuid(account_uuid: UUID4, account_list_uuid: UUID4):
            account_lists = AccountListsModels.account_lists
            statement = Select(account_lists).where(
                and_(
                    account_lists.account_uuid == account_uuid,
                    account_lists.uuid == account_list_uuid,
                    account_lists.sys_deleted_at == None,
                )
            )
            return statement

        @staticmethod
        def sel_acc_ls_by_acc(account_uuid: UUID4, limit: int, offset: int):
            account_lists = AccountListsModels.account_lists
            statement = (
                Select(account_lists)
                .where(
                    and_(
                        account_lists.account_uuid == account_uuid,
                        account_lists.sys_deleted_at == None,
                    )
                )
                .offset(offset=offset)
                .limit(limit=limit)
            )
            return statement

        @staticmethod
        def sel_acc_ls_ct(account_uuid: UUID4):
            account_lists = AccountListsModels.account_lists
            statement = (
                Select(func.count())
                .select_from(account_lists)
                .where(
                    and_(
                        account_lists.account_uuid == account_uuid,
                        account_lists.sys_deleted_at == None,
                    )
                )
            )
            return statement

        @staticmethod
        def sel_acc_ls_by_acc_prd(account_uuid: UUID4, product_list_uuid: UUID4):
            account_lists = AccountListsModels.account_lists
            statement = Select(account_lists).where(
                and_(
                    account_lists.account_uuid == account_uuid,
                    account_lists.product_list_uuid == product_list_uuid,
                    account_lists.sys_deleted_at == None,
                )
            )
            return statement

    class UpdateStatements:
        pass

        @staticmethod
        def update_acc_ls_by_uuid(
            account_uuid: UUID4, account_list_uuid: UUID4, account_list_data: object
        ):
            account_lists = AccountListsModels.account_lists
            statement = (
                update(account_lists)
                .where(
                    and_(
                        account_lists.account_uuid == account_uuid,
                        account_lists.uuid == account_list_uuid,
                        account_lists.sys_deleted_at == None,
                    )
                )
                .values(di.set_empty_strs_null(values=account_list_data))
                .returning(account_lists)
            )
            return statement


class AccountListsServices:
    pass

    class ReadService:
        def __init__(self) -> None:
            pass

        async def get_account_list(
            self,
            account_uuid: UUID4,
            account_list_uuid: UUID4,
            db: AsyncSession = Depends(get_db),
        ):
            statement = AccountListsStatements.SelStatements.sel_acc_ls_by_uuid(
                account_uuid=account_uuid, account_list_uuid=account_list_uuid
            )
            account_list = await Operations.return_one_row(
                service=cnst.ACCOUNTS_LISTS_READ_SERVICE, statement=statement, db=db
            )
            return di.record_not_exist(instance=account_list, exception=AccListNotExist)

        async def get_account_lists(
            self,
            account_uuid: UUID4,
            limit: int,
            offset: int,
            db: AsyncSession = Depends(get_db),
        ):
            statement = AccountListsStatements.SelStatements.sel_acc_ls_by_acc(
                account_uuid=account_uuid, limit=limit, offset=offset
            )
            account_lists = await Operations.return_all_rows(
                service=cnst.ACCOUNTS_LISTS_READ_SERVICE, statement=statement, db=db
            )
            return di.record_not_exist(
                instance=account_lists, exception=AccListNotExist
            )

        async def get_account_list_ct(
            self, account_uuid: UUID4, db: AsyncSession = Depends(get_db)
        ):
            statement = AccountListsStatements.SelStatements.sel_acc_ls_ct(
                account_uuid=account_uuid
            )
            return await Operations.return_count(
                service=cnst.ACCOUNTS_LISTS_READ_SERVICE, statement=statement, db=db
            )

    class CreateService:
        def __init__(self) -> None:
            pass

        async def create_account_list(
            self,
            account_uuid: UUID4,
            account_list_data: s_account_lists.AccountListsCreate,
            db: AsyncSession = Depends(get_db),
        ):
            account_lists = AccountListsModels.account_lists
            statement = AccountListsStatements.SelStatements.sel_acc_ls_by_acc_prd(
                account_uuid=account_uuid,
                product_list_uuid=account_list_data.product_list_uuid,
            )
            account_list_exists = await Operations.return_one_row(
                service=cnst.ACCOUNTS_LISTS_CREATE_SERVICE, statement=statement, db=db
            )
            di.record_exists(instance=account_list_exists, exception=AccListExists)

            account_list = await Operations.add_instance(
                service=cnst.ACCOUNTS_LISTS_CREATE_SERVICE,
                model=account_lists,
                data=account_list_data,
                db=db,
            )
            return di.record_not_exist(instance=account_list, exception=AccListNotExist)

    class UpdateService:
        def __init__(self) -> None:
            pass

        async def update_account_list(
            self,
            account_uuid: UUID4,
            account_list_uuid: UUID4,
            account_list_data: s_account_lists.AccountListsUpdate,
            db: AsyncSession = Depends(get_db),
        ):
            statement = AccountListsStatements.UpdateStatements.update_acc_ls_by_uuid(
                account_uuid=account_uuid,
                account_list_uuid=account_list_uuid,
                account_list_data=account_list_data,
            )
            account_list = await Operations.return_one_row(
                service=cnst.ACCOUNTS_LISTS_UPDATE_SERVICE, statement=statement, db=db
            )
            return di.record_not_exist(instance=account_list, exception=AccListNotExist)

    class DelService:
        def __init__(self) -> None:
            pass

        async def soft_del_account_list(
            self,
            account_uuid: UUID4,
            account_list_uuid: UUID4,
            account_list_data: s_account_lists.AccountListsDel,
            db: AsyncSession = Depends(get_db),
        ):
            statement = AccountListsStatements.UpdateStatements.update_acc_ls_by_uuid(
                account_uuid=account_uuid,
                account_list_uuid=account_list_uuid,
                account_list_data=account_list_data,
            )
            account_list = await Operations.return_one_row(
                service=cnst.ACCOUNTS_LISTS_UPDATE_SERVICE, statement=statement, db=db
            )
            return di.record_not_exist(instance=account_list, exception=AccListNotExist)
