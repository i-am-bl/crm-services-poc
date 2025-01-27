from typing import List

from pydantic import UUID4
from sqlalchemy import Select, and_, func, select, update

from ..models.accounts import Accounts
from ..utilities.utilities import DataUtils as di


class AccountsStms:
    def __init__(self, model: Accounts) -> None:
        self._accounts: Accounts = model

    @property
    def accounts(self):
        return self._accounts

    def get_account(self, account_uuid: UUID4):
        accounts = self._accounts
        return Select(accounts).where(
            and_(accounts.uuid == account_uuid, accounts.sys_deleted_at == None)
        )

    def get_accounts_by_uuids(self, account_uuids: List[UUID4]) -> Select:
        accounts = self._accounts
        return Select(accounts).where(
            and_(accounts.uuid.in_(account_uuids), accounts.sys_deleted_at == None)
        )

    def get_accounts(self, offset: int, limit: int) -> Select:
        accounts = self._accounts
        return (
            Select(accounts)
            .where(
                and_(accounts.sys_deleted_at == None, accounts.sys_deleted_at == None)
            )
            .offset(offset=offset)
            .limit(limit=limit)
        )

    def get_accounts_ct(self) -> int:
        accounts = self._accounts
        return (
            select(func.count())
            .select_from(accounts)
            .where(accounts.sys_deleted_at == None)
        )

    def update_account(self, account_uuid: UUID4, account_data: object) -> update:
        # TODO: review the utility dependency
        accounts = self._accounts
        return (
            update(accounts)
            .where(and_(accounts.uuid == account_uuid, accounts.sys_deleted_at == None))
            .values(di.set_empty_strs_null(account_data))
            .returning(accounts)
        )


def account_stms(model: Accounts) -> AccountsStms:
    return AccountsStms(model=model)
