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


class EntitiesReadOrch:
    def __init__(
        self,
        entities_read_srvc: entities_srvcs.ReadSrvc,
        individuals_read_srvc: individuals_srvcs.ReadSrvc,
        non_individuals_read_srvc: non_individuals_srvcs.ReadSrvc,
    ):
        self._entities_read_srvc: entities_srvcs.ReadSrvc = entities_read_srvc
        self._individuals_read_srvc: individuals_srvcs.ReadSrvc = individuals_read_srvc
        self._non_individuals_read_srvc: non_individuals_srvcs.ReadSrvc = (
            non_individuals_read_srvc
        )

    @property
    def entities_read_srvc(self) -> entities_srvcs.ReadSrvc:
        return self._entities_read_srvc

    @property
    def individuals_read_srvc(self) -> individuals_srvcs.ReadSrvc:
        return self._individuals_read_srvc

    def non_individuals_read_srvc(self) -> non_individuals_srvcs.ReadSrvc:
        return self._non_individuals_read_srvc

    async def get_entity(self): ...
    async def get_individual(self): ...
    async def get_non_individual(self): ...


class EntitiesCreateOrch:
    def __init__(
        self,
        entities_create_srvc: entities_srvcs.CreateSrvc,
        individuals_create_srvc: individuals_srvcs.CreateSrvc,
        non_individuals_create_srvc: non_individuals_srvcs.CreateSrvc,
    ):
        self._entities_create_srvc: entities_srvcs.CreateSrvc = entities_create_srvc
        self._individuals_create_srvc: individuals_srvcs.CreateSrvc = (
            individuals_create_srvc
        )
        self._non_individuals_create_srvc: non_individuals_srvcs.CreateSrvc = (
            non_individuals_create_srvc
        )

    @property
    def entities_create_srvc(self) -> entities_srvcs.CreateSrvc:
        return self._entities_create_srvc

    @property
    def individuals_create_srvc(self) -> individuals_srvcs.CreateSrvc:
        return self._individuals_create_srvc

    @property
    def non_individuals_create_srvc(self) -> non_individuals_srvcs.CreateSrvc:
        return self._non_individuals_create_srvc

    async def create_entity(
        self,
        entity_data: IndividualsInitCreate | NonIndividualsInitCreate,
        db: AsyncSession,
        sys_user: SysUsers,
    ) -> IndividualsRes | NonIndividualsRes:

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
