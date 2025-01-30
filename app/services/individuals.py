from typing import List
from pydantic import UUID4
from sqlalchemy import Select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..constants import constants as cnst
from ..database.operations import Operations
from ..exceptions import IndividualExists, IndividualNotExist
from ..models.individuals import Individuals
from ..schemas.individuals import (
    IndividualsCreate,
    IndividualsUpdate,
    IndividualsRes,
    IndividualsDel,
    IndividualsDelRes,
)
from ..statements.individuals import IndividualsStms
from ..utilities.data import record_not_exist, record_exists


class ReadSrvc:
    """
    Service for reading individual data from the database.

    This class provides functionality to fetch individual records based on various criteria such as
    entity UUID, pagination, and count.

    :param statements: The SQL statements used for interacting with individual records.
    :type statements: IndividualsStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(self, statements: IndividualsStms, db_operations: Operations) -> None:
        """
        Initializes the ReadSrvc class with the provided statements and database operations.

        :param statements: The SQL statements used for interacting with individual records.
        :type statements: IndividualsStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: IndividualsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> IndividualsStms:
        """
        Returns the instance of IndividualsStms.

        :returns: The SQL statements for individual operations.
        :rtype: IndividualsStms
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

    async def get_individual(
        self,
        entity_uuid: UUID4,
        db: AsyncSession,
    ) -> IndividualsRes:
        """
        Retrieves an individual record by the given entity UUID.

        :param entity_uuid: The UUID of the entity for which the individual record is being fetched.
        :type entity_uuid: UUID4
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The individual record corresponding to the entity UUID or an error if the record does not exist.
        :rtype: IndividualsRes
        """
        statement: Select = self._statements.get_individual(entity_uuid=entity_uuid)
        individual: IndividualsRes = await self._db_ops.return_one_row(
            service=cnst.INDIVIDUALS_READ_SERV, statement=statement, db=db
        )
        return record_not_exist(instance=individual, exception=IndividualNotExist)

    async def get_individuals(
        self,
        offset: int,
        limit: int,
        db: AsyncSession,
    ) -> List[IndividualsRes]:
        """
        Retrieves a list of individual records with pagination support.

        :param offset: The starting point for fetching individual records.
        :type offset: int
        :param limit: The maximum number of individual records to fetch.
        :type limit: int
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: A list of individual records or an error if no records are found.
        :rtype: List[IndividualsRes]
        """
        statement: Select = self._statements.get_individuals(offset=offset, limit=limit)
        individual: List[IndividualsRes] = await self._db_ops.return_all_rows(
            service=cnst.INDIVIDUALS_READ_SERV, statement=statement, db=db
        )
        return record_not_exist(instance=individual, exception=IndividualNotExist)

    async def get_individuals_ct(
        self,
        db: AsyncSession,
    ) -> int:
        """
        Retrieves the total count of individual records.

        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The count of individual records.
        :rtype: int
        """
        statement: Select = self._statements.get_individuals_ct()
        return await self._db_ops.return_count(
            service=cnst.INDIVIDUALS_READ_SERV, statement=statement, db=db
        )


class CreateSrvc:
    """
    Handles the creation of individual records in the database.

    This class provides functionality to create individual records, ensuring that no duplicate records
    exist for a given entity UUID.

    :param statements: The SQL statements used for interacting with individual records.
    :type statements: IndividualsStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    :param model: The Individuals model used for creating records in the database.
    :type model: Individuals
    """

    def __init__(
        self, statements: IndividualsStms, db_operations: Operations, model: Individuals
    ) -> None:
        """
        Initializes the CreateSrvc class with the provided statements, database operations, and model.

        :param statements: The SQL statements used for interacting with individual records.
        :type statements: IndividualsStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        :param model: The Individuals model used for creating records in the database.
        :type model: Individuals
        """
        self._statements: IndividualsStms = statements
        self._db_ops: Operations = db_operations
        self._model: Individuals = model

    @property
    def statements(self) -> IndividualsStms:
        """
        Returns the instance of IndividualsStms.

        :returns: The SQL statements for individual operations.
        :rtype: IndividualsStms
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
    def model(self) -> Individuals:
        """
        Returns the Individuals model.

        :returns: The model used for creating individual records.
        :rtype: Individuals
        """
        return self._model

    async def create_individual(
        self,
        entity_uuid: UUID4,
        individual_data: IndividualsCreate,
        db: AsyncSession,
    ) -> IndividualsRes:
        """
        Creates a new individual record if the record does not already exist for the given entity UUID.

        :param entity_uuid: The UUID of the entity for which the individual record is being created.
        :type entity_uuid: UUID4
        :param individual_data: The data used to create a new individual record.
        :type individual_data: IndividualsCreate
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The result of the creation process, either the created individual or an error if the record already exists.
        :rtype: IndividualsRes
        """
        statement: Select = self._statements.get_individual(entity_uuid=entity_uuid)
        individuals: Individuals = self._model
        individual_exists: IndividualsRes = await self._db_ops.return_one_row(
            service=cnst.INDIVIDUALS_CREATE_SERV, statement=statement, db=db
        )
        record_exists(instance=individual_exists, exception=IndividualExists)
        individual: IndividualsRes = await self._db_ops.add_instance(
            service=cnst.INDIVIDUALS_CREATE_SERV,
            model=individuals,
            data=individual_data,
            db=db,
        )
        return record_not_exist(instance=individual, exception=IndividualNotExist)


