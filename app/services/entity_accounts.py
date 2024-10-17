from math import e
from fastapi import Depends, status
from pydantic import UUID4
from sqlalchemy import Select, and_, func, update, values
from sqlalchemy.ext.asyncio import AsyncSession

import app.models.entity_accounts as m_entity_accounts
import app.schemas.entity_accounts as s_entity_accounts

from ..constants import constants as cnst
from ..database.database import Operations, get_db
from ..utilities.utilities import DataUtils as di
from ..exceptions import EntityAccNotExist, EntityAccExists


class EntityAccountsModels:
    entity_accounts = m_entity_accounts.EntityAccounts


class EntityAccountsStatements:
    pass

    class SelStatements:
        pass

        @staticmethod
        def sel_e_acc_by_uuid(entity_uuid: UUID4, entity_account_uuid: UUID4):
            entity_accounts = EntityAccountsModels.entity_accounts
            statement = Select(entity_accounts).where(
                entity_accounts.entity_uuid == entity_uuid,
                entity_accounts.uuid == entity_account_uuid,
                entity_accounts.sys_deleted_at == None,
            )
            return statement

        @staticmethod
        def sel_e_accs_by_entity(entity_uuid: UUID4, limit: int, offset: int):
            entity_accounts = EntityAccountsModels.entity_accounts
            statement = (
                Select(entity_accounts)
                .where(
                    and_(
                        entity_accounts.entity_uuid == entity_uuid,
                        entity_accounts.sys_deleted_at == None,
                    )
                )
                .offset(offset=offset)
                .limit(limit=limit)
            )
            return statement

        @staticmethod
        def sel_entity_acc_ct(entity_uuid: UUID4):
            entity_accounts = EntityAccountsModels.entity_accounts
            statement = (
                Select(func.count())
                .select_from(entity_accounts)
                .where(
                    and_(
                        entity_accounts.entity_uuid == entity_uuid,
                        entity_accounts.sys_deleted_at == None,
                    )
                )
            )
            return statement

        @staticmethod
        def sel_e_acc_by_parent_uuids(entity_uuid: UUID4, account_uuid: UUID4):
            entity_accounts = EntityAccountsModels.entity_accounts
            statement = Select(entity_accounts).where(
                and_(
                    entity_accounts.entity_uuid == entity_uuid,
                    entity_accounts.account_uuid == account_uuid,
                    entity_accounts.sys_deleted_at == None,
                )
            )
            return statement

    class UpdateStatements:
        pass

        @staticmethod
        def update_e_acc_by_uuid(
            entity_uuid: UUID4, entity_account_uuid: UUID4, entity_account_data: object
        ):
            entity_accounts = EntityAccountsModels.entity_accounts
            statement = (
                update(entity_accounts)
                .where(
                    and_(
                        entity_accounts.entity_uuid == entity_uuid,
                        entity_accounts.uuid == entity_account_uuid,
                        entity_accounts.sys_deleted_at == None,
                    )
                )
                .values(di.set_empty_strs_null(entity_account_data))
                .returning(entity_accounts)
            )
            return statement


class EntityAccountsServices:
    pass

    class ReadService:
        def __init__(self) -> None:
            pass

        async def get_entity_account(
            self,
            entity_uuid: UUID4,
            entity_account_uuid: UUID4,
            db: AsyncSession = Depends(get_db),
        ):
            statement = EntityAccountsStatements.SelStatements.sel_e_acc_by_uuid(
                entity_uuid=entity_uuid, entity_account_uuid=entity_account_uuid
            )
            entity_account = await Operations.return_one_row(
                service=cnst.ENTITY_ACCOUNTS_READ_SERV, statement=statement, db=db
            )
            di.record_not_exist(instance=entity_account, exception=EntityAccNotExist)
            return entity_account

        async def get_entity_accounts(
            self,
            entity_uuid: UUID4,
            limit: int,
            offset: int,
            db: AsyncSession = Depends(get_db),
        ):
            statement = EntityAccountsStatements.SelStatements.sel_e_accs_by_entity(
                entity_uuid=entity_uuid, limit=limit, offset=offset
            )
            entity_account = await Operations.return_all_rows(
                service=cnst.ENTITY_ACCOUNTS_READ_SERV, statement=statement, db=db
            )
            di.record_not_exist(instance=entity_account, exception=EntityAccNotExist)
            return entity_account

        async def get_entity_accounts_ct(
            self,
            entity_uuid: UUID4,
            db: AsyncSession = Depends(get_db),
        ):
            statement = EntityAccountsStatements.SelStatements.sel_entity_acc_ct(
                entity_uuid=entity_uuid
            )
            entity_accounts = await Operations.return_count(
                service=cnst.ENTITY_ACCOUNTS_READ_SERV, statement=statement, db=db
            )
            return entity_accounts

    class CreateService:
        def __init__(self) -> None:
            pass

        async def create_entity_account(
            self,
            entity_uuid: UUID4,
            entity_account_data: s_entity_accounts.EntityAccountsCreate,
            db: AsyncSession = Depends(get_db),
        ):
            statement = (
                EntityAccountsStatements.SelStatements.sel_e_acc_by_parent_uuids(
                    entity_uuid=entity_uuid,
                    account_uuid=entity_account_data.account_uuid,
                )
            )
            entity_accounts = EntityAccountsModels.entity_accounts

            entity_account_exists = await Operations.return_one_row(
                service=cnst.ENTITY_ACCOUNTS_CREATE_SERV, statement=statement, db=db
            )

            di.record_exists(instance=entity_account, exception=EntityAccExists)

            entity_account = await Operations.add_instance(
                service=cnst.ENTITY_ACCOUNTS_CREATE_SERV,
                model=entity_accounts,
                data=entity_account_data,
                db=db,
            )
            di.record_not_exist(instance=entity_account, exception=EntityAccNotExist)
            return entity_account

    class UpdateService:
        def __init__(self) -> None:
            pass

        async def update_entity_account(
            self,
            entity_uuid: UUID4,
            entity_account_uuid: UUID4,
            entity_account_data: s_entity_accounts.EntityAccountsUpdate,
            db: AsyncSession = Depends(get_db),
        ):
            statement = EntityAccountsStatements.UpdateStatements.update_e_acc_by_uuid(
                entity_uuid=entity_uuid,
                entity_account_uuid=entity_account_uuid,
                entity_account_data=entity_account_data,
            )
            entity_account = await Operations.return_one_row(
                service=cnst.ENTITY_ACCOUNTS_UPDATE_SERV,
                statement=statement,
                db=db,
            )
            di.record_not_exist(instance=entity_account, exception=EntityAccNotExist)
            return entity_account

    class DelService:
        def __init__(self) -> None:
            pass

        async def soft_del_entity_account(
            self,
            entity_uuid: UUID4,
            entity_account_uuid: UUID4,
            entity_account_data: s_entity_accounts.EntityAccountsDel,
            db: AsyncSession = Depends(get_db),
        ):
            statement = EntityAccountsStatements.UpdateStatements.update_e_acc_by_uuid(
                entity_uuid=entity_uuid,
                entity_account_uuid=entity_account_uuid,
                entity_account_data=entity_account_data,
            )
            entity_account = await Operations.return_one_row(
                service=cnst.ENTITY_ACCOUNTS_UPDATE_SERV,
                statement=statement,
                db=db,
            )
            di.record_not_exist(instance=entity_account, exception=EntityAccNotExist)
            return entity_account
