from pydantic import UUID4
from sqlalchemy import Select, Update, func, update, and_

from ..models.order_items import OrderItems
from ..utilities.data import set_empty_strs_null


class OrderItemsStms:
    """
    A class responsible for constructing SQLAlchemy queries and statements for managing order item records.

    ivars:
    ivar: _model: OrderItems: An instance of the OrderItems model.
    """

    def __init__(self, model: OrderItems) -> None:
        """
        Initializes the OrderItemsStms class.

        :param model: OrderItems: An instance of the OrderItems model.
        :return: None
        """
        self._model: OrderItems = model

    @property
    def model(self) -> OrderItems:
        """
        Returns the OrderItems model.

        :return: OrderItems: The OrderItems model instance.
        """
        return self._model

    def get_order_item(self, order_uuid: UUID4, order_item_uuid: UUID4) -> Select:
        """
        Selects a specific order item by its order UUID and order item UUID.

        :param order_uuid: UUID4: The UUID of the order.
        :param order_item_uuid: UUID4: The UUID of the order item.
        :return: Select: A Select statement for the specific order item.
        """
        order_items = self._model
        return Select(order_items).where(
            and_(
                order_items.order_uuid == order_uuid,
                order_items.uuid == order_item_uuid,
                order_items.sys_deleted_at == None,
            )
        )

    def get_order_items(self, order_uuid: UUID4, limit: int, offset: int) -> Select:
        """
        Selects order items for a given order UUID with pagination.

        :param order_uuid: UUID4: The UUID of the order.
        :param limit: int: The maximum number of records to return.
        :param offset: int: The number of records to skip.
        :return: Select: A Select statement for order items filtered by order UUID with pagination.
        """
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
        """
        Selects the count of order items for a given order UUID.

        :param order_uuid: UUID4: The UUID of the order.
        :return: Select: A Select statement for the count of order items for the given order UUID.
        """
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
        """
        Updates a specific order item by its order UUID and order item UUID.

        :param order_uuid: UUID4: The UUID of the order.
        :param order_item_uuid: UUID4: The UUID of the order item.
        :param order_item_data: object: The data to update the order item with.
        :return: Update: An Update statement for the order item.
        """
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
            .values(set_empty_strs_null(values=order_item_data))
            .returning(order_items)
        )
