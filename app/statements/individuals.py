from pydantic import UUID4
from sqlalchemy import Select, and_, func, update, values

from ..models.individuals import Individuals
from ..utilities.data import set_empty_strs_null


class IndividualsStms:
    def __init__(self, model: Individuals) -> None:
        self._model = model

    @property
    def model(self) -> Individuals:
        return self._model

    def get_individual(self, entity_uuid: UUID4) -> Select:
        individuals = self._model
        return Select(individuals).where(
            and_(
                individuals.entity_uuid == entity_uuid,
                individuals.sys_deleted_at == None,
            )
        )

    def get_individuals(self, offset: int, limit: int) -> Select:
        individuals = self._model
        return (
            Select(individuals)
            .where(
                individuals.sys_deleted_at == None,
            )
            .offset(offset=offset)
            .limit(limit=limit)
        )

    def get_individuals_ct(self) -> Select:
        individuals = self._model
        return (
            Select(func.count())
            .select_from(individuals)
            .where(
                individuals.sys_deleted_at == None,
            )
        )

    def update_individual(self, entity_uuid: UUID4, individual_data: object) -> update:
        individuals = self._model
        return (
            update(individuals)
            .where(
                and_(
                    individuals.entity_uuid == entity_uuid,
                    individuals.sys_deleted_at == None,
                )
            )
            .values(set_empty_strs_null(individual_data))
        ).returning(individuals)
