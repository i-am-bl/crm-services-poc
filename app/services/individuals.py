from typing import List
from pydantic import UUID4
from sqlalchemy import Select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..constants import constants as cnst
from ..database.operations import Operations
from ..exceptions import IndividualExists, IndividualNotExist
from ..models.individuals import Individuals
from ..schemas.individuals import (
    IndividualsCreate,
    IndividualsUpdate,
    IndividualsRes,
    IndividualsDel,
    IndividualsDelRes,
)
from ..statements.individuals import IndividualsStms
from ..utilities.utilities import DataUtils as di


class ReadSrvc:
    def __init__(self, statements: IndividualsStms, db_operations: Operations) -> None:
        self._statements: IndividualsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> IndividualsStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def get_individual(
        self,
        entity_uuid: UUID4,
        db: AsyncSession,
    ) -> IndividualsRes:
        statement: Select = self._statements.get_individual(entity_uuid=entity_uuid)
        individual: IndividualsRes = await self._db_ops.return_one_row(
            service=cnst.INDIVIDUALS_READ_SERV, statement=statement, db=db
        )
        return di.record_not_exist(instance=individual, exception=IndividualNotExist)

    async def get_individuals(
        self,
        offset: int,
        limit: int,
        db: AsyncSession,
    ) -> List[IndividualsRes]:
        statement: Select = self._statements.get_individuals(offset=offset, limit=limit)
        individual: List[IndividualsRes] = await self._db_ops.return_all_rows(
            service=cnst.INDIVIDUALS_READ_SERV, statement=statement, db=db
        )
        return di.record_not_exist(instance=individual, exception=IndividualNotExist)

    async def get_individuals_ct(
        self,
        db: AsyncSession,
    ) -> int:
        statement: Select = self._statements.get_individuals_ct()
        return await self._db_ops.return_count(
            service=cnst.INDIVIDUALS_READ_SERV, statement=statement, db=db
        )


class CreateSrvc:
    def __init__(
        self, statements: IndividualsStms, db_operations: Operations, model: Individuals
    ) -> None:
        self._statements: IndividualsStms = statements
        self._db_ops: Operations = db_operations
        self._model: Individuals = model

    @property
    def statements(self) -> IndividualsStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    @property
    def model(self) -> Individuals:
        return self._model

    async def create_individual(
        self,
        entity_uuid: UUID4,
        individual_data: IndividualsCreate,
        db: AsyncSession,
    ) -> IndividualsRes:
        statement: Select = self._statements.get_individual(entity_uuid=entity_uuid)
        individuals: Individuals = self._model
        individual_exists: IndividualsRes = await self._db_ops.return_one_row(
            service=cnst.INDIVIDUALS_CREATE_SERV, statement=statement, db=db
        )
        di.record_exists(instance=individual_exists, exception=IndividualExists)
        individual: IndividualsRes = await self._db_ops.add_instance(
            service=cnst.INDIVIDUALS_CREATE_SERV,
            model=individuals,
            data=individual_data,
            db=db,
        )
        return di.record_not_exist(instance=individual, exception=IndividualNotExist)


class UpdateSrvc:
    def __init__(self, statements: IndividualsStms, db_operations: Operations) -> None:
        self._statements: IndividualsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> IndividualsStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def update_individual(
        self,
        entity_uuid: UUID4,
        individual_data: IndividualsUpdate,
        db: AsyncSession,
    ) -> IndividualsRes:
        statement: update = self._statements.update_individual(
            entity_uuid=entity_uuid,
            individual_data=individual_data,
        )
        individual: IndividualsRes = await self._db_ops.return_one_row(
            service=cnst.INDIVIDUALS_UPDATE_SERV, statement=statement, db=db
        )
        return di.record_not_exist(instance=individual, exception=IndividualNotExist)


class DelSrvc:
    def __init__(self, statements: IndividualsStms, db_operations: Operations) -> None:
        self._statements: IndividualsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> IndividualsStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def soft_del_individual(
        self,
        entity_uuid: UUID4,
        individual_data: IndividualsDel,
        db: AsyncSession,
    ):
        statement: update = self._statements.update_individual(
            entity_uuid=entity_uuid,
            individual_data=individual_data,
        )
        individual: IndividualsDelRes = await self._db_ops.return_one_row(
            service=cnst.INDIVIDUALS_DEL_SERV, statement=statement, db=db
        )
        return di.record_not_exist(instance=individual, exception=IndividualNotExist)
