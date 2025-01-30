from pydantic import UUID4
from sqlalchemy import Select, Update, and_, func, update, values

from ..models.orders import Orders
from ..utilities.data import set_empty_strs_null


class OrdersStms:
    def __init__(self, model: Orders) -> None:
        self._model: Orders = model

    def get_order(self, order_uuid: UUID4) -> Select:
        orders = self._model
        return Select(orders).where(
            and_(
                orders.uuid == order_uuid,
                orders.sys_deleted_at == None,
            )
        )

    def get_orders(self, limit: int, offset: int) -> Select:
        orders = self._model
        return (
            Select(orders)
            .where(orders.sys_deleted_at == None)
            .offset(offset=offset)
            .limit(limit=limit)
        )

    def get_orders_ct(self) -> Select:
        orders = self._model
        return (
            Select(func.count())
            .select_from(orders)
            .where(orders.sys_deleted_at == None)
        )

    def update_order(self, order_uuid: UUID4, order_data: object) -> Update:
        orders = self._model
        return (
            update(orders)
            .where(and_(orders.uuid == order_uuid, orders.sys_deleted_at == None))
            .values(set_empty_strs_null(values=order_data))
            .returning(orders)
        )
