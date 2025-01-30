from pydantic import UUID4
from sqlalchemy import Select, Update, and_, func, update, values

from ..models.individuals import Individuals
from ..utilities.data import set_empty_strs_null


class IndividualsStms:
    """
    A class responsible for constructing SQLAlchemy queries and statements for managing individual entities.

    ivars:
    ivar: _model: Individuals: An instance of the Individuals model.
    """

    def __init__(self, model: Individuals) -> None:
        """
        Initializes the IndividualsStms class.

        :param model: Individuals: An instance of the Individuals model.
        :return: None
        """
        self._model = model

    @property
    def model(self) -> Individuals:
        """
        Returns the Individuals model.

        :return: Individuals: The Individuals model instance.
        """
        return self._model

    def get_individual(self, entity_uuid: UUID4) -> Select:
        """
        Selects an individual by entity UUID.

        :param entity_uuid: UUID4: The UUID of the entity.
        :return: Select: A Select statement for the individual.
        """
        individuals = self._model
        return Select(individuals).where(
            and_(
                individuals.entity_uuid == entity_uuid,
                individuals.sys_deleted_at == None,
            )
        )

    def get_individuals(self, offset: int, limit: int) -> Select:
        """
        Selects individuals with pagination.

        :param offset: int: The number of records to skip.
        :param limit: int: The number of records to return.
        :return: Select: A Select statement for the individuals.
        """
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
        """
        Selects the count of all individuals.

        :return: Select: A Select statement for the individuals count.
        """
        individuals = self._model
        return (
            Select(func.count())
            .select_from(individuals)
            .where(
                individuals.sys_deleted_at == None,
            )
        )

    def update_individual(self, entity_uuid: UUID4, individual_data: object) -> Update:
        """
        Updates an individual by entity UUID.

        :param entity_uuid: UUID4: The UUID of the entity.
        :param individual_data: object: The data to update the individual with.
        :return: Update: An Update statement for the individual.
        """
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