class UpdateSrvc:
    """
    Service for updating individual entity data in the database.

    This class provides functionality to update records for individuals based on their entity UUID.

    :param statements: The SQL statements used for updating individual data.
    :type statements: IndividualsStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(self, statements: IndividualsStms, db_operations: Operations) -> None:
        """
        Initializes the UpdateSrvc class with the provided statements and database operations.

        :param statements: The SQL statements used for updating individual data.
        :type statements: IndividualsStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: IndividualsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> IndividualsStms:
        """
        Returns the instance of IndividualsStms.

        :returns: The SQL statements for updating individual data.
        :rtype: IndividualsStms
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

    async def update_individual(
        self,
        entity_uuid: UUID4,
        individual_data: IndividualsUpdate,
        db: AsyncSession,
    ) -> IndividualsRes:
        """
        Updates an individual entity record in the database for the given entity UUID.

        :param entity_uuid: The UUID of the entity whose individual record is being updated.
        :type entity_uuid: UUID4
        :param individual_data: The data used to update the individual's record.
        :type individual_data: IndividualsUpdate
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The result of the update process, either the updated individual or an error if the record does not exist.
        :rtype: IndividualsRes
        """
        statement: update = self._statements.update_individual(
            entity_uuid=entity_uuid,
            individual_data=individual_data,
        )
        individual: IndividualsRes = await self._db_ops.return_one_row(
            service=cnst.INDIVIDUALS_UPDATE_SERV, statement=statement, db=db
        )
        return record_not_exist(instance=individual, exception=IndividualNotExist)


class DelSrvc:
    """
    Service for handling soft deletion of individual entity records in the database.

    This class provides functionality for marking an individual record as deleted based on its entity UUID.

    :param statements: The SQL statements used for deleting individual data.
    :type statements: IndividualsStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(self, statements: IndividualsStms, db_operations: Operations) -> None:
        """
        Initializes the DelSrvc class with the provided statements and database operations.

        :param statements: The SQL statements used for deleting individual data.
        :type statements: IndividualsStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: IndividualsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> IndividualsStms:
        """
        Returns the instance of IndividualsStms.

        :returns: The SQL statements for deleting individual data.
        :rtype: IndividualsStms
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

    async def soft_del_individual(
        self,
        entity_uuid: UUID4,
        individual_data: IndividualsDel,
        db: AsyncSession,
    ):
        """
        Marks an individual record as deleted in the database for the given entity UUID.

        :param entity_uuid: The UUID of the entity whose individual record is to be marked as deleted.
        :type entity_uuid: UUID4
        :param individual_data: The data used to soft delete the individual's record.
        :type individual_data: IndividualsDel
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The result of the deletion process, or an error if the record does not exist.
        :rtype: IndividualsDelRes
        """
        statement: update = self._statements.update_individual(
            entity_uuid=entity_uuid,
            individual_data=individual_data,
        )
        individual: IndividualsDelRes = await self._db_ops.return_one_row(
            service=cnst.INDIVIDUALS_DEL_SERV, statement=statement, db=db
        )
        return record_not_exist(instance=individual, exception=IndividualNotExist)
