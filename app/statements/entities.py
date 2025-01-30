from typing import List
from pydantic import UUID4
from sqlalchemy import Select, and_, func, update

from ..database.operations import Operations
from ..models.entities import Entities
from ..utilities.data import set_empty_strs_null


class EntitiesStms:
    """
    A class responsible for constructing SQLAlchemy queries and statements for managing entities.

    ivars:
    ivar: _entities: Entities: An instance of the Entities model.
    ivar: _individuals: A model for individual entities.
    ivar: _non_individuals: A model for non-individual entities (e.g., companies).
    """

    def __init__(self, entities: Entities, individuals, non_individuals) -> None:
        """
        Initializes the EntitiesStms class.

        :param entities: Entities: An instance of the Entities model.
        :param individuals: A model for individual entities.
        :param non_individuals: A model for non-individual entities (e.g., companies).
        :return: None
        """
        self._entities = entities
        self._individuals = individuals
        self._non_individuals = non_individuals

    @property
    def db_operations(self) -> Operations:
        """
        Returns the database operations.

        :return: Operations: The database operations instance.
        """
        return self._db_ops

    def get_entity(self, entity_uuid: UUID4):
        """
        Selects an entity by its UUID.

        :param entity_uuid: UUID4: The UUID of the entity.
        :return: Select: A Select statement for the entity.
        """
        entities = self._entities
        return Select(entities).where(
            and_(entities.uuid == entity_uuid, entities.sys_deleted_at == None)
        )

    def get_entities(self, limit: int, offset: int):
        """
        Selects entities with pagination support.

        :param limit: int: The number of records to return.
        :param offset: int: The number of records to skip.
        :return: Select: A Select statement for the entities.
        """
        entities = self._entities
        return (
            Select(entities)
            .where(entities.sys_deleted_at == None)
            .offset(offset=offset)
            .limit(limit=limit)
        )

    def get_entities_by_uuids(self, entity_uuids: List[UUID4]) -> Select:
        """
        Selects entities by a list of UUIDs, joining individual and non-individual entity information.

        :param entity_uuids: List[UUID4]: A list of UUIDs of the entities to retrieve.
        :return: Select: A Select statement with joined individual and non-individual data.
        """
        entities = self._entities
        individuals = self._individuals
        non_individuals = self._non_individuals

        return (
            Select(
                entities.uuid.label("entity_uuid"),
                individuals.first_name,
                individuals.last_name,
                non_individuals.name.label("company_name"),
            )
            .join(
                isouter=True,
                target=individuals,
                onclause=entities.uuid == individuals.entity_uuid,
            )
            .join(
                isouter=True,
                target=non_individuals,
                onclause=entities.uuid == non_individuals.entity_uuid,
            )
            .where(
                and_(entities.uuid.in_(entity_uuids), entities.sys_deleted_at == None)
            )
        )

    def get_entity_ct(self) -> Select:
        """
        Selects the count of entities.

        :return: int: The count of entities.
        """
        entities = self._entities
        return (
            Select(func.count())
            .select_from(entities)
            .where(entities.sys_deleted_at == None)
        )

    def update_entity(self, entity_uuid: UUID4, entity_data: object) -> update:
        """
        Updates an entity by its UUID.

        :param entity_uuid: UUID4: The UUID of the entity to update.
        :param entity_data: object: The data to update the entity with.
        :return: update: An Update statement for the entity.
        """
        entities = self._entities
        return (
            update(entities)
            .where(and_(entities.uuid == entity_uuid, entities.sys_deleted_at == None))
            .values(set_empty_strs_null(entity_data))
            .returning(entities)
        )
