from typing import List
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ..constants import constants as cnst
from ..database.operations import Operations
from ..exceptions import NonIndividualExists, NonIndividualNotExist
from ..models.non_individuals import NonIndividuals
from ..schemas.non_individuals import (
    NonIndividualsCreate,
    NonIndividualsDel,
    NonIndividualsRes,
    NonIndividualsDelRes,
    NonIndividualsInternalUpdate,
)
from ..statements.non_individuals import NonIndivididualsStms
from ..utilities.data import record_not_exist, record_exists


class ReadSrvc:
    """
    Service for retrieving non-individual entities from the database.

    This class provides functionality to fetch non-individual entities (such as organizations or entities
    that are not individuals) from the database, including individual records and lists with pagination support.

    :param statements: The SQL statements used for querying non-individual entities.
    :type statements: NonIndivididualsStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(
        self, statements: NonIndivididualsStms, db_operations: Operations
    ) -> None:
        """
        Initializes the ReadSrvc class with the provided statements and database operations.

        :param statements: The SQL statements used for querying non-individual entities.
        :type statements: NonIndivididualsStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: NonIndivididualsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> NonIndivididualsStms:
        """
        Returns the instance of NonIndivididualsStms.

        :returns: The SQL statements for querying non-individual entities.
        :rtype: NonIndivididualsStms
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

    async def get_non_individual(
        self,
        entity_uuid: UUID4,
        db: AsyncSession,
    ) -> NonIndividualsRes:
        """
        Retrieves a single non-individual entity by its UUID.

        :param entity_uuid: The UUID of the non-individual entity to retrieve.
        :type entity_uuid: UUID4
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The non-individual entity if found, otherwise raises an exception.
        :rtype: NonIndividualsRes
        """
        statement = self._statements.get_non_individual(entity_uuid=entity_uuid)
        non_individual: NonIndividualsRes = await self._db_ops.return_one_row(
            service=cnst.NON_INDIVIDUALS_READ_SERV, statement=statement, db=db
        )
        return record_not_exist(
            instance=non_individual, exception=NonIndividualNotExist
        )

    async def get_non_individuals(
        self, offset: int, limit: int, db: AsyncSession
    ) -> List[NonIndividualsRes]:
        """
        Retrieves a list of non-individual entities with pagination support.

        :param offset: The number of records to skip before starting to return results.
        :type offset: int
        :param limit: The maximum number of records to return.
        :type limit: int
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: A list of non-individual entities.
        :rtype: List[NonIndividualsRes]
        """
        statement = self._statements.sel_non_indivs(offset=offset, limit=limit)
        non_individual: List[NonIndividualsRes] = await self._db_ops.return_all_rows(
            service=cnst.NON_INDIVIDUALS_READ_SERV, statement=statement, db=db
        )
        return record_not_exist(
            instance=non_individual, exception=NonIndividualNotExist
        )

    async def get_non_individuals_ct(
        self, offset: int, limit: int, db: AsyncSession
    ) -> int:
        """
        Retrieves the count of non-individual entities in the database.

        :param offset: The number of records to skip.
        :type offset: int
        :param limit: The maximum number of records to consider.
        :type limit: int
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The count of non-individual entities.
        :rtype: int
        """
        statement = self._statements.get_non_individuals_count()
        return await self._db_ops.return_count(
            service=cnst.NON_INDIVIDUALS_READ_SERV, statement=statement, db=db
        )


class CreateSrvc:
    """
    Service for creating non-individual entities in the database.

    This class provides functionality to create non-individual entities (such as organizations or entities
    that are not individuals) by inserting new records into the database.

    :param statements: The SQL statements used for querying and inserting non-individual entities.
    :type statements: NonIndivididualsStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    :param model: The model representing the non-individual entities.
    :type model: NonIndividuals
    """

    def __init__(
        self,
        statements: NonIndivididualsStms,
        db_operations: Operations,
        model: NonIndividuals,
    ) -> None:
        """
        Initializes the CreateSrvc class with the provided statements, database operations, and model.

        :param statements: The SQL statements used for querying and inserting non-individual entities.
        :type statements: NonIndivididualsStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        :param model: The model representing the non-individual entities.
        :type model: NonIndividuals
        """
        self._statements: NonIndivididualsStms = statements
        self._db_ops: Operations = db_operations
        self._model: NonIndividuals = model

    @property
    def statements(self) -> NonIndivididualsStms:
        """
        Returns the instance of NonIndivididualsStms.

        :returns: The SQL statements for querying non-individual entities.
        :rtype: NonIndivididualsStms
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
    def model(self) -> NonIndividuals:
        """
        Returns the instance of the NonIndividuals model.

        :returns: The model representing the non-individual entities.
        :rtype: NonIndividuals
        """
        return self._model

    async def create_non_individual(
        self,
        entity_uuid: UUID4,
        non_individual_data: NonIndividualsCreate,
        db: AsyncSession,
    ) -> NonIndividualsRes:
        """
        Creates a new non-individual entity in the database.

        This method checks whether the entity already exists, and if not, it creates a new entry in the database.

        :param entity_uuid: The UUID of the non-individual entity.
        :type entity_uuid: UUID4
        :param non_individual_data: The data for the new non-individual entity.
        :type non_individual_data: NonIndividualsCreate
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The created non-individual entity.
        :rtype: NonIndividualsRes
        """
        non_individuals = self._model
        statement = self._statements.sel_by_entity_ni_name(
            entity_uuid=entity_uuid, name=non_individual_data.name
        )
        non_individual_exists: NonIndividualsRes = await self._db_ops.return_one_row(
            service=cnst.NON_INDIVIDUALS_CREATE_SERV, statement=statement, db=db
        )
        record_exists(instance=non_individual_exists, exception=NonIndividualExists)
        non_individual: NonIndividualsRes = await self._db_ops.add_instance(
            service=cnst.NON_INDIVIDUALS_CREATE_SERV,
            model=non_individuals,
            data=non_individual_data,
            db=db,
        )
        return record_not_exist(
            instance=non_individual, exception=NonIndividualNotExist
        )


