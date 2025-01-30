from typing import List
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ..constants import constants as cnst
from ..database.operations import Operations
from ..exceptions import NumberExists, NumbersNotExist
from ..models.numbers import Numbers
from ..schemas.numbers import (
    NumbersCreate,
    NumbersDel,
    NumbersDelRes,
    NumbersPgRes,
    NumbersRes,
    NumbersUpdate,
)
from ..statements.numbers import NumbersStms
from ..utilities import pagination
from ..utilities.data import record_exists, record_not_exist


class ReadSrvc:
    """
    Service for reading number data related to an entity.

    This class provides methods to retrieve individual numbers or a collection of numbers
    for a given entity, including paginated results.

    :param statements: The SQL statements used for querying number data from the database.
    :type statements: NumbersStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(self, statements: NumbersStms, db_operations: Operations) -> None:
        """
        Initializes the ReadSrvc class with the provided statements and database operations.

        :param statements: The SQL statements used for querying number data from the database.
        :type statements: NumbersStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: NumbersStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> NumbersStms:
        """
        Returns the instance of NumbersStms.

        :returns: The SQL statements for querying number data.
        :rtype: NumbersStms
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

    async def get_number(
        self,
        entity_uuid: UUID4,
        number_uuid: UUID4,
        db: AsyncSession,
    ) -> NumbersRes:
        """
        Retrieves a specific number by its UUID and associated entity UUID.

        :param entity_uuid: The UUID of the entity to which the number belongs.
        :type entity_uuid: UUID4
        :param number_uuid: The UUID of the number to be retrieved.
        :type number_uuid: UUID4
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The number data for the specified UUID.
        :rtype: NumbersRes
        """
        statement = self._statements.get_number(
            entity_uuid=entity_uuid,
            number_uuid=number_uuid,
        )
        number: NumbersRes = await self._db_ops.return_one_row(
            service=cnst.NUMBERS_READ_SERVICE, statement=statement, db=db
        )
        return record_not_exist(instance=number, exception=NumbersNotExist)

    async def get_numbers(
        self,
        entity_uuid: UUID4,
        limit: int,
        offset: int,
        db: AsyncSession,
    ) -> List[NumbersRes]:
        """
        Retrieves a list of numbers associated with a specific entity.

        :param entity_uuid: The UUID of the entity to which the numbers belong.
        :type entity_uuid: UUID4
        :param limit: The maximum number of numbers to retrieve.
        :type limit: int
        :param offset: The starting point to retrieve numbers (for pagination).
        :type offset: int
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: A list of numbers associated with the given entity.
        :rtype: List[NumbersRes]
        """
        statement = self._statements.get_number_by_entity(
            entity_uuid=entity_uuid, limit=limit, offset=offset
        )
        numbers: List[NumbersRes] = await self._db_ops.return_all_rows(
            service=cnst.NUMBERS_READ_SERVICE, statement=statement, db=db
        )
        return record_not_exist(instance=numbers, exception=NumbersNotExist)

    async def get_numbers_ct(
        self,
        entity_uuid: UUID4,
        db: AsyncSession,
    ) -> int:
        """
        Retrieves the count of numbers associated with a specific entity.

        :param entity_uuid: The UUID of the entity to count the associated numbers for.
        :type entity_uuid: UUID4
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The count of numbers associated with the given entity.
        :rtype: int
        """
        statement = self._statements.get_number_by_entity_ct(entity_uuid=entity_uuid)
        return await self._db_ops.return_count(
            service=cnst.NUMBERS_READ_SERVICE, statement=statement, db=db
        )

    async def paginated_numbers(
        self, entity_uuid: UUID4, page: int, limit: int, db: AsyncSession
    ) -> NumbersPgRes:
        """
        Retrieves paginated numbers for a specific entity.

        This method includes the total count of numbers, the current page, and whether more numbers
        are available on the next page.

        :param entity_uuid: The UUID of the entity to which the numbers belong.
        :type entity_uuid: UUID4
        :param page: The page number to retrieve.
        :type page: int
        :param limit: The number of items per page.
        :type limit: int
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: A paginated result containing numbers, total count, and pagination information.
        :rtype: NumbersPgRes
        """
        total_count = await self.get_numbers_ct(entity_uuid=entity_uuid, db=db)
        offset = pagination.page_offset(page=page, limit=limit)
        has_more = pagination.has_more_items(
            total_count=total_count, page=page, limit=limit
        )
        numbers = await self.get_numbers(
            entity_uuid=entity_uuid, offset=offset, limit=limit, db=db
        )
        return NumbersPgRes(
            total=total_count,
            page=page,
            limit=limit,
            has_more=has_more,
            numbers=numbers,
        )


class CreateSrvc:
    """
    Service for creating number data related to an entity.

    This class provides the method to create a new number entry for a specific entity
    and ensures the uniqueness of the number before adding it to the database.

    :param statements: The SQL statements used for querying and manipulating number data in the database.
    :type statements: NumbersStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    :param model: The model representing the number data structure.
    :type model: Numbers
    """

    def __init__(
        self, statements: NumbersStms, db_operations: Operations, model: Numbers
    ) -> None:
        """
        Initializes the CreateSrvc class with the provided statements, database operations, and model.

        :param statements: The SQL statements used for querying and manipulating number data in the database.
        :type statements: NumbersStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        :param model: The model representing the number data structure.
        :type model: Numbers
        """
        self._statements: NumbersStms = statements
        self._db_ops: Operations = db_operations
        self._model: Numbers = model

    @property
    def statements(self) -> NumbersStms:
        """
        Returns the instance of NumbersStms.

        :returns: The SQL statements for querying and manipulating number data.
        :rtype: NumbersStms
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
    def model(self) -> Numbers:
        """
        Returns the instance of Numbers model.

        :returns: The model representing the number data.
        :rtype: Numbers
        """
        return self._model

    async def create_number(
        self,
        entity_uuid: UUID4,
        number_data: NumbersCreate,
        db: AsyncSession,
    ) -> NumbersRes:
        """
        Creates a new number entry for a specific entity after checking for its uniqueness.

        This method checks if the number already exists in the database based on
        the combination of country code, area code, line number, and extension.
        If the number exists, it raises an exception. If the number doesn't exist,
        it adds the new number to the database.

        :param entity_uuid: The UUID of the entity to which the number belongs.
        :type entity_uuid: UUID4
        :param number_data: The data for the new number to be created.
        :type number_data: NumbersCreate
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The created number data if the operation is successful.
        :rtype: NumbersRes
        :raises NumberExists: If the number already exists in the database.
        :raises NumbersNotExist: If the number could not be created.
        """
        numbers = self._model
        statement = self._statements.get_number_by_number(
            entity_uuid=entity_uuid,
            country_code=number_data.country_code,
            area_code=number_data.area_code,
            line_number=number_data.line_number,
            ext=number_data.extension,
        )
        number_exists: NumbersRes = await self._db_ops.return_one_row(
            service=cnst.NUMBERS_CREATE_SERVICE, statement=statement, db=db
        )
        record_exists(instance=number_exists, exception=NumberExists)

        number: NumbersRes = await self._db_ops.add_instance(
            service=cnst.NUMBERS_CREATE_SERVICE,
            model=numbers,
            data=number_data,
            db=db,
        )
        return record_not_exist(instance=number, exception=NumbersNotExist)


