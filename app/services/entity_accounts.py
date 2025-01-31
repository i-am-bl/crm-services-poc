from typing import List
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ..constants import constants as cnst
from ..database.operations import Operations
from ..exceptions import EntityAccExists, EntityAccNotExist
from ..models.entity_accounts import EntityAccounts

from ..schemas.entity_accounts import (
    AccountEntityInternalCreate,
    EntityAccountsCreate,
    EntityAccountsDel,
    EntityAccountsDelRes,
    EntityAccountsInternalUpdate,
    EntityAccountsRes,
    EntityAccountsUpdate,
)
from ..statements.entity_accounts import EntityAccountsStms
from ..utilities.data import record_exists, record_not_exist


class ReadSrvc:
    """
    Service for reading entity account data from the database.

    This class provides functionality to fetch entity account records based on various criteria.

    :param statements: The SQL statements used for fetching entity account data.
    :type statements: EntityAccountsStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(self, statements: EntityAccounts, db_operations: Operations) -> None:
        """
        Initializes the ReadSrvc class with the provided statements and database operations.

        :param statements: The SQL statements used for fetching entity account data.
        :type statements: EntityAccountsStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: EntityAccountsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> EntityAccountsStms:
        """
        Returns the entity account-related SQL statements.

        :return: The entity account-related SQL statements.
        :rtype: EntityAccountsStms
        """
        return self._statements

    @property
    def db_operations(self) -> Operations:
        """
        Returns the database operations object.

        :return: The database operations object.
        :rtype: Operations
        """
        return self._db_ops

    async def get_entity_account(
        self,
        entity_uuid: UUID4,
        entity_account_uuid: UUID4,
        db: AsyncSession,
    ) -> EntityAccountsRes:
        """
        Fetches a specific entity account record based on the entity UUID and entity account UUID.

        :param entity_uuid: The UUID of the entity.
        :type entity_uuid: UUID4
        :param entity_account_uuid: The UUID of the entity account.
        :type entity_account_uuid: UUID4
        :param db: The database session.
        :type db: AsyncSession
        :return: The entity account data.
        :rtype: EntityAccountsRes
        :raises EntityAccNotExist: If the entity account does not exist.
        """
        statement = self._statements.get_entity_account(
            entity_uuid=entity_uuid, entity_account_uuid=entity_account_uuid
        )
        entity_account: EntityAccountsRes = await self._db_ops.return_one_row(
            service=cnst.ENTITY_ACCOUNTS_READ_SERV, statement=statement, db=db
        )
        return record_not_exist(instance=entity_account, exception=EntityAccNotExist)

    async def get_account_entity(
        self,
        account_uuid: UUID4,
        entity_account_uuid: UUID4,
        db: AsyncSession,
    ) -> EntityAccountsRes:
        """
        Fetches a specific entity account record based on the account UUID and entity account UUID.

        :param account_uuid: The UUID of the account.
        :type account_uuid: UUID4
        :param entity_account_uuid: The UUID of the entity account.
        :type entity_account_uuid: UUID4
        :param db: The database session.
        :type db: AsyncSession
        :return: The entity account data.
        :rtype: EntityAccountsRes
        :raises EntityAccNotExist: If the entity account does not exist.
        """
        statement = self._statements.get_account_entity(
            account_uuid=account_uuid, entity_account_uuid=entity_account_uuid
        )
        entity_account: EntityAccountsRes = await self._db_ops.return_one_row(
            service=cnst.ENTITY_ACCOUNTS_READ_SERV, statement=statement, db=db
        )
        return record_not_exist(instance=entity_account, exception=EntityAccNotExist)

    async def get_account_entities(
        self,
        account_uuid: UUID4,
        limit: int,
        offset: int,
        db: AsyncSession,
    ) -> List[EntityAccountsRes]:
        """
        Fetches a list of entity account records for a specific account, with pagination support.

        :param account_uuid: The UUID of the account.
        :type account_uuid: UUID4
        :param limit: The maximum number of records to fetch.
        :type limit: int
        :param offset: The number of records to skip before starting to return results.
        :type offset: int
        :param db: The database session.
        :type db: AsyncSession
        :return: A list of entity account data.
        :rtype: List[EntityAccountsRes]
        :raises EntityAccNotExist: If no entity accounts are found.
        """
        statement = self._statements.get_account_entities(
            account_uuid=account_uuid, limit=limit, offset=offset
        )
        entity_account: List[EntityAccountsRes] = await self._db_ops.return_all_rows(
            service=cnst.ENTITY_ACCOUNTS_READ_SERV, statement=statement, db=db
        )
        return record_not_exist(instance=entity_account, exception=EntityAccNotExist)

    async def get_entity_accounts(
        self,
        entity_uuid: UUID4,
        limit: int,
        offset: int,
        db: AsyncSession,
    ) -> List[EntityAccountsRes]:
        """
        Fetches a list of entity account records for a specific entity, with pagination support.

        :param entity_uuid: The UUID of the entity.
        :type entity_uuid: UUID4
        :param limit: The maximum number of records to fetch.
        :type limit: int
        :param offset: The number of records to skip before starting to return results.
        :type offset: int
        :param db: The database session.
        :type db: AsyncSession
        :return: A list of entity account data.
        :rtype: List[EntityAccountsRes]
        :raises EntityAccNotExist: If no entity accounts are found.
        """
        statement = self._statements.get_entity_accounts(
            entity_uuid=entity_uuid, limit=limit, offset=offset
        )
        entity_account = await self._db_ops.return_all_rows(
            service=cnst.ENTITY_ACCOUNTS_READ_SERV, statement=statement, db=db
        )
        return record_not_exist(instance=entity_account, exception=EntityAccNotExist)

    async def get_entity_accounts_ct(
        self,
        entity_uuid: UUID4,
        db: AsyncSession,
    ) -> int:
        """
        Fetches the count of entity accounts for a specific entity.

        :param entity_uuid: The UUID of the entity.
        :type entity_uuid: UUID4
        :param db: The database session.
        :type db: AsyncSession
        :return: The count of entity accounts for the entity.
        :rtype: int
        """
        statement = self._statements.get_entity_account_ct(entity_uuid=entity_uuid)
        return await self._db_ops.return_count(
            service=cnst.ENTITY_ACCOUNTS_READ_SERV, statement=statement, db=db
        )

    async def get_account_entities_ct(
        self,
        account_uuid: UUID4,
        db: AsyncSession,
    ) -> int:
        """
        Fetches the count of entity accounts for a specific account.

        :param account_uuid: The UUID of the account.
        :type account_uuid: UUID4
        :param db: The database session.
        :type db: AsyncSession
        :return: The count of entity accounts for the account.
        :rtype: int
        """
        statement = self._statements.get_account_entities_ct(account_uuid=account_uuid)
        return await self._db_ops.return_count(
            service=cnst.ENTITY_ACCOUNTS_READ_SERV, statement=statement, db=db
        )


