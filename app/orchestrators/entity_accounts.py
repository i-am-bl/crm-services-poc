from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.accounts import AccountsInternalCreate
from ..schemas.entity_accounts import (
    AccountEntitiesPgRes,
    EntityAccountParentRes,
    EntityAccountsPgRes,
    EntityAccountsInternalCreate,
    EntityAccountsRes,
)
from ..services import accounts as accounts_srvcs
from ..services import entity_accounts as entity_accounts_srvcs
from ..services import entities as entities_srvcs
from ..utilities import pagination


class EntityAccountsReadOrch:
    """
    Orchestrates the retrieval of account and entity data, including pagination for account-entity relationships.

    :param accounts_read_srvc: Service responsible for reading account data.
    :type accounts_read_srvc: accounts_srvcs.ReadSrvc
    :param entities_read_srvc: Service responsible for reading entity data.
    :type entities_read_srvc: entities_srvcs.ReadSrvc
    :param entity_accounts_read_srvc: Service responsible for reading entity-account relationships.
    :type entity_accounts_read_srvc: entity_accounts_srvcs.ReadSrvc

    :ivar accounts_read_srvc: The accounts read service instance.
    :vartype accounts_read_srvc: accounts_srvcs.ReadSrvc
    :ivar entities_read_srvc: The entities read service instance.
    :vartype entities_read_srvc: entities_srvcs.ReadSrvc
    :ivar entity_accounts_read_srvc: The entity-accounts read service instance.
    :vartype entity_accounts_read_srvc: entity_accounts_srvcs.ReadSrvc
    """

    def __init__(
        self,
        accounts_read_srvc: accounts_srvcs.ReadSrvc,
        entities_read_srvc: entities_srvcs.ReadSrvc,
        entity_accounts_read_srvc: entity_accounts_srvcs.ReadSrvc,
    ) -> None:
        """
        Initializes the EntityAccountsReadOrch instance with the provided read services for accounts, entities,
        and entity-accounts.

        :param accounts_read_srvc: Service responsible for reading account data.
        :type accounts_read_srvc: accounts_srvcs.ReadSrvc
        :param entities_read_srvc: Service responsible for reading entity data.
        :type entities_read_srvc: entities_srvcs.ReadSrvc
        :param entity_accounts_read_srvc: Service responsible for reading entity-account relationships.
        :type entity_accounts_read_srvc: entity_accounts_srvcs.ReadSrvc
        """
        self._accounts_read_srvc: accounts_srvcs.ReadSrvc = accounts_read_srvc
        self._entities_read_srvc: entities_srvcs.ReadSrvc = entities_read_srvc
        self._entity_accounts_read_srvc: entity_accounts_srvcs.ReadSrvc = (
            entity_accounts_read_srvc
        )

    @property
    def accounts_read_srvc(self) -> accounts_srvcs.ReadSrvc:
        """
        Returns the accounts read service instance.

        :return: The accounts read service instance.
        :rtype: accounts_srvcs.ReadSrvc
        """
        return self._accounts_read_srvc

    @property
    def entities_read_srvc(self) -> entities_srvcs.ReadSrvc:
        """
        Returns the entities read service instance.

        :return: The entities read service instance.
        :rtype: entities_srvcs.ReadSrvc
        """
        return self._entities_read_srvc

    @property
    def entity_accounts_read_srvc(self) -> entity_accounts_srvcs.ReadSrvc:
        """
        Returns the entity-accounts read service instance.

        :return: The entity-accounts read service instance.
        :rtype: entity_accounts_srvcs.ReadSrvc
        """
        return self._entity_accounts_read_srvc

    async def paginated_account_entities(
        self, account_uuid: UUID4, page: int, limit: int, db: AsyncSession
    ) -> AccountEntitiesPgRes:
        """
        Retrieves paginated account entities based on the account UUID, page, and limit.

        :param account_uuid: The UUID of the account to fetch associated entities.
        :type account_uuid: UUID4
        :param page: The current page number.
        :type page: int
        :param limit: The number of records per page.
        :type limit: int
        :param db: The database session for performing queries.
        :type db: AsyncSession

        :return: Paginated response containing account entities.
        :rtype: AccountEntitiesPgRes
        """
        total_count = await self.entity_accounts_read_srvc.get_account_entities_ct(
            account_uuid=account_uuid, db=db
        )
        offset = pagination.page_offset(page=page, limit=limit)
        has_more = pagination.has_more_items(page=page, limit=limit)
        account_entities = await self.entity_accounts_read_srvc.get_account_entities(
            account_uuid=account_uuid, offset=offset, limit=limit, db=db
        )
        entity_uuids = [account_entity.uuid for account_entity in account_entities]
        entities = await self.entities_read_srvc.get_entities_by_uuids(
            entity_uuids=entity_uuids, db=db
        )
        if not isinstance(entities, list):
            entities = [entities]
        return AccountEntitiesPgRes(
            total=total_count, page=page, limit=limit, has_more=has_more, data=entities
        )

    async def paginated_entity_accounts(
        self, entity_uuid: UUID4, page: int, limit: int, db: AsyncSession
    ) -> EntityAccountsPgRes:
        """
        Retrieves paginated entity accounts based on the entity UUID, page, and limit.

        :param entity_uuid: The UUID of the entity to fetch associated accounts.
        :type entity_uuid: UUID4
        :param page: The current page number.
        :type page: int
        :param limit: The number of records per page.
        :type limit: int
        :param db: The database session for performing queries.
        :type db: AsyncSession

        :return: Paginated response containing entity accounts.
        :rtype: EntityAccountsPgRes
        """
        total_count = await self.entity_accounts_read_srvc.get_entity_accounts_ct(
            entity_uuid=entity_uuid, db=db
        )
        offset = pagination.page_offset(page=page, limit=limit)
        has_more = pagination.has_more_items(
            total_count=total_count, page=page, limit=limit
        )
        entity_accounts = await self.entity_accounts_read_srvc.get_entity_accounts(
            entity_uuid=entity_uuid, offset=offset, limit=limit, db=db
        )
        account_uuids = [entity_account.uuid for entity_account in entity_accounts]
        accounts = await self.accounts_read_srvc.get_accounts_by_uuids(
            account_uuids=account_uuids, db=db
        )
        if not isinstance(accounts, list):
            accounts = [accounts]
        return EntityAccountsPgRes(
            total=total_count, page=page, limit=limit, has_more=has_more, data=accounts
        )


