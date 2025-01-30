from typing import List
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ..constants import constants as cnst
from ..database.operations import Operations
from ..exceptions import NumberExists, NumbersNotExist
from ..models.numbers import Numbers
from ..schemas.numbers import (
    NumbersCreate,
    NumbersDel,
    NumbersDelRes,
    NumbersPgRes,
    NumbersRes,
    NumbersUpdate,
)
from ..statements.numbers import NumberStms
from ..utilities import pagination
from ..utilities.data import record_exists, record_not_exist


class ReadSrvc:
    def __init__(self, statements: NumberStms, db_operations: Operations) -> None:
        self._statements: NumberStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> NumberStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def get_number(
        self,
        entity_uuid: UUID4,
        number_uuid: UUID4,
        db: AsyncSession,
    ) -> NumbersRes:

        statement = self._statements.get_number(
            entity_uuid=entity_uuid,
            number_uuid=number_uuid,
        )
        number: NumbersRes = await self._db_ops.return_one_row(
            service=cnst.NUMBERS_READ_SERVICE, statement=statement, db=db
        )
        return record_not_exist(instance=number, exception=NumbersNotExist)

    async def get_numbers(
        self,
        entity_uuid: UUID4,
        limit: int,
        offset: int,
        db: AsyncSession,
    ) -> List[NumbersRes]:

        statement = self._statements.get_number_by_entity(
            entity_uuid=entity_uuid, limit=limit, offset=offset
        )
        numbers: List[NumbersRes] = await self._db_ops.return_all_rows(
            service=cnst.NUMBERS_READ_SERVICE, statement=statement, db=db
        )
        return record_not_exist(instance=numbers, exception=NumbersNotExist)

    async def get_numbers_ct(
        self,
        entity_uuid: UUID4,
        db: AsyncSession,
    ) -> int:

        statement = self._statements.get_number_by_entity_ct(entity_uuid=entity_uuid)
        return await self._db_ops.return_count(
            service=cnst.NUMBERS_READ_SERVICE, statement=statement, db=db
        )

    async def paginated_numbers(
        self, entity_uuid: UUID4, page: int, limit: int, db: AsyncSession
    ) -> NumbersPgRes:
        total_count = await self.get_numbers_ct(entity_uuid=entity_uuid, db=db)
        offset = pagination.page_offset(page=page, limit=limit)
        has_more = pagination.has_more_items(
            total_count=total_count, page=page, limit=limit
        )
        numbers = await self.get_numbers(
            entity_uuid=entity_uuid, offset=offset, limit=limit, db=db
        )
        return NumbersPgRes(
            total=total_count,
            page=page,
            limit=limit,
            has_more=has_more,
            numbers=numbers,
        )


class CreateSrvc:
    def __init__(
        self, statements: NumberStms, db_operations: Operations, model: Numbers
    ) -> None:
        self._statements: NumberStms = statements
        self._db_ops: Operations = db_operations
        self._model: Numbers = model

    @property
    def statements(self) -> NumberStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    @property
    def model(self) -> Numbers:
        return self._model

    async def create_number(
        self,
        entity_uuid: UUID4,
        number_data: NumbersCreate,
        db: AsyncSession,
    ) -> NumbersRes:
        numbers = self._model
        statement = self._statements.get_number_by_number(
            entity_uuid=entity_uuid,
            country_code=number_data.country_code,
            area_code=number_data.area_code,
            line_number=number_data.line_number,
            ext=number_data.extension,
        )
        number_exists: NumbersRes = await self._db_ops.return_one_row(
            service=cnst.NUMBERS_CREATE_SERVICE, statement=statement, db=db
        )
        record_exists(instance=number_exists, exception=NumberExists)
        number: NumbersRes = await self._db_ops.add_instance(
            service=cnst.NUMBERS_CREATE_SERVICE,
            model=numbers,
            data=number_data,
            db=db,
        )
        return record_not_exist(instance=number, exception=NumbersNotExist)


class UpdateSrvc:
    def __init__(self, statements: NumberStms, db_operations: Operations) -> None:
        self._statements: NumberStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> NumberStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def update_number(
        self,
        entity_uuid: UUID4,
        number_uuid: UUID4,
        number_data: NumbersUpdate,
        db: AsyncSession,
    ) -> NumbersRes:
        statement = self._statements.update_number(
            entity_uuid=entity_uuid,
            number_uuid=number_uuid,
            number_data=number_data,
        )
        number: NumbersRes = await self._db_ops.return_one_row(
            service=cnst.NUMBERS_UPDATE_SERVICE, statement=statement, db=db
        )
        return record_not_exist(instance=number, exception=NumbersNotExist)


class DelSrvc:
    def __init__(self, statements: NumberStms, db_operations: Operations) -> None:
        self._statements: NumberStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> NumberStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def soft_delete_number(
        self,
        entity_uuid: UUID4,
        number_uuid: UUID4,
        number_data: NumbersDel,
        db: AsyncSession,
    ) -> NumbersDelRes:
        statement = self._statements.update_number(
            entity_uuid=entity_uuid,
            number_uuid=number_uuid,
            number_data=number_data,
        )
        number: NumbersDelRes = await self._db_ops.return_one_row(
            service=cnst.NUMBERS_DEL_SERVICE,
            statement=statement,
            db=db,
        )
        return record_not_exist(instance=number, exception=NumbersNotExist)
