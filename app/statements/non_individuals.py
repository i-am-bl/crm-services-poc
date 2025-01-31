from pydantic import UUID4
from sqlalchemy import Select, and_, func, update, values, Update

from ..models.non_individuals import NonIndividuals
from ..utilities.data import set_empty_strs_null


class NonIndivididualsStms:
    """
    A class responsible for constructing SQLAlchemy queries and statements for managing non-individual (entity) records.

    ivars:
    ivar: _model: NonIndividuals: An instance of the NonIndividuals model.
    """

    def __init__(self, model: NonIndividuals) -> None:
        """
        Initializes the NonIndivididualsStms class.

        :param model: NonIndividuals: An instance of the NonIndividuals model.
        :return: None
        """
        self._model: NonIndividuals = model

    @property
    def model(self) -> NonIndividuals:
        """
        Returns the NonIndividuals model.

        :return: NonIndividuals: The NonIndividuals model instance.
        """
        return self._model

    def get_non_individual(self, entity_uuid: UUID4) -> Select:
        """
        Selects a specific non-individual entity by its entity UUID.

        :param entity_uuid: UUID4: The UUID of the entity.
        :return: Select: A Select statement for the specific non-individual entity.
        """
        non_individuals = self._model
        return Select(non_individuals).where(
            and_(
                non_individuals.entity_uuid == entity_uuid,
                non_individuals.sys_deleted_at == None,
            )
        )

    def sel_non_indivs(self, offset: int, limit: int) -> Select:
        """
        Selects non-individual entities with pagination.

        :param offset: int: The number of records to skip.
        :param limit: int: The maximum number of records to return.
        :return: Select: A Select statement for non-individual entities with pagination.
        """
        non_individuals = self._model
        return (
            Select(non_individuals)
            .where(non_individuals.sys_deleted_at == None)
            .offset(offset=offset)
            .limit(limit=limit)
        )

    def get_non_individuals_count(self) -> Select:
        """
        Selects the count of all non-individual entities.

        :return: Select: A Select statement for the count of non-individual entities.
        """
        non_individuals = self._model
        return (
            Select(func.count())
            .select_from(non_individuals)
            .where(non_individuals.sys_deleted_at == None)
        )

    def get_non_individual_by_name(self, entity_uuid: UUID4, name: str) -> Select:
        """
        Selects a non-individual entity by its entity UUID and name.

        :param entity_uuid: UUID4: The UUID of the entity.
        :param name: str: The name of the non-individual entity.
        :return: Select: A Select statement for the specific non-individual entity by name.
        """
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
    ) -> Update:
        """
        Updates a non-individual entity by its entity UUID.

        :param entity_uuid: UUID4: The UUID of the non-individual entity.
        :param non_individual_data: object: The data to update the non-individual entity with.
        :return: Update: An Update statement for the non-individual entity.
        """
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