class CreateSrvc:
    """
    Handles the creation of EntityAccounts records in the database.

    This service provides functionality to create new entity account records in the database,
    ensuring that no duplicate records exist for the given entity and account UUIDs.

    :param statements: The SQL statements used for interacting with EntityAccounts.
    :type statements: EntityAccountsStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    :param model: The EntityAccounts model used for creating records in the database.
    :type model: EntityAccounts
    """

    def __init__(
        self,
        statements: EntityAccounts,
        db_operations: Operations,
        model: EntityAccounts,
    ) -> None:
        """
        Initializes the CreateSrvc class with the provided statements, database operations,
        and the EntityAccounts model.

        :param statements: The SQL statements used for interacting with EntityAccounts.
        :type statements: EntityAccountsStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        :param model: The EntityAccounts model used for creating records in the database.
        :type model: EntityAccounts
        """
        self._statements: EntityAccountsStms = statements
        self._db_ops: Operations = db_operations
        self._model: EntityAccounts = model

    @property
    def statements(self) -> EntityAccountsStms:
        """
        Returns the instance of EntityAccountsStms.

        :returns: The SQL statements for EntityAccounts operations.
        :rtype: EntityAccountsStms
        """
        return self._statements

    @property
    def db_operations(self) -> Operations:
        """
        Returns the instance of Operations.

        :returns: The database operations handler.
        :rtype: Operations
        """
        return self._db_ops

    @property
    def model(self) -> EntityAccounts:
        """
        Returns the EntityAccounts model.

        :returns: The model used for creating records.
        :rtype: EntityAccounts
        """
        return self._model

    async def create_entity_account(
        self,
        entity_uuid: UUID4,
        entity_account_data: EntityAccountsCreate,
        db: AsyncSession,
    ) -> EntityAccountsRes:
        """
        Creates a new EntityAccounts record by first checking if the account already exists
        for the given entity_uuid and entity_account_data.account_uuid.

        :param entity_uuid: The UUID of the entity for which the account is being created.
        :type entity_uuid: UUID4
        :param entity_account_data: The data used to create a new EntityAccounts record.
        :type entity_account_data: EntityAccountsCreate
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The result of the creation process, either the created entity account
                  or an error if the record already exists.
        :rtype: EntityAccountsRes
        """
        statement = self._statements.get_entity_account_by_parent(
            entity_uuid=entity_uuid,
            account_uuid=entity_account_data.account_uuid,
        )
        entity_accounts = self._model

        entity_account_exists: EntityAccountsRes = await self._db_ops.return_one_row(
            service=cnst.ENTITY_ACCOUNTS_CREATE_SERV, statement=statement, db=db
        )

        record_exists(instance=entity_account_exists, exception=EntityAccExists)

        entity_account: EntityAccountsRes = await self._db_ops.add_instance(
            service=cnst.ENTITY_ACCOUNTS_CREATE_SERV,
            model=entity_accounts,
            data=entity_account_data,
            db=db,
        )
        return record_not_exist(instance=entity_account, exception=EntityAccNotExist)

    async def create_account_entity(
        self,
        account_uuid: UUID4,
        entity_account_data: AccountEntityInternalCreate,
        db: AsyncSession,
    ) -> EntityAccountsRes:
        """
        Creates a new EntityAccounts record by first checking if the entity already exists
        for the given account_uuid and entity_account_data.entity_uuid.

        :param account_uuid: The UUID of the account for which the entity account is being created.
        :type account_uuid: UUID4
        :param entity_account_data: The data used to create a new EntityAccounts record.
        :type entity_account_data: AccountEntityInternalCreate
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The result of the creation process, either the created account entity
                  or an error if the record already exists.
        :rtype: EntityAccountsRes
        """
        statement = self._statements.get_entity_account_by_parent(
            entity_uuid=entity_account_data.entity_uuid,
            account_uuid=account_uuid,
        )
        entity_accounts = self._model

        entity_account_exists: EntityAccountsRes = await self._db_ops.return_one_row(
            service=cnst.ENTITY_ACCOUNTS_CREATE_SERV, statement=statement, db=db
        )

        record_exists(instance=entity_account_exists, exception=EntityAccExists)

        entity_account: EntityAccountsRes = await self._db_ops.add_instance(
            service=cnst.ENTITY_ACCOUNTS_CREATE_SERV,
            model=entity_accounts,
            data=entity_account_data,
            db=db,
        )
        return record_not_exist(instance=entity_account, exception=EntityAccNotExist)


