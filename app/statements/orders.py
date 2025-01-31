from pydantic import UUID4
from sqlalchemy import Select, Update, and_, func, update, values

from ..models.orders import Orders
from ..utilities.data import set_empty_strs_null


class OrdersStms:
    """
    A class responsible for constructing SQLAlchemy queries and statements for managing order records.

    ivars:
    ivar: _model: Orders: An instance of the Orders model.
    """

    def __init__(self, model: Orders) -> None:
        """
        Initializes the OrdersStms class.

        :param model: Orders: An instance of the Orders model.
        :return: None
        """
        self._model: Orders = model

    def get_order(self, order_uuid: UUID4) -> Select:
        """
        Selects a specific order by its order UUID.

        :param order_uuid: UUID4: The UUID of the order.
        :return: Select: A Select statement for the specific order.
        """
        orders = self._model
        return Select(orders).where(
            and_(
                orders.uuid == order_uuid,
                orders.sys_deleted_at == None,
            )
        )

    def get_orders(self, limit: int, offset: int) -> Select:
        """
        Selects orders with pagination support.

        :param limit: int: The maximum number of records to return.
        :param offset: int: The number of records to skip.
        :return: Select: A Select statement for orders with pagination.
        """
        orders = self._model
        return (
            Select(orders)
            .where(orders.sys_deleted_at == None)
            .offset(offset=offset)
            .limit(limit=limit)
        )

    def get_orders_ct(self) -> Select:
        """
        Selects the count of orders.

        :return: Select: A Select statement for the count of all orders.
        """
        orders = self._model
        return (
            Select(func.count())
            .select_from(orders)
            .where(orders.sys_deleted_at == None)
        )

    def update_order(self, order_uuid: UUID4, order_data: object) -> Update:
        """
        Updates a specific order by its order UUID.

        :param order_uuid: UUID4: The UUID of the order.
        :param order_data: object: The data to update the order with.
        :return: Update: An Update statement for the order.
        """
        orders = self._model
        return (
            update(orders)
            .where(and_(orders.uuid == order_uuid, orders.sys_deleted_at == None))
            .values(set_empty_strs_null(values=order_data))
            .returning(orders)
        )
