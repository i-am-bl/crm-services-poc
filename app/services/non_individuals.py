from typing import List
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ..constants import constants as cnst
from ..database.operations import Operations
from ..exceptions import NonIndividualExists, NonIndividualNotExist
from ..models.non_individuals import NonIndividuals
from ..schemas.non_individuals import (
    NonIndividualsCreate,
    NonIndividualsDel,
    NonIndividualsRes,
    NonIndividualsDelRes,
    NonIndividualsUpdate,
)
from ..statements.non_individuals import NonInvdividualsStms
from ..utilities.data import record_not_exist, record_exists


class ReadSrvc:
    def __init__(
        self, statements: NonInvdividualsStms, db_operations: Operations
    ) -> None:
        self._statements: NonInvdividualsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> NonInvdividualsStms:
        return self._statements

    @property
    def db_opoerations(self) -> Operations:
        return self._db_ops

    async def get_non_individual(
        self,
        entity_uuid: UUID4,
        db: AsyncSession,
    ) -> NonIndividualsRes:
        statement = self._statements.get_non_individual(entity_uuid=entity_uuid)
        non_individual: NonIndividualsRes = await self._db_ops.return_one_row(
            service=cnst.NON_INDIVIDUALS_READ_SERV, statement=statement, db=db
        )
        return record_not_exist(
            instance=non_individual, exception=NonIndividualNotExist
        )

    async def get_non_individuals(
        self, offset: int, limit: int, db: AsyncSession
    ) -> List[NonIndividualsRes]:
        statement = self._statements.sel_non_indivs(offset=offset, limit=limit)
        non_individual: List[NonIndividualsRes] = await self._db_ops.return_all_rows(
            service=cnst.NON_INDIVIDUALS_READ_SERV, statement=statement, db=db
        )
        return record_not_exist(
            instance=non_individual, exception=NonIndividualNotExist
        )

    async def get_non_individuals_ct(
        self, offset: int, limit: int, db: AsyncSession
    ) -> int:
        statement = self._statements.get_non_individuals_count()
        return await self._db_ops.return_count(
            service=cnst.NON_INDIVIDUALS_READ_SERV, statement=statement, db=db
        )


class CreateSrvc:
    def __init__(
        self,
        statements: NonInvdividualsStms,
        db_operations: Operations,
        model: NonIndividuals,
    ) -> None:
        self._statements: NonInvdividualsStms = statements
        self._db_ops: Operations = db_operations
        self._model: NonIndividuals = model

    @property
    def statements(self) -> NonInvdividualsStms:
        return self._statements

    @property
    def db_opoerations(self) -> Operations:
        return self._db_ops

    @property
    def model(self) -> NonIndividuals:
        return self._model

    async def create_non_individual(
        self,
        entity_uuid: UUID4,
        non_individual_data: NonIndividualsCreate,
        db: AsyncSession,
    ) -> NonIndividualsRes:
        non_individuals = self._model
        statement = self._statements.sel_by_entity_ni_name(
            entity_uuid=entity_uuid, name=non_individual_data.name
        )
        non_individual_exists: NonIndividualsRes = await self._db_ops.return_one_row(
            service=cnst.NON_INDIVIDUALS_CREATE_SERV, statement=statement, db=db
        )
        record_exists(instance=non_individual_exists, exception=NonIndividualExists)
        non_individual: NonIndividualsRes = await self._db_ops.add_instance(
            service=cnst.NON_INDIVIDUALS_CREATE_SERV,
            model=non_individuals,
            data=non_individual_data,
            db=db,
        )
        return record_not_exist(
            instance=non_individual, exception=NonIndividualNotExist
        )


class UpdateSrvc:
    def __init__(
        self, statements: NonInvdividualsStms, db_operations: Operations
    ) -> None:
        self._statements: NonInvdividualsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> NonInvdividualsStms:
        return self._statements

    @property
    def db_opoerations(self) -> Operations:
        return self._db_ops

    async def update_non_individual(
        self,
        entity_uuid: UUID4,
        non_individual_data: NonIndividualsUpdate,
        db: AsyncSession,
    ) -> NonIndividualsRes:
        statement = self._statements.update_non_individual(
            entity_uuid=entity_uuid,
            non_individual_data=non_individual_data,
        )
        non_individual: NonIndividualsRes = await self._db_ops.return_one_row(
            service=cnst.NON_INDIVIDUALS_UPDATE_SERV, statement=statement, db=db
        )
        return record_not_exist(
            instance=non_individual, exception=NonIndividualNotExist
        )


class DelSrvc:
    def __init__(
        self, statements: NonInvdividualsStms, db_operations: Operations
    ) -> None:
        self._statements: NonInvdividualsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> NonInvdividualsStms:
        return self._statements

    @property
    def db_opoerations(self) -> Operations:
        return self._db_ops

    async def soft_del_non_individual(
        self,
        entity_uuid: UUID4,
        non_individual_uuid: UUID4,
        non_individual_data: NonIndividualsDel,
        db: AsyncSession,
    ) -> NonIndividualsDelRes:
        statement = self._statements.update_non_individual(
            entity_uuid=entity_uuid,
            non_individual_uuid=non_individual_uuid,
            non_individual_data=non_individual_data,
        )
        non_individual: NonIndividualsDelRes = await self._db_ops.return_one_row(
            service=cnst.NON_INDIVIDUALS_UPDATE_SERV, statement=statement, db=db
        )
        return record_not_exist(
            instance=non_individual, exception=NonIndividualNotExist
        )
