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
from ..utilities.data import record_not_exist


class ReadSrvc:
    """
    Service for reading orders from the database.

    This class provides methods for fetching single or multiple orders, counting orders,
    and handling paginated results of orders.

    :param statements: The SQL statements used for querying orders.
    :type statements: OrdersStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(self, statements: OrdersStms, db_operations: Operations) -> None:
        """
        Initializes the ReadSrvc class with the provided statements and database operations.

        :param statements: The SQL statements used for querying orders.
        :type statements: OrdersStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: OrdersStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> OrdersStms:
        """
        Returns the instance of OrdersStms.

        :returns: The SQL statements for reading orders.
        :rtype: OrdersStms
        """
        return self._statements

    @property
    def db_operations(self) -> Operations:
        """
        Returns the instance of Operations.

        :returns: The database operations handler.
        :rtype: Operations
        """
        return self._db_ops

    async def get_order(self, order_uuid: UUID4, db: AsyncSession) -> OrdersRes:
        """
        Retrieves a specific order by its UUID.

        :param order_uuid: The UUID of the order to retrieve.
        :type order_uuid: UUID4
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The retrieved order data.
        :rtype: OrdersRes
        :raises OrderNotExist: If the order does not exist in the database.
        """
        statement = self._statements.get_order(order_uuid=order_uuid)
        order: OrdersRes = await self._db_ops.return_one_row(
            service=cnst.ORDERS_READ_SERVICE, statement=statement, db=db
        )
        return record_not_exist(instance=order, exception=OrderNotExist)

    async def get_orders(
        self, limt: int, offset: int, db: AsyncSession
    ) -> List[OrdersRes]:
        """
        Retrieves a list of orders based on the provided limit and offset.

        :param limt: The maximum number of orders to retrieve.
        :type limt: int
        :param offset: The starting point from where to retrieve orders.
        :type offset: int
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: A list of orders matching the provided criteria.
        :rtype: List[OrdersRes]
        :raises OrderNotExist: If no orders are found.
        """
        statement = self._statements.get_orders(limit=limt, offset=offset)
        orders: List[OrdersRes] = await self._db_ops.return_all_rows(
            service=cnst.ORDERS_READ_SERVICE, statement=statement, db=db
        )
        return record_not_exist(instance=orders, exception=OrderNotExist)

    async def get_orders_ct(self, db: AsyncSession) -> int:
        """
        Retrieves the total count of orders.

        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The total number of orders in the database.
        :rtype: int
        """
        statement = self._statements.get_orders_ct()
        return await self._db_ops.return_count(
            service=cnst.ORDERS_READ_SERVICE, statement=statement, db=db
        )

    async def paginated_orders(
        self, page: int, limit: int, db: AsyncSession
    ) -> OrdersPgRes:
        """
        Retrieves orders in a paginated format, including total count and information
        about whether there are more items available for the next page.

        :param page: The current page number.
        :type page: int
        :param limit: The number of orders per page.
        :type limit: int
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: A paginated response containing the orders.
        :rtype: OrdersPgRes
        """
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
    """
    Service for creating orders in the database.

    This class provides a method to create a new order by taking in order data
    and interacting with the database to persist the order.

    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    :param model: The model class for orders that will be used for database interactions.
    :type model: Orders
    """

    def __init__(self, db_operations: Operations, model: Orders) -> None:
        """
        Initializes the CreateSrvc class with the provided database operations and model.

        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        :param model: The model class for orders.
        :type model: Orders
        """
        self._db_ops: Operations = db_operations
        self._model: Orders = model

    @property
    def db_operations(self) -> Operations:
        """
        Returns the instance of Operations.

        :returns: The database operations handler.
        :rtype: Operations
        """
        return self._db_ops

    @property
    def model(self) -> Orders:
        """
        Returns the instance of Orders model.

        :returns: The Orders model.
        :rtype: Orders
        """
        return self._model

    async def create_order(
        self, order_data: OrdersCreate, db: AsyncSession
    ) -> OrdersRes:
        """
        Creates a new order in the database using the provided order data.

        :param order_data: The data to create the new order.
        :type order_data: OrdersCreate
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The created order data.
        :rtype: OrdersRes
        :raises OrderNotExist: If the order could not be created or found.
        """
        orders = self._model
        order: OrdersRes = await self._db_ops.add_instance(
            service=cnst.ORDERS_CREATE_SERVICE, model=orders, data=order_data, db=db
        )
        return record_not_exist(instance=order, exception=OrderNotExist)