class UpdateSrvc:
    """
    Service for updating number data related to an entity.

    This class provides the method to update the number details for a specific entity.

    :param statements: The SQL statements used for querying and manipulating number data in the database.
    :type statements: NumbersStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(self, statements: NumbersStms, db_operations: Operations) -> None:
        """
        Initializes the UpdateSrvc class with the provided statements and database operations.

        :param statements: The SQL statements used for querying and manipulating number data in the database.
        :type statements: NumbersStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: NumbersStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> NumbersStms:
        """
        Returns the instance of NumbersStms.

        :returns: The SQL statements for querying and manipulating number data.
        :rtype: NumbersStms
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

    async def update_number(
        self,
        entity_uuid: UUID4,
        number_uuid: UUID4,
        number_data: NumbersUpdate,
        db: AsyncSession,
    ) -> NumbersRes:
        """
        Updates an existing number for a specific entity.

        This method checks if the number exists in the database and updates it with the provided data.
        If the number doesn't exist, it raises an exception.

        :param entity_uuid: The UUID of the entity that owns the number.
        :type entity_uuid: UUID4
        :param number_uuid: The UUID of the number to be updated.
        :type number_uuid: UUID4
        :param number_data: The new data for the number.
        :type number_data: NumbersUpdate
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The updated number data if the operation is successful.
        :rtype: NumbersRes
        :raises NumbersNotExist: If the number doesn't exist in the database.
        """
        statement = self._statements.update_number(
            entity_uuid=entity_uuid,
            number_uuid=number_uuid,
            number_data=number_data,
        )
        number: NumbersRes = await self._db_ops.return_one_row(
            service=cnst.NUMBERS_UPDATE_SERVICE, statement=statement, db=db
        )
        return record_not_exist(instance=number, exception=NumbersNotExist)


class DelSrvc:
    """
    Service for deleting number data related to an entity.

    This class provides the method to soft delete a number entry from the database.

    :param statements: The SQL statements used for querying and manipulating number data in the database.
    :type statements: NumbersStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(self, statements: NumbersStms, db_operations: Operations) -> None:
        """
        Initializes the DelSrvc class with the provided statements and database operations.

        :param statements: The SQL statements used for querying and manipulating number data in the database.
        :type statements: NumbersStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: NumbersStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> NumbersStms:
        """
        Returns the instance of NumbersStms.

        :returns: The SQL statements for querying and manipulating number data.
        :rtype: NumbersStms
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

    async def soft_delete_number(
        self,
        entity_uuid: UUID4,
        number_uuid: UUID4,
        number_data: NumbersDel,
        db: AsyncSession,
    ) -> NumbersDelRes:
        """
        Soft deletes a number entry for a specific entity.

        This method marks the number as deleted without removing it from the database.

        :param entity_uuid: The UUID of the entity that owns the number.
        :type entity_uuid: UUID4
        :param number_uuid: The UUID of the number to be deleted.
        :type number_uuid: UUID4
        :param number_data: The data indicating how the number should be soft deleted.
        :type number_data: NumbersDel
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The soft-deleted number data if the operation is successful.
        :rtype: NumbersDelRes
        :raises NumbersNotExist: If the number doesn't exist in the database.
        """
        statement = self._statements.update_number(
            entity_uuid=entity_uuid,
            number_uuid=number_uuid,
            number_data=number_data,
        )
        number: NumbersDelRes = await self._db_ops.return_one_row(
            service=cnst.NUMBERS_DEL_SERVICE,
            statement=statement,
            db=db,
        )
        return record_not_exist(instance=number, exception=NumbersNotExist)
