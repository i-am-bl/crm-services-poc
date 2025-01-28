from typing import List

from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ..constants import constants as cnst
from ..database.operations import Operations
from ..exceptions import OrderItemNotExist
from ..models.order_items import OrderItems
from ..schemas.order_items import (
    OrderItemsCreate,
    OrderItemsDel,
    OrderItemsDelRes,
    OrderItemsPgRes,
    OrderItemsRes,
    OrderItemsUpdate,
)
from ..statements.order_items import OrderItemsStms
from ..utilities import pagination
from ..utilities.utilities import DataUtils as di


class ReadSrvc:
    def __init__(self, statements: OrderItemsStms, db_operations: Operations) -> None:
        self._statements: OrderItemsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> OrderItemsStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def get_order_item(
        self,
        order_uuid: UUID4,
        order_item_uuid: UUID4,
        db: AsyncSession,
    ) -> OrderItemsRes:
        statement = self._statements.get_order_item(
            order_uuid=order_uuid, order_item_uuid=order_item_uuid
        )
        order_item: OrderItemsRes = await self._db_ops.return_one_row(
            cnst.ORDERS_ITEMS_READ_SERVICE, statement=statement, db=db
        )
        return di.record_not_exist(instance=order_item, exception=OrderItemNotExist)

    async def get_order_items(
        self,
        order_uuid: UUID4,
        limit: int,
        offset: int,
        db: AsyncSession,
    ) -> List[OrderItemsRes]:
        statement = self._statements.get_order_items(
            order_uuid=order_uuid, limit=limit, offset=offset
        )
        order_items: List[OrderItemsRes] = await self._db_ops.return_all_rows(
            service=cnst.ORDERS_ITEMS_READ_SERVICE, statement=statement, db=db
        )
        return di.record_not_exist(instance=order_items, exception=OrderItemNotExist)

    async def get_order_items_ct(
        self,
        order_uuid: UUID4,
        db: AsyncSession,
    ) -> int:
        statement = self._statements.get_order_item_ct(order_uuid=order_uuid)
        return await self._db_ops.return_count(
            service=cnst.ORDERS_ITEMS_READ_SERVICE, statement=statement, db=db
        )

    async def paginated_order_items(
        self, order_uuid: UUID4, page: int, limit: int, db: AsyncSession
    ) -> OrderItemsPgRes:
        total_count = await self.get_order_items_ct(order_uuid=order_uuid, db=db)
        offset = pagination.page_offset(page=page, limit=limit)
        has_more = pagination.has_more_items(
            total_count=total_count, page=page, limit=limit
        )
        order_items = await self.get_order_items(
            order_uuid=order_uuid, offset=offset, limit=limit, db=db
        )
        return OrderItemsPgRes(
            total=total_count,
            page=page,
            limit=limit,
            has_more=has_more,
            order_items=order_items,
        )


class CreateSrvc:
    def __init__(
        self, statements: OrderItemsStms, db_operations: Operations, model: OrderItems
    ) -> None:
        self._statements: OrderItemsStms = statements
        self._db_ops: Operations = db_operations
        self._model: OrderItems = model

    @property
    def statements(self) -> OrderItemsStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    @property
    def model(self) -> OrderItems:
        return self._model

    async def create_order_item(
        self,
        order_uuid: UUID4,
        order_item_data: OrderItemsCreate,
        db: AsyncSession,
    ) -> OrderItemsRes:
        # TODO: unsused param
        order_items = self._model
        order_item: OrderItemsRes = await self._db_ops.add_instances(
            service=cnst.ORDERS_ITEMS_CREATE_SERVICE,
            model=order_items,
            data=order_item_data,
            db=db,
        )
        return di.record_not_exist(instance=order_item, exception=OrderItemNotExist)


class UpdateSrvc:
    def __init__(self, statements: OrderItemsStms, db_operations: Operations) -> None:
        self._statements: OrderItemsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> OrderItemsStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def update_order_item(
        self,
        order_uuid: UUID4,
        order_item_uuid: UUID4,
        order_item_data: OrderItemsUpdate,
        db: AsyncSession,
    ) -> OrderItemsRes:
        statement = self._statements.update_order_item(
            order_uuid=order_uuid,
            order_item_uuid=order_item_uuid,
            order_item_data=order_item_data,
        )
        order_item: OrderItemsRes = await self._db_ops.return_one_row(
            service=cnst.ORDERS_ITEMS_UPDATE_SERVICE, statement=statement, db=db
        )
        return di.record_not_exist(instance=order_item, exception=OrderItemNotExist)


class DelSrvc:
    def __init__(self, statements: OrderItemsStms, db_operations: Operations) -> None:
        self._statements: OrderItemsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> OrderItemsStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def soft_del_order_item(
        self,
        order_uuid: UUID4,
        order_item_uuid: UUID4,
        order_item_data: OrderItemsDel,
        db: AsyncSession,
    ) -> OrderItemsDelRes:
        statement = self._statements.update_order_item(
            order_uuid=order_uuid,
            order_item_uuid=order_item_uuid,
            order_item_data=order_item_data,
        )
        order_item: OrderItemsDelRes = await self._db_ops.return_one_row(
            service=cnst.ORDERS_ITEMS_DEL_SERVICE, statement=statement, db=db
        )
        return di.record_not_exist(instance=order_item, exception=OrderItemNotExist)