class EntityAccountsCreateOrch:
    """
    Orchestrates the creation of accounts and entity-account relationships.

    :param accounts_create_srvc: Service responsible for creating account data.
    :type accounts_create_srvc: accounts_srvcs.CreateSrvc
    :param entity_accounts_create_srvc: Service responsible for creating entity-account relationships.
    :type entity_accounts_create_srvc: entity_accounts_srvcs.CreateSrvc

    :ivar accounts_create_srvc: The accounts creation service instance.
    :vartype accounts_create_srvc: accounts_srvcs.CreateSrvc
    :ivar entity_accounts_create_srvc: The entity-accounts creation service instance.
    :vartype entity_accounts_create_srvc: entity_accounts_srvcs.CreateSrvc
    """

    def __init__(
        self,
        accounts_create_srvc: accounts_srvcs.CreateSrvc,
        entity_accounts_create_srvc: entity_accounts_srvcs.CreateSrvc,
    ):
        """
        Initializes the EntityAccountsCreateOrch instance with the provided create services for accounts and entity-accounts.

        :param accounts_create_srvc: Service responsible for creating account data.
        :type accounts_create_srvc: accounts_srvcs.CreateSrvc
        :param entity_accounts_create_srvc: Service responsible for creating entity-account relationships.
        :type entity_accounts_create_srvc: entity_accounts_srvcs.CreateSrvc
        """
        self._accounts_create_srvc: accounts_srvcs.CreateSrvc = accounts_create_srvc
        self._entity_accounts_create_srvc: entity_accounts_srvcs.CreateSrvc = (
            entity_accounts_create_srvc
        )

    @property
    def accounts_create_srvc(self) -> accounts_srvcs.CreateSrvc:
        """
        Returns the accounts creation service instance.

        :return: The accounts creation service instance.
        :rtype: accounts_srvcs.CreateSrvc
        """
        return self._accounts_create_srvc

    @property
    def entity_accounts_create_srvc(self) -> entity_accounts_srvcs.CreateSrvc:
        """
        Returns the entity-accounts creation service instance.

        :return: The entity-accounts creation service instance.
        :rtype: entity_accounts_srvcs.CreateSrvc
        """
        return self._entity_accounts_create_srvc

    async def create_account(
        self,
        entity_uuid: UUID4,
        account_data: AccountsInternalCreate,
        entity_account_data: EntityAccountsInternalCreate,
        db: AsyncSession,
    ) -> EntityAccountsRes:
        """
        Creates an account and associates it with an entity by creating an entity-account relationship.

        :param entity_uuid: The UUID of the entity to associate with the new account.
        :type entity_uuid: UUID4
        :param account_data: Data used to create the new account.
        :type account_data: AccountsInternalCreate
        :param entity_account_data: Data used to create the entity-account relationship.
        :type entity_account_data: EntityAccountsInternalCreate
        :param db: The database session for performing queries.
        :type db: AsyncSession

        :return: A response containing newly created entity account.
        :rtype: EntityAccountRes
        """
        account = await self._accounts_create_srvc.create_account(
            account_data=account_data, db=db
        )
        await db.flush()
        setattr(entity_account_data, "account_uuid", account.uuid)
        return await self._entity_accounts_create_srvc.create_entity_account(
            entity_uuid=entity_uuid, entity_account_data=entity_account_data, db=db
        )
