from typing import List

from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ..constants import constants as cnst
from ..database.operations import Operations
from ..exceptions import OrderNotExist
from ..models.orders import Orders
from ..schemas.orders import (
    OrdersCreate,
    OrdersRes,
    OrdersUpdate,
    OrdersDel,
    OrdersDelRes,
    OrdersPgRes,
)
from ..statements.orders import OrdersStms
from ..utilities import pagination
from ..utilities.utilities import DataUtils as di


class ReadSrvc:
    def __init__(self, statements: OrdersStms, db_operations: Operations) -> None:
        self._statements: OrdersStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> OrdersStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def get_order(self, order_uuid: UUID4, db: AsyncSession) -> OrdersRes:
        statement = self._statements.get_order(order_uuid=order_uuid)
        order: OrdersRes = await self._db_ops.return_one_row(
            service=cnst.ORDERS_READ_SERVICE, statement=statement, db=db
        )
        return di.record_not_exist(instance=order, exception=OrderNotExist)

    async def get_orders(
        self, limt: int, offset: int, db: AsyncSession
    ) -> List[OrdersRes]:
        statement = self._statements.get_orders(limit=limt, offset=offset)
        orders: List[OrdersRes] = await self._db_ops.return_all_rows(
            service=cnst.ORDERS_READ_SERVICE, statement=statement, db=db
        )
        return di.record_not_exist(instance=orders, exception=OrderNotExist)

    async def get_orders_ct(self, db: AsyncSession) -> int:
        statement = self._statements.get_orders_ct()
        return await self._db_ops.return_count(
            service=cnst.ORDERS_READ_SERVICE, statement=statement, db=db
        )

    async def paginated_orders(
        self, page: int, limit: int, db: AsyncSession
    ) -> OrdersPgRes:
        total_count = await self.get_orders_ct(db=db)
        offset = pagination.page_offset(page=page, limit=limit)
        has_more = pagination.has_more_items(
            total_count=total_count, page=page, limit=limit
        )
        orders = await self.get_orders(offset=offset, limt=limit, db=db)
        return OrdersPgRes(
            total=total_count, page=page, limit=limit, has_more=has_more, orders=orders
        )


class CreateSrvc:
    def __init__(self, db_operations: Operations, model: Orders) -> None:
        self._db_ops: Operations = db_operations
        self._model: Orders = model

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    @property
    def model(self) -> Orders:
        return self._model

    async def create_order(
        self, order_data: OrdersCreate, db: AsyncSession
    ) -> OrdersRes:
        orders = self._model
        order: OrdersRes = await self._db_ops.add_instance(
            service=cnst.ORDERS_CREATE_SERVICE, model=orders, data=order_data, db=db
        )
        return di.record_not_exist(instance=order, exception=OrderNotExist)


class UpdateSrvc:
    def __init__(self, statements: OrdersStms, db_operations: Operations) -> None:
        self._statements: OrdersStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> OrdersStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def update_order(
        self,
        order_uuid: UUID4,
        order_data: OrdersUpdate,
        db: AsyncSession,
    ) -> OrdersRes:
        # TODO: intllisense not working
        statement = self._statements.update_order(
            order_uuid=order_uuid, order_data=order_data
        )
        order: OrdersRes = await self._db_ops.return_one_row(
            service=cnst.ORDERS_UPDATE_SERVICE, statement=statement, db=db
        )
        return di.record_not_exist(instance=order, exception=OrderNotExist)


class DelSrvc:
    def __init__(self, statements: OrdersStms, db_operations: Operations) -> None:
        self._statements: OrdersStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> OrdersStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def soft_del_order(
        self,
        order_uuid: UUID4,
        order_data: OrdersDel,
        db: AsyncSession,
    ) -> OrdersDelRes:
        # TODO: intllisense not working
        statement = self._statements.update_order(
            order_uuid=order_uuid, order_data=order_data
        )
        order: OrdersDelRes = await self._db_ops.return_one_row(
            service=cnst.ORDERS_DEL_SERVICE, statement=statement, db=db
        )
        return di.record_not_exist(instance=order, exception=OrderNotExist)
