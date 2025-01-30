from typing import List

from pydantic import UUID4
from sqlalchemy import Select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..constants import constants as cnst
from ..database.operations import Operations
from ..exceptions import EntityNotExist
from ..models.entities import Entities
from ..schemas.entities import (
    EntitiesCreate,
    EntitiesDel,
    EntitiesDelRes,
    EntitiesPgRes,
    EntitiesRes,
    EntitiesUpdate,
)
from ..statements.entities import EntitiesStms
from ..utilities import pagination
from ..utilities.data import record_not_exist


class ReadSrvc:
    """
    Service for reading entity data from the database.

    This class provides functionality to retrieve entities from the database based on different criteria
    such as UUID, pagination, and entity count.

    :param statements: The SQL statements used for reading entity data.
    :type statements: EntitiesStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(self, statements: EntitiesStms, db_operations: Operations) -> None:
        """
        Initializes the ReadSrvc class with the provided statements and database operations.

        :param statements: The SQL statements used for reading entity data.
        :type statements: EntitiesStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: EntitiesStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> EntitiesStms:
        """
        Returns the entity-related SQL statements.

        :return: The entity-related SQL statements.
        :rtype: EntitiesStms
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

    async def get_entity(self, entity_uuid: UUID4, db: AsyncSession) -> EntitiesRes:
        """
        Retrieves a single entity from the database by its UUID.

        :param entity_uuid: The UUID of the entity to retrieve.
        :type entity_uuid: UUID4
        :param db: The database session.
        :type db: AsyncSession
        :return: The retrieved entity data.
        :rtype: EntitiesRes
        :raises EntityNotExist: If the entity does not exist.
        """
        statement: Select = self._statements.get_entity(entity_uuid=entity_uuid)
        entity: EntitiesRes = await self._db_ops.return_one_row(
            service=cnst.ENTITIES_READ_SERV, statement=statement, db=db
        )
        return record_not_exist(instance=entity, exception=EntityNotExist)

    async def get_entities_by_uuids(self, entity_uuids: List[UUID4], db: AsyncSession):
        """
        Retrieves multiple entities from the database by their UUIDs.

        :param entity_uuids: A list of UUIDs for the entities to retrieve.
        :type entity_uuids: List[UUID4]
        :param db: The database session.
        :type db: AsyncSession
        :return: A list of the retrieved entity data.
        :rtype: List[EntitiesRes]
        :raises EntityNotExist: If no entities are found for the provided UUIDs.
        """
        statement: Select = self._statements.get_entities_by_uuids(
            entity_uuids=entity_uuids
        )
        entities: List[EntitiesRes] = await self._db_ops.return_all_rows_and_values(
            service=cnst.ENTITIES_READ_SERV, statement=statement, db=db
        )
        return record_not_exist(instance=entities, exception=EntityNotExist)

    async def get_entities(
        self,
        limit: int,
        offset: int,
        db: AsyncSession,
    ) -> List[EntitiesRes]:
        """
        Retrieves a list of entities from the database with pagination support.

        :param limit: The maximum number of entities to retrieve.
        :type limit: int
        :param offset: The offset from where to start retrieving entities.
        :type offset: int
        :param db: The database session.
        :type db: AsyncSession
        :return: A list of the retrieved entity data.
        :rtype: List[EntitiesRes]
        :raises EntityNotExist: If no entities are found.
        """
        statement: Select = self._statements.get_entities(limit=limit, offset=offset)
        entities: List[EntitiesRes] = await self._db_ops.return_all_rows(
            service=cnst.ENTITIES_READ_SERV, statement=statement, db=db
        )
        record_not_exist(instance=entities, exception=EntityNotExist)
        return entities

    async def get_entity_ct(self, db: AsyncSession) -> int:
        """
        Retrieves the count of entities in the database.

        :param db: The database session.
        :type db: AsyncSession
        :return: The total count of entities.
        :rtype: int
        """
        statement: Select = self._statements.get_entity_ct()
        return await self._db_ops.return_count(
            service=cnst.ENTITIES_READ_SERV, statement=statement, db=db
        )

    async def paginated_entities(
        self, page: int, limit: int, db: AsyncSession
    ) -> EntitiesPgRes:
        """
        Retrieves entities with pagination support, including metadata about the result.

        :param page: The page number to retrieve.
        :type page: int
        :param limit: The number of entities per page.
        :type limit: int
        :param db: The database session.
        :type db: AsyncSession
        :return: A paginated result with metadata about the total count and available pages.
        :rtype: EntitiesPgRes
        """
        total_count: int = await self.get_entity_ct(db=db)
        offset = pagination.page_offset(page=page, limit=limit)
        has_more = pagination.has_more_items(
            total_count=total_count, page=page, limit=limit
        )
        entities = await self.get_entities(offset=offset, limit=limit, db=db)
        return EntitiesPgRes(
            total=total_count, page=page, limit=limit, has_more=has_more, data=entities
        )


class CreateSrvc:
    """
    Service for creating new entity records in the database.

    This class provides functionality to add new entities into the database.

    :param statements: The SQL statements used for entity creation.
    :type statements: EntitiesStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    :param model: The model for the entity being created.
    :type model: Entities
    """

    def __init__(
        self, statements: EntitiesStms, db_operations: Operations, model: Entities
    ) -> None:
        """
        Initializes the CreateSrvc class with the provided statements, database operations, and model.

        :param statements: The SQL statements used for entity creation.
        :type statements: EntitiesStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        :param model: The model for the entity being created.
        :type model: Entities
        """
        self._statements: EntitiesStms = statements
        self._db_ops: Operations = db_operations
        self._model: Entities = model

    @property
    def statements(self) -> EntitiesStms:
        """
        Returns the entity-related SQL statements.

        :return: The entity-related SQL statements.
        :rtype: EntitiesStms
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

    async def create_entity(
        self,
        entity_data: EntitiesCreate,
        db: AsyncSession,
    ) -> EntitiesRes:
        """
        Creates a new entity in the database.

        :param entity_data: The data for the new entity.
        :type entity_data: EntitiesCreate
        :param db: The database session.
        :type db: AsyncSession
        :return: The created entity data.
        :rtype: EntitiesRes
        :raises EntityNotExist: If the entity already exists.
        """
        entities = self._model
        entity: EntitiesRes = await self._db_ops.add_instance(
            service=cnst.ENTITIES_CREATE_SERV,
            model=entities,
            data=entity_data,
            db=db,
        )
        return record_not_exist(instance=entity, exception=EntityNotExist)


