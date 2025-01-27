from typing import List
from pydantic import UUID4
from sqlalchemy import Select, and_, func, update

from ..database.operations import Operations
from ..models.entities import Entities
from ..models.individuals import Individuals
from ..models.non_individuals import NonIndividuals
from ..utilities.utilities import DataUtils as di


class EntitiesStms:
    def __init__(self, entities: Entities, individuals, non_individuals) -> None:
        self._entities: Entities = entities
        self._individuals = individuals
        self._non_individuals = non_individuals

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    def get_entity(self, entity_uuid: UUID4):
        entities = self._entities
        return Select(entities).where(
            and_(entities.uuid == entity_uuid, entities.sys_deleted_at == None)
        )

    def get_entities(self, limit: int, offset: int):
        entities = self._entities
        return (
            Select(entities)
            .where(entities.sys_deleted_at == None)
            .offset(offset=offset)
            .limit(limit=limit)
        )

    def get_entities_by_uuids(self, entity_uuids: List[UUID4]) -> Select:
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

    def get_entity_ct(
        self,
    ) -> int:
        entities = self._entities
        return (
            Select(func.count())
            .select_from(entities)
            .where(entities.sys_deleted_at == None)
        )

    def update_entity(self, entity_uuid: UUID4, entity_data: object) -> update:
        entities = self._entities
        return (
            update(entities)
            .where(and_(entities.uuid == entity_uuid, entities.sys_deleted_at == None))
            .values(di.set_empty_strs_null(entity_data))
            .returning(entities)
        )
