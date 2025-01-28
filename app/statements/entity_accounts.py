from pydantic import UUID4
from sqlalchemy import Select, Update, and_, func, update, values

from ..models.entity_accounts import EntityAccounts

from ..utilities.utilities import DataUtils as di


class EntityAccountsStms:
    def __init__(self, model: EntityAccounts) -> None:
        self._model: EntityAccounts = model

    @property
    def model(self) -> EntityAccounts:
        return self._model

    def get_entity_account(
        self, entity_uuid: UUID4, entity_account_uuid: UUID4
    ) -> Select:
        entity_accounts = self._model
        return Select(entity_accounts).where(
            entity_accounts.entity_uuid == entity_uuid,
            entity_accounts.uuid == entity_account_uuid,
            entity_accounts.sys_deleted_at == None,
        )

    def get_account_entity(
        self, account_uuid: UUID4, entity_account_uuid: UUID4
    ) -> Select:
        entity_accounts = self._model
        return Select(entity_accounts).where(
            entity_accounts.account_uuid == account_uuid,
            entity_accounts.uuid == entity_account_uuid,
            entity_accounts.sys_deleted_at == None,
        )

    def get_entity_accounts(
        self, entity_uuid: UUID4, limit: int, offset: int
    ) -> Select:
        entity_accounts = self._model
        return (
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

    def get_account_entities(
        self, account_uuid: UUID4, limit: int, offset: int
    ) -> Select:
        entity_accounts = self._model
        return (
            Select(entity_accounts)
            .where(
                and_(
                    entity_accounts.account_uuid == account_uuid,
                    entity_accounts.sys_deleted_at == None,
                )
            )
            .offset(offset=offset)
            .limit(limit=limit)
        )

    def get_entity_account_ct(self, entity_uuid: UUID4) -> Select:
        entity_accounts = self._model
        return (
            Select(func.count())
            .select_from(entity_accounts)
            .where(
                and_(
                    entity_accounts.entity_uuid == entity_uuid,
                    entity_accounts.sys_deleted_at == None,
                )
            )
        )

    def get_account_entities_ct(self, account_uuid: UUID4) -> Select:
        entity_accounts = self._model
        return (
            Select(func.count())
            .select_from(entity_accounts)
            .where(
                and_(
                    entity_accounts.account_uuid == account_uuid,
                    entity_accounts.sys_deleted_at == None,
                )
            )
        )

    def get_entity_account_by_parent(self, entity_uuid: UUID4, account_uuid: UUID4):
        entity_accounts = self._model
        return Select(entity_accounts).where(
            and_(
                entity_accounts.entity_uuid == entity_uuid,
                entity_accounts.account_uuid == account_uuid,
                entity_accounts.sys_deleted_at == None,
            )
        )

    def update_entity_account(
        self,
        entity_uuid: UUID4,
        entity_account_uuid: UUID4,
        entity_account_data: object,
    ) -> Update:
        entity_accounts = self._model
        return (
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

    def update_account_entity(
        self,
        account_uuid: UUID4,
        entity_account_uuid: UUID4,
        entity_account_data: object,
    ) -> Update:
        entity_accounts = self._model
        return (
            update(entity_accounts)
            .where(
                and_(
                    entity_accounts.account_uuid == account_uuid,
                    entity_accounts.uuid == entity_account_uuid,
                    entity_accounts.sys_deleted_at == None,
                )
            )
            .values(di.set_empty_strs_null(entity_account_data))
            .returning(entity_accounts)
        )