class UpdateSrvc:
    """
    Service for updating existing entity records in the database.

    This class provides functionality to update entity data in the database.

    :param statements: The SQL statements used for entity updates.
    :type statements: EntitiesStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(self, statements: EntitiesStms, db_operations: Operations) -> None:
        """
        Initializes the UpdateSrvc class with the provided statements and database operations.

        :param statements: The SQL statements used for entity updates.
        :type statements: EntitiesStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: EntitiesStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> EntitiesStms:
        """
        Returns the entity-related SQL statements.

        :return: The entity-related SQL statements.
        :rtype: EntitiesStms
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

    async def update_entity(
        self,
        entity_uuid: UUID4,
        entity_data: EntitiesUpdate,
        db: AsyncSession,
    ):
        """
        Updates an existing entity in the database.

        :param entity_uuid: The UUID of the entity to update.
        :type entity_uuid: UUID4
        :param entity_data: The updated data for the entity.
        :type entity_data: EntitiesUpdate
        :param db: The database session.
        :type db: AsyncSession
        :return: The updated entity data.
        :rtype: EntitiesRes
        :raises EntityNotExist: If the entity does not exist.
        """
        statement: update = self._statements.update_entity(
            entity_uuid=entity_uuid, entity_data=entity_data
        )
        entity: EntitiesRes = await Operations.return_one_row(
            service=cnst.ENTITIES_UPDATE_SERV, statement=statement, db=db
        )
        return record_not_exist(instance=entity, exception=EntityNotExist)


class DelSrvc:
    """
    Service for soft-deleting entity records from the database.

    This class provides functionality to mark entities as deleted in the database.

    :param statements: The SQL statements used for entity deletion.
    :type statements: EntitiesStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(self, statements: EntitiesStms, db_operations: Operations) -> None:
        """
        Initializes the DelSrvc class with the provided statements and database operations.

        :param statements: The SQL statements used for entity deletion.
        :type statements: EntitiesStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: EntitiesStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> EntitiesStms:
        """
        Returns the entity-related SQL statements.

        :return: The entity-related SQL statements.
        :rtype: EntitiesStms
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

    async def soft_del_entity(
        self,
        entity_uuid: UUID4,
        entity_data: EntitiesDel,
        db: AsyncSession,
    ):
        """
        Soft-deletes an entity from the database by marking it as deleted.

        :param entity_uuid: The UUID of the entity to delete.
        :type entity_uuid: UUID4
        :param entity_data: The data used to mark the entity as deleted.
        :type entity_data: EntitiesDel
        :param db: The database session.
        :type db: AsyncSession
        :return: The deleted entity data.
        :rtype: EntitiesDelRes
        :raises EntityNotExist: If the entity does not exist.
        """
        statement: update = self._statements.update_entity(
            entity_uuid=entity_uuid, entity_data=entity_data
        )
        entity: EntitiesDelRes = await self._db_ops.return_one_row(
            service=cnst.ENTITIES_DEL_SERV, statement=statement, db=db
        )
        return record_not_exist(instance=entity, exception=EntityNotExist)