class UpdateSrvc:
    """
    Service for updating entity account data in the database.

    This class provides functionality to update existing entity account records.

    :param statements: The SQL statements used for updating entity account data.
    :type statements: EntityAccountsStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(self, statements: EntityAccounts, db_operations: Operations) -> None:
        """
        Initializes the UpdateSrvc class with the provided statements and database operations.

        :param statements: The SQL statements used for updating entity account data.
        :type statements: EntityAccountsStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: EntityAccountsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> EntityAccountsStms:
        """
        Returns the entity account-related SQL statements.

        :return: The entity account-related SQL statements.
        :rtype: EntityAccountsStms
        """
        return self._statements

    @property
    def db_operations(self) -> Operations:
        """
        Returns the database operations object.

        :return: The database operations object.
        :rtype: Operations
        """
        return self._db_ops

    async def update_entity_account(
        self,
        entity_uuid: UUID4,
        entity_account_uuid: UUID4,
        entity_account_data: EntityAccountsUpdate,
        db: AsyncSession,
    ) -> EntityAccountsRes:
        """
        Updates an entity account record in the database.

        :param entity_uuid: The UUID of the entity whose account is being updated.
        :type entity_uuid: UUID4
        :param entity_account_uuid: The UUID of the entity account to update.
        :type entity_account_uuid: UUID4
        :param entity_account_data: The data to update the entity account with.
        :type entity_account_data: EntityAccountsUpdate
        :param db: The database session used to execute the query.
        :type db: AsyncSession

        :return: The updated entity account record.
        :rtype: EntityAccountsRes
        """
        statement = self._statements.update_entity_account(
            entity_uuid=entity_uuid,
            entity_account_uuid=entity_account_uuid,
            entity_account_data=entity_account_data,
        )
        entity_account = await self._db_ops.return_one_row(
            service=cnst.ENTITY_ACCOUNTS_UPDATE_SERV,
            statement=statement,
            db=db,
        )
        return record_not_exist(instance=entity_account, exception=EntityAccNotExist)

    async def update_account_entity(
        self,
        account_uuid: UUID4,
        entity_account_uuid: UUID4,
        entity_account_data: EntityAccountsInternalUpdate,
        db: AsyncSession,
    ) -> EntityAccountsRes:
        """
        Updates an account entity record in the database.

        :param account_uuid: The UUID of the account whose entity is being updated.
        :type account_uuid: UUID4
        :param entity_account_uuid: The UUID of the entity account to update.
        :type entity_account_uuid: UUID4
        :param entity_account_data: The data to update the account entity with.
        :type entity_account_data: EntityAccountsInternalUpdate
        :param db: The database session used to execute the query.
        :type db: AsyncSession

        :return: The updated account entity record.
        :rtype: EntityAccountsRes
        """
        statement = self._statements.update_account_entity(
            account_uuid=account_uuid,
            entity_account_uuid=entity_account_uuid,
            entity_account_data=entity_account_data,
        )
        entity_account = await self._db_ops.return_one_row(
            service=cnst.ENTITY_ACCOUNTS_UPDATE_SERV,
            statement=statement,
            db=db,
        )
        return record_not_exist(instance=entity_account, exception=EntityAccNotExist)


