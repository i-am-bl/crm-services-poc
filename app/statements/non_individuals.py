from pydantic import UUID4
from sqlalchemy import Select, and_, func, update, values

from ..models.non_individuals import NonIndividuals
from ..utilities.data import set_empty_strs_null


class NonInvdividualsStms:
    def __init__(self, model: NonIndividuals):
        self._model: NonIndividuals = model

    @property
    def model(self) -> NonIndividuals:
        return self._model

    def get_non_individual(self, entity_uuid: UUID4) -> Select:
        non_individuals = self._model
        return Select(non_individuals).where(
            and_(
                non_individuals.entity_uuid == entity_uuid,
                non_individuals.sys_deleted_at == None,
            )
        )

    def sel_non_indivs(self, offset: int, limit: int) -> Select:
        non_individuals = self._model
        return (
            Select(non_individuals)
            .where(
                non_individuals.sys_deleted_at == None,
            )
            .offset(offset=offset)
            .limit(limit=limit)
        )

    def get_non_individuals_count(
        self,
    ) -> Select:
        non_individuals = self._model
        return (
            Select(func.count())
            .select_from(non_individuals)
            .where(
                non_individuals.sys_deleted_at == None,
            )
        )

    def get_non_individual_by_name(self, entity_uuid: UUID4, name: str) -> Select:
        non_individuals = self._model
        return Select(non_individuals).where(
            and_(
                non_individuals.entity_uuid == entity_uuid,
                non_individuals.name == name,
                non_individuals.sys_deleted_at == None,
            )
        )

    def update_non_individual(
        self, entity_uuid: UUID4, non_individual_data: object
    ) -> update:
        non_individuals = self._model
        return (
            update(non_individuals)
            .where(
                and_(
                    non_individuals.entity_uuid == entity_uuid,
                    non_individuals.sys_deleted_at == None,
                )
            )
            .values(set_empty_strs_null(non_individual_data))
            .returning(non_individuals)
        )
