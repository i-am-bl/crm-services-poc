from pydantic import UUID4
from sqlalchemy import Select, Update, func, update, and_

from ..models.order_items import OrderItems
from ..utilities.utilities import DataUtils as di


class OrderItemsStms:
    def __init__(self, model: OrderItems) -> None:
        self._model: OrderItems = model

    @property
    def model(self) -> OrderItems:
        return self._model

    def get_order_item(self, order_uuid: UUID4, order_item_uuid: UUID4) -> Select:
        order_items = self._model
        return Select(order_items).where(
            and_(
                order_items.order_uuid == order_uuid,
                order_items.uuid == order_item_uuid,
                order_items.sys_deleted_at == None,
            )
        )

    def get_order_items(self, order_uuid: UUID4, limit: int, offset: int) -> Select:
        order_items = self._model
        return (
            Select(order_items)
            .where(
                and_(
                    order_items.order_uuid == order_uuid,
                    order_items.sys_deleted_at == None,
                )
            )
            .offset(offset=offset)
            .limit(limit=limit)
        )

    def get_order_item_ct(self, order_uuid: UUID4) -> Select:
        order_items = self._model
        return (
            Select(func.count())
            .select_from(order_items)
            .where(
                and_(
                    order_items.order_uuid == order_uuid,
                    order_items.sys_deleted_at == None,
                )
            )
        )

    def update_order_item(
        self, order_uuid: UUID4, order_item_uuid: UUID4, order_item_data: object
    ) -> Update:
        order_items = self._model
        return (
            update(order_items)
            .where(
                and_(
                    order_items.order_uuid == order_uuid,
                    order_items.uuid == order_item_uuid,
                    order_items.sys_deleted_at == None,
                )
            )
            .values(di.set_empty_strs_null(values=order_item_data))
            .returning(order_items)
        )