class UpdateSrvc:
    """
    Service for updating non-individual entities in the database.

    This class provides functionality to update existing non-individual entities by modifying their data
    in the database.

    :param statements: The SQL statements used for querying and updating non-individual entities.
    :type statements: NonIndivididualsStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(
        self, statements: NonIndivididualsStms, db_operations: Operations
    ) -> None:
        """
        Initializes the UpdateSrvc class with the provided statements and database operations.

        :param statements: The SQL statements used for querying and updating non-individual entities.
        :type statements: NonIndivididualsStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: NonIndivididualsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> NonIndivididualsStms:
        """
        Returns the instance of NonIndivididualsStms.

        :returns: The SQL statements for querying non-individual entities.
        :rtype: NonIndivididualsStms
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

    async def update_non_individual(
        self,
        entity_uuid: UUID4,
        non_individual_data: NonIndividualsInternalUpdate,
        db: AsyncSession,
    ) -> NonIndividualsRes:
        """
        Updates an existing non-individual entity in the database.

        :param entity_uuid: The UUID of the non-individual entity to update.
        :type entity_uuid: UUID4
        :param non_individual_data: The updated data for the non-individual entity.
        :type non_individual_data: NonIndividualsInternalUpdate
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The updated non-individual entity.
        :rtype: NonIndividualsRes
        """
        statement = self._statements.update_non_individual(
            entity_uuid=entity_uuid,
            non_individual_data=non_individual_data,
        )
        non_individual: NonIndividualsRes = await self._db_ops.return_one_row(
            service=cnst.NON_INDIVIDUALS_UPDATE_SERV, statement=statement, db=db
        )
        return record_not_exist(
            instance=non_individual, exception=NonIndividualNotExist
        )


class DelSrvc:
    """
    Service for soft deleting non-individual entities from the database.

    This class provides functionality to perform a soft deletion of non-individual entities, meaning that
    the entity is marked as deleted rather than completely removed from the database.

    :param statements: The SQL statements used for querying and updating non-individual entities.
    :type statements: NonIndivididualsStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(
        self, statements: NonIndivididualsStms, db_operations: Operations
    ) -> None:
        """
        Initializes the DelSrvc class with the provided statements and database operations.

        :param statements: The SQL statements used for querying and updating non-individual entities.
        :type statements: NonIndivididualsStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: NonIndivididualsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> NonIndivididualsStms:
        """
        Returns the instance of NonIndivididualsStms.

        :returns: The SQL statements for querying non-individual entities.
        :rtype: NonIndivididualsStms
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

    async def soft_del_non_individual(
        self,
        entity_uuid: UUID4,
        non_individual_uuid: UUID4,
        non_individual_data: NonIndividualsDel,
        db: AsyncSession,
    ) -> NonIndividualsDelRes:
        """
        Soft deletes a non-individual entity by updating its status in the database.

        This method performs a soft deletion, meaning it marks the non-individual entity as deleted
        instead of removing it from the database entirely.

        :param entity_uuid: The UUID of the entity to which the non-individual belongs.
        :type entity_uuid: UUID4
        :param non_individual_uuid: The UUID of the non-individual entity to be deleted.
        :type non_individual_uuid: UUID4
        :param non_individual_data: The data representing the non-individual entity to be deleted.
        :type non_individual_data: NonIndividualsDel
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The result of the soft delete operation, indicating the entity's updated state.
        :rtype: NonIndividualsDelRes
        """
        statement = self._statements.update_non_individual(
            entity_uuid=entity_uuid,
            non_individual_uuid=non_individual_uuid,
            non_individual_data=non_individual_data,
        )
        non_individual: NonIndividualsDelRes = await self._db_ops.return_one_row(
            service=cnst.NON_INDIVIDUALS_UPDATE_SERV, statement=statement, db=db
        )
        return record_not_exist(
            instance=non_individual, exception=NonIndividualNotExist
        )
