from typing import Literal, List

from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ..constants import constants as cnst
from ..database.operations import Operations
from ..exceptions import AddressExists, AddressNotExist
from ..models.addresses import Addresses
from ..schemas.addresses import (
    AddressesCreate,
    AddressesDel,
    AddressesDelRes,
    AddressesPgRes,
    AddressesRes,
    AddressesUpdate,
)
from ..statements.addresses import AddressesStms
from ..utilities import pagination
from ..utilities.utilities import DataUtils as di


class ReadSrvc:
    def __init__(self, statements: AddressesStms, db_operations: Operations) -> None:
        self._statements: AddressesStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> Addresses:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def get_address(
        self,
        parent_uuid: UUID4,
        parent_table: Literal["entities", "accounts"],
        address_uuid: UUID4,
        db: AsyncSession,
    ) -> AddressesRes:
        statement = self._statements.get_address(
            parent_uuid=parent_uuid,
            address_uuid=address_uuid,
            parent_table=parent_table,
        )
        address: AddressesRes = await self._db_ops.return_one_row(
            service=cnst.ADDRESSES_READ_SERVICE, statement=statement, db=db
        )
        return di.record_not_exist(instance=address, exception=AddressNotExist)

    async def get_addresses(
        self,
        parent_uuid: UUID4,
        parent_table: Literal["entities", "accounts"],
        limit: int,
        offset: int,
        db: AsyncSession,
    ) -> List[AddressesRes]:
        statement = self._statements.get_address_by_entity(
            parent_uuid=parent_uuid,
            parent_table=parent_table,
            offset=offset,
            limit=limit,
        )
        addresses: List[AddressesRes] = await self._db_ops.return_all_rows(
            service=cnst.ADDRESSES_READ_SERVICE, statement=statement, db=db
        )
        return di.record_not_exist(instance=addresses, exception=AddressNotExist)

    async def get_addresses_ct(
        self,
        parent_uuid: UUID4,
        parent_table: Literal["entities", "accounts"],
        db: AsyncSession,
    ) -> int:
        statement = self._statements.get_addresses_ct(
            parent_uuid=parent_uuid, parent_table=parent_table
        )
        return await self._db_ops.return_count(
            service=cnst.ADDRESSES_READ_SERVICE, statement=statement, db=db
        )

    async def paginated_addresses(
        self,
        parent_uuid: UUID4,
        parent_table: Literal["entities", "accounts"],
        limit: int,
        page: int,
        db: AsyncSession,
    ) -> AddressesPgRes:
        total_count = await self.get_addresses_ct(
            parent_uuid=parent_uuid, parent_table=parent_table, db=db
        )
        offset = pagination.page_offset(page=page, limit=limit)
        has_more = pagination.has_more_items(
            total_count=total_count, page=page, limit=limit
        )
        addresses = await self.get_addresses(
            parent_uuid=parent_uuid,
            parent_table=parent_table,
            offset=offset,
            limit=limit,
            db=db,
        )
        return AddressesPgRes(
            total=total_count,
            page=page,
            limit=limit,
            has_more=has_more,
            addresses=addresses,
        )


class CreateSrvc:
    def __init__(
        self, statements: AddressesStms, db_operations: Operations, model: Addresses
    ) -> None:
        self._statements: AddressesStms = statements
        self._db_ops: Operations = db_operations
        self._model: Addresses = model

    @property
    def statements(self) -> Addresses:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    @property
    def model(self) -> Addresses:
        return self._model

    async def create_address(
        self,
        parent_uuid: UUID4,
        address_data: AddressesCreate,
        db: AsyncSession,
    ) -> AddressesRes:
        addresses = self._model
        statement = self._statements.get_address_by_address(
            parent_uuid=parent_uuid,
            address_line1=address_data.address_line1,
            address_line2=address_data.address_line2,
            city=address_data.city,
        )
        address_exists: AddressesRes = await self._db_ops.return_one_row(
            service=cnst.ADDRESSES_CREATE_SERVICE, statement=statement, db=db
        )
        if not di.record_exists(instance=address_exists, exception=AddressExists):
            address: AddressesRes = await self._db_ops.add_instance(
                service=cnst.ADDRESSES_CREATE_SERVICE,
                model=addresses,
                data=address_data,
                db=db,
            )
            return di.record_not_exist(instance=address, exception=AddressNotExist)


class UpdateSrvc:
    def __init__(self, statements: AddressesStms, db_operations: Operations) -> None:
        self._statements: AddressesStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> Addresses:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def update_address(
        self,
        parent_uuid: UUID4,
        parent_table: Literal["entities", "accounts"],
        address_uuid: UUID4,
        address_data: AddressesUpdate,
        db: AsyncSession,
    ) -> AddressesRes:
        statement = self._statements.update_address(
            parent_uuid=parent_uuid,
            parent_table=parent_table,
            addresses_uuid=address_uuid,
            address_data=address_data,
        )
        address: AddressesRes = await self._db_ops.return_one_row(
            service=cnst.ADDRESSES_UPDATE_SERVICE, statement=statement, db=db
        )
        return di.record_not_exist(instance=address, exception=AddressNotExist)


class DelSrvc:
    def __init__(self, statements: AddressesStms, db_operations: Operations) -> None:
        self._statements: AddressesStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> Addresses:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def soft_del_address(
        self,
        parent_uuid: UUID4,
        parent_table: Literal["entities", "accounts"],
        address_uuid: UUID4,
        address_data: AddressesDel,
        db: AsyncSession,
    ) -> AddressesDelRes:
        statement = self._statements.update_address(
            parent_uuid=parent_uuid,
            parent_table=parent_table,
            addresses_uuid=address_uuid,
            address_data=address_data,
        )
        address: AddressesDelRes = await self._db_ops.return_one_row(
            service=cnst.ADDRESSES_DEL_SERVICE, statement=statement, db=db
        )
        return di.record_not_exist(instance=address, exception=AddressNotExist)
