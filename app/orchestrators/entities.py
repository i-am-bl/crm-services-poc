from sqlalchemy.ext.asyncio import AsyncSession

from ..models.sys_users import SysUsers
from ..schemas.entities import EntitiesCreate
from ..schemas.individuals import (
    Individuals as IndividualsInitCreate,
    IndividualsRes,
    IndividualsCreate,
)
from ..schemas.non_individuals import (
    NonIndividuals as NonIndividualsInitCreate,
    NonIndividualsRes,
    NonIndividualsCreate,
)
from ..services import entities as entities_srvcs
from ..services import individuals as individuals_srvcs
from ..services import non_individuals as non_individuals_srvcs


class EntitiesCreateOrch:
    """
    Orchestrates the creation of entities, individuals, and non-individuals
    by interacting with the respective create services.

    :param entities_create_srvc: Service responsible for creating entity data.
    :type entities_create_srvc: entities_srvcs.CreateSrvc
    :param individuals_create_srvc: Service responsible for creating individual data.
    :type individuals_create_srvc: individuals_srvcs.CreateSrvc
    :param non_individuals_create_srvc: Service responsible for creating non-individual data.
    :type non_individuals_create_srvc: non_individuals_srvcs.CreateSrvc

    :ivar entities_create_srvc: The entity creation service instance.
    :vartype entities_create_srvc: entities_srvcs.CreateSrvc
    :ivar individuals_create_srvc: The individual creation service instance.
    :vartype individuals_create_srvc: individuals_srvcs.CreateSrvc
    :ivar non_individuals_create_srvc: The non-individual creation service instance.
    :vartype non_individuals_create_srvc: non_individuals_srvcs.CreateSrvc
    """

    def __init__(
        self,
        entities_create_srvc: entities_srvcs.CreateSrvc,
        individuals_create_srvc: individuals_srvcs.CreateSrvc,
        non_individuals_create_srvc: non_individuals_srvcs.CreateSrvc,
    ):
        """
        Initializes the EntitiesCreateOrch instance with the provided entity, individual, and non-individual create services.

        :param entities_create_srvc: Service responsible for creating entity data.
        :type entities_create_srvc: entities_srvcs.CreateSrvc
        :param individuals_create_srvc: Service responsible for creating individual data.
        :type individuals_create_srvc: individuals_srvcs.CreateSrvc
        :param non_individuals_create_srvc: Service responsible for creating non-individual data.
        :type non_individuals_create_srvc: non_individuals_srvcs.CreateSrvc
        """
        self._entities_create_srvc: entities_srvcs.CreateSrvc = entities_create_srvc
        self._individuals_create_srvc: individuals_srvcs.CreateSrvc = (
            individuals_create_srvc
        )
        self._non_individuals_create_srvc: non_individuals_srvcs.CreateSrvc = (
            non_individuals_create_srvc
        )

    @property
    def entities_create_srvc(self) -> entities_srvcs.CreateSrvc:
        """
        Returns the entities creation service instance.

        :return: The entities creation service instance.
        :rtype: entities_srvcs.CreateSrvc
        """
        return self._entities_create_srvc

    @property
    def individuals_create_srvc(self) -> individuals_srvcs.CreateSrvc:
        """
        Returns the individuals creation service instance.

        :return: The individuals creation service instance.
        :rtype: individuals_srvcs.CreateSrvc
        """
        return self._individuals_create_srvc

    @property
    def non_individuals_create_srvc(self) -> non_individuals_srvcs.CreateSrvc:
        """
        Returns the non-individuals creation service instance.

        :return: The non-individuals creation service instance.
        :rtype: non_individuals_srvcs.CreateSrvc
        """
        return self._non_individuals_create_srvc

    async def create_entity(
        self,
        entity_data: IndividualsInitCreate | NonIndividualsInitCreate,
        db: AsyncSession,
        sys_user: SysUsers,
    ) -> IndividualsRes | NonIndividualsRes:
        """
        Creates an entity along with either an individual or non-individual based on the provided entity data.

        The method first determines the type of entity (individual or non-individual) and invokes the
        appropriate creation services for the entity, individual, or non-individual.

        :param entity_data: Data used for creating the entity (either individual or non-individual).
        :type entity_data: IndividualsInitCreate | NonIndividualsInitCreate
        :param db: The database session for performing queries.
        :type db: AsyncSession
        :param sys_user: The system user performing the creation action.
        :type sys_user: SysUsers

        :return: The created individual or non-individual data.
        :rtype: IndividualsRes | NonIndividualsRes
        """
        if isinstance(entity_data, IndividualsInitCreate):
            _entity_data = EntitiesCreate(
                type="individual", sys_created_by=sys_user.uuid
            )
            entity = await self._entities_create_srvc.create_entity(
                entity_data=_entity_data, db=db
            )
            individual_data = IndividualsCreate(
                *entity_data, entity_uuid=entity.uuid, sys_created_by=sys_user.uuid
            )
            return await self._individuals_create_srvc.create_individual(
                entity_uuid=entity.uuid, individual_data=individual_data, db=db
            )
        if isinstance(entity_data, NonIndividualsInitCreate):
            _entity_data = EntitiesCreate(
                type="non-individual", sys_created_by=sys_user.uuid
            )
            entity = await self._entities_create_srvc.create_entity(
                entity_data=_entity_data, db=db
            )
            non_individual_data = NonIndividualsCreate(
                *entity_data, entity_uuid=entity.uuid, sys_created_by=sys_user.uuid
            )
            return await self._non_individuals_create_srvc.create_non_individual(
                entity_uuid=entity.uuid, non_individual_data=non_individual_data, db=db
            )