class DelSrvc:
    """
    Service for deleting (soft delete) entity account data in the database.

    This class provides functionality to delete entity account records with soft deletion.

    :param statements: The SQL statements used for soft deleting entity account data.
    :type statements: EntityAccountsStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(self, statements: EntityAccounts, db_operations: Operations) -> None:
        """
        Initializes the DelSrvc class with the provided statements and database operations.

        :param statements: The SQL statements used for soft deleting entity account data.
        :type statements: EntityAccountsStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: EntityAccountsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> EntityAccountsStms:
        """
        Returns the entity account-related SQL statements.

        :return: The entity account-related SQL statements.
        :rtype: EntityAccountsStms
        """
        return self._statements

    @property
    def db_operations(self) -> Operations:
        """
        Returns the database operations object.

        :return: The database operations object.
        :rtype: Operations
        """
        return self._db_ops

    async def soft_del_entity_account(
        self,
        entity_uuid: UUID4,
        entity_account_uuid: UUID4,
        entity_account_data: EntityAccountsDel,
        db: AsyncSession,
    ) -> EntityAccountsDelRes:
        """
        Soft deletes an entity account record from the database.

        :param entity_uuid: The UUID of the entity whose account is being deleted.
        :type entity_uuid: UUID4
        :param entity_account_uuid: The UUID of the entity account to delete.
        :type entity_account_uuid: UUID4
        :param entity_account_data: The data used to perform the soft delete.
        :type entity_account_data: EntityAccountsDel
        :param db: The database session used to execute the query.
        :type db: AsyncSession

        :return: The deleted entity account record.
        :rtype: EntityAccountsDelRes
        """
        statement = self._statements.update_entity_account(
            entity_uuid=entity_uuid,
            entity_account_uuid=entity_account_uuid,
            entity_account_data=entity_account_data,
        )
        entity_account = await self._db_ops.return_one_row(
            service=cnst.ENTITY_ACCOUNTS_UPDATE_SERV,
            statement=statement,
            db=db,
        )
        return record_not_exist(instance=entity_account, exception=EntityAccNotExist)

    async def soft_del_account_entity(
        self,
        account_uuid: UUID4,
        entity_account_uuid: UUID4,
        entity_account_data: EntityAccountsDel,
        db: AsyncSession,
    ) -> EntityAccountsDelRes:
        """
        Soft deletes an account entity record from the database.

        :param account_uuid: The UUID of the account whose entity is being deleted.
        :type account_uuid: UUID4
        :param entity_account_uuid: The UUID of the entity account to delete.
        :type entity_account_uuid: UUID4
        :param entity_account_data: The data used to perform the soft delete.
        :type entity_account_data: EntityAccountsDel
        :param db: The database session used to execute the query.
        :type db: AsyncSession

        :return: The deleted account entity record.
        :rtype: EntityAccountsDelRes
        """
        statement = self._statements.update_account_entity(
            account_uuid=account_uuid,
            entity_account_uuid=entity_account_uuid,
            entity_account_data=entity_account_data,
        )
        entity_account = await self._db_ops.return_one_row(
            service=cnst.ENTITY_ACCOUNTS_UPDATE_SERV,
            statement=statement,
            db=db,
        )
        return record_not_exist(instance=entity_account, exception=EntityAccNotExist)