class UpdateSrvc:
    """
    Service for updating orders in the database.

    This class provides a method to update an existing order by taking in updated order data
    and interacting with the database to persist the changes.

    :param statements: The SQL statements used for order-related queries.
    :type statements: OrdersStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(self, statements: OrdersStms, db_operations: Operations) -> None:
        """
        Initializes the UpdateSrvc class with the provided SQL statements and database operations.

        :param statements: The SQL statements used for order-related queries.
        :type statements: OrdersStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: OrdersStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> OrdersStms:
        """
        Returns the instance of OrdersStms.

        :returns: The SQL statements handler for orders.
        :rtype: OrdersStms
        """
        return self._statements

    @property
    def db_operations(self) -> Operations:
        """
        Returns the instance of Operations.

        :returns: The database operations handler.
        :rtype: Operations
        """
        return self._db_ops

    async def update_order(
        self,
        order_uuid: UUID4,
        order_data: OrdersUpdate,
        db: AsyncSession,
    ) -> OrdersRes:
        """
        Updates an existing order in the database with the provided order data.

        :param order_uuid: The UUID of the order to be updated.
        :type order_uuid: UUID4
        :param order_data: The data to update the existing order.
        :type order_data: OrdersUpdate
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The updated order data.
        :rtype: OrdersRes
        :raises OrderNotExist: If the order could not be updated or found.
        """
        statement = self._statements.update_order(
            order_uuid=order_uuid, order_data=order_data
        )
        order: OrdersRes = await self._db_ops.return_one_row(
            service=cnst.ORDERS_UPDATE_SERVICE, statement=statement, db=db
        )
        return record_not_exist(instance=order, exception=OrderNotExist)


class DelSrvc:
    """
    Service for soft-deleting orders in the database.

    This class provides a method to soft-delete an existing order, which involves marking
    the order as deleted without actually removing it from the database.

    :param statements: The SQL statements used for order-related queries.
    :type statements: OrdersStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(self, statements: OrdersStms, db_operations: Operations) -> None:
        """
        Initializes the DelSrvc class with the provided SQL statements and database operations.

        :param statements: The SQL statements used for order-related queries.
        :type statements: OrdersStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: OrdersStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> OrdersStms:
        """
        Returns the instance of OrdersStms.

        :returns: The SQL statements handler for orders.
        :rtype: OrdersStms
        """
        return self._statements

    @property
    def db_operations(self) -> Operations:
        """
        Returns the instance of Operations.

        :returns: The database operations handler.
        :rtype: Operations
        """
        return self._db_ops

    async def soft_del_order(
        self,
        order_uuid: UUID4,
        order_data: OrdersDel,
        db: AsyncSession,
    ) -> OrdersDelRes:
        """
        Soft-deletes an existing order by updating its status in the database.

        This method marks the order as deleted by updating the order data with the
        provided `order_data`. It does not permanently delete the record but rather
        flags it for deletion.

        :param order_uuid: The UUID of the order to be soft-deleted.
        :type order_uuid: UUID4
        :param order_data: The data to mark the order as deleted.
        :type order_data: OrdersDel
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The updated order data after soft deletion.
        :rtype: OrdersDelRes
        :raises OrderNotExist: If the order could not be found or soft-deleted.
        """
        statement = self._statements.update_order(
            order_uuid=order_uuid, order_data=order_data
        )
        order: OrdersDelRes = await self._db_ops.return_one_row(
            service=cnst.ORDERS_DEL_SERVICE, statement=statement, db=db
        )
        return record_not_exist(instance=order, exception=OrderNotExist)
