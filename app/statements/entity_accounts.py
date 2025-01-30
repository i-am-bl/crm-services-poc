from pydantic import UUID4
from sqlalchemy import Select, Update, and_, func, update, values

from ..models.entity_accounts import EntityAccounts

from ..utilities.data import set_empty_strs_null


class EntityAccountsStms:
    """
    A class responsible for constructing SQLAlchemy queries and statements for managing entity-account relationships.

    ivars:
    ivar: _model: EntityAccounts: An instance of the EntityAccounts model.
    """

    def __init__(self, model: EntityAccounts) -> None:
        """
        Initializes the EntityAccountsStms class.

        :param model: EntityAccounts: An instance of the EntityAccounts model.
        :return: None
        """
        self._model = model

    @property
    def model(self) -> EntityAccounts:
        """
        Returns the EntityAccounts model.

        :return: EntityAccounts: The EntityAccounts model instance.
        """
        return self._model

    def get_entity_account(
        self, entity_uuid: UUID4, entity_account_uuid: UUID4
    ) -> Select:
        """
        Selects an entity-account relationship by entity UUID and entity account UUID.

        :param entity_uuid: UUID4: The UUID of the entity.
        :param entity_account_uuid: UUID4: The UUID of the entity account.
        :return: Select: A Select statement for the entity-account relationship.
        """
        entity_accounts = self._model
        return Select(entity_accounts).where(
            entity_accounts.entity_uuid == entity_uuid,
            entity_accounts.uuid == entity_account_uuid,
            entity_accounts.sys_deleted_at == None,
        )

    def get_account_entity(
        self, account_uuid: UUID4, entity_account_uuid: UUID4
    ) -> Select:
        """
        Selects an account-entity relationship by account UUID and entity account UUID.

        :param account_uuid: UUID4: The UUID of the account.
        :param entity_account_uuid: UUID4: The UUID of the entity account.
        :return: Select: A Select statement for the account-entity relationship.
        """
        entity_accounts = self._model
        return Select(entity_accounts).where(
            entity_accounts.account_uuid == account_uuid,
            entity_accounts.uuid == entity_account_uuid,
            entity_accounts.sys_deleted_at == None,
        )

    def get_entity_accounts(
        self, entity_uuid: UUID4, limit: int, offset: int
    ) -> Select:
        """
        Selects entity-account relationships by entity UUID with pagination.

        :param entity_uuid: UUID4: The UUID of the entity.
        :param limit: int: The number of records to return.
        :param offset: int: The number of records to skip.
        :return: Select: A Select statement for the entity-account relationships.
        """
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
        """
        Selects account-entity relationships by account UUID with pagination.

        :param account_uuid: UUID4: The UUID of the account.
        :param limit: int: The number of records to return.
        :param offset: int: The number of records to skip.
        :return: Select: A Select statement for the account-entity relationships.
        """
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
        """
        Selects the count of entity-account relationships for a specific entity.

        :param entity_uuid: UUID4: The UUID of the entity.
        :return: Select: A Select statement for the entity-account count.
        """
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
        """
        Selects the count of account-entity relationships for a specific account.

        :param account_uuid: UUID4: The UUID of the account.
        :return: Select: A Select statement for the account-entity count.
        """
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

    def get_entity_account_by_parent(
        self, entity_uuid: UUID4, account_uuid: UUID4
    ) -> Select:
        """
        Selects an entity-account relationship by both entity UUID and account UUID.

        :param entity_uuid: UUID4: The UUID of the entity.
        :param account_uuid: UUID4: The UUID of the account.
        :return: Select: A Select statement for the entity-account relationship by parent.
        """
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
        """
        Updates an entity-account relationship by entity UUID and entity account UUID.

        :param entity_uuid: UUID4: The UUID of the entity.
        :param entity_account_uuid: UUID4: The UUID of the entity account.
        :param entity_account_data: object: The data to update the entity-account relationship with.
        :return: Update: An Update statement for the entity-account relationship.
        """
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
            .values(set_empty_strs_null(entity_account_data))
            .returning(entity_accounts)
        )

    def update_account_entity(
        self,
        account_uuid: UUID4,
        entity_account_uuid: UUID4,
        entity_account_data: object,
    ) -> Update:
        """
        Updates an account-entity relationship by account UUID and entity account UUID.

        :param account_uuid: UUID4: The UUID of the account.
        :param entity_account_uuid: UUID4: The UUID of the entity account.
        :param entity_account_data: object: The data to update the account-entity relationship with.
        :return: Update: An Update statement for the account-entity relationship.
        """
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
            .values(set_empty_strs_null(entity_account_data))
            .returning(entity_accounts)
        )
