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
from ..utilities.data import record_not_exist


class ReadSrvc:
    """
    Service for reading order item data related to an order.

    This class provides methods for fetching individual and multiple order items,
    as well as retrieving paginated results and counts for order items.

    :param statements: The SQL statements used for querying order items from the database.
    :type statements: OrderItemsStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(self, statements: OrderItemsStms, db_operations: Operations) -> None:
        """
        Initializes the ReadSrvc class with the provided statements and database operations.

        :param statements: The SQL statements used for querying order items from the database.
        :type statements: OrderItemsStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: OrderItemsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> OrderItemsStms:
        """
        Returns the instance of OrderItemsStms.

        :returns: The SQL statements for querying order items data.
        :rtype: OrderItemsStms
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

    async def get_order_item(
        self,
        order_uuid: UUID4,
        order_item_uuid: UUID4,
        db: AsyncSession,
    ) -> OrderItemsRes:
        """
        Retrieves a single order item based on its UUID within a specific order.

        :param order_uuid: The UUID of the order that contains the order item.
        :type order_uuid: UUID4
        :param order_item_uuid: The UUID of the order item to be fetched.
        :type order_item_uuid: UUID4
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The order item data if found.
        :rtype: OrderItemsRes
        :raises OrderItemNotExist: If the order item doesn't exist.
        """
        statement = self._statements.get_order_item(
            order_uuid=order_uuid, order_item_uuid=order_item_uuid
        )
        order_item: OrderItemsRes = await self._db_ops.return_one_row(
            cnst.ORDERS_ITEMS_READ_SERVICE, statement=statement, db=db
        )
        return record_not_exist(instance=order_item, exception=OrderItemNotExist)

    async def get_order_items(
        self,
        order_uuid: UUID4,
        limit: int,
        offset: int,
        db: AsyncSession,
    ) -> List[OrderItemsRes]:
        """
        Retrieves a list of order items for a specific order, with pagination support.

        :param order_uuid: The UUID of the order for which items are fetched.
        :type order_uuid: UUID4
        :param limit: The maximum number of order items to return.
        :type limit: int
        :param offset: The offset for pagination (e.g., starting point).
        :type offset: int
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: A list of order item data.
        :rtype: List[OrderItemsRes]
        :raises OrderItemNotExist: If no order items are found.
        """
        statement = self._statements.get_order_items(
            order_uuid=order_uuid, limit=limit, offset=offset
        )
        order_items: List[OrderItemsRes] = await self._db_ops.return_all_rows(
            service=cnst.ORDERS_ITEMS_READ_SERVICE, statement=statement, db=db
        )
        return record_not_exist(instance=order_items, exception=OrderItemNotExist)

    async def get_order_items_ct(
        self,
        order_uuid: UUID4,
        db: AsyncSession,
    ) -> int:
        """
        Retrieves the count of order items for a specific order.

        :param order_uuid: The UUID of the order.
        :type order_uuid: UUID4
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The total count of order items in the order.
        :rtype: int
        """
        statement = self._statements.get_order_item_ct(order_uuid=order_uuid)
        return await self._db_ops.return_count(
            service=cnst.ORDERS_ITEMS_READ_SERVICE, statement=statement, db=db
        )

    async def paginated_order_items(
        self, order_uuid: UUID4, page: int, limit: int, db: AsyncSession
    ) -> OrderItemsPgRes:
        """
        Retrieves order items for a specific order in a paginated format.

        This method calculates the offset based on the requested page and limit,
        checks if there are more items, and returns a paginated response.

        :param order_uuid: The UUID of the order.
        :type order_uuid: UUID4
        :param page: The current page number for pagination.
        :type page: int
        :param limit: The number of items to return per page.
        :type limit: int
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: A paginated response containing the order items, total count, and page information.
        :rtype: OrderItemsPgRes
        """
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
    """
    Service for creating new order items in the system.

    This class provides methods for adding new order items to the database.

    :param statements: The SQL statements used for creating order items.
    :type statements: OrderItemsStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    :param model: The model used for creating order items.
    :type model: OrderItems
    """

    def __init__(
        self, statements: OrderItemsStms, db_operations: Operations, model: OrderItems
    ) -> None:
        """
        Initializes the CreateSrvc class with the provided statements, database operations, and model.

        :param statements: The SQL statements used for creating order items.
        :type statements: OrderItemsStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        :param model: The model used for creating order items.
        :type model: OrderItems
        """
        self._statements: OrderItemsStms = statements
        self._db_ops: Operations = db_operations
        self._model: OrderItems = model

    @property
    def statements(self) -> OrderItemsStms:
        """
        Returns the instance of OrderItemsStms.

        :returns: The SQL statements for creating order items.
        :rtype: OrderItemsStms
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

    @property
    def model(self) -> OrderItems:
        """
        Returns the instance of OrderItems model.

        :returns: The model used for creating order items.
        :rtype: OrderItems
        """
        return self._model

    async def create_order_item(
        self,
        order_uuid: UUID4,
        order_item_data: OrderItemsCreate,
        db: AsyncSession,
    ) -> OrderItemsRes:
        """
        Creates a new order item and adds it to the database.

        This method takes the provided order item data and creates a new order item in the database.

        :param order_uuid: The UUID of the order to which the order item belongs.
        :type order_uuid: UUID4
        :param order_item_data: The data for the new order item to be created.
        :type order_item_data: OrderItemsCreate
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The created order item data.
        :rtype: OrderItemsRes
        :raises OrderItemNotExist: If the creation process fails or the item does not exist.
        """
        order_items = self._model
        order_item: OrderItemsRes = await self._db_ops.add_instances(
            service=cnst.ORDERS_ITEMS_CREATE_SERVICE,
            model=order_items,
            data=order_item_data,
            db=db,
        )
        return record_not_exist(instance=order_item, exception=OrderItemNotExist)


class UpdateSrvc:
    """
    Service for updating existing order items in the system.

    This class provides methods for updating details of order items in the database.

    :param statements: The SQL statements used for updating order items.
    :type statements: OrderItemsStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(self, statements: OrderItemsStms, db_operations: Operations) -> None:
        """
        Initializes the UpdateSrvc class with the provided statements and database operations.

        :param statements: The SQL statements used for updating order items.
        :type statements: OrderItemsStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: OrderItemsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> OrderItemsStms:
        """
        Returns the instance of OrderItemsStms.

        :returns: The SQL statements for updating order items.
        :rtype: OrderItemsStms
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

    async def update_order_item(
        self,
        order_uuid: UUID4,
        order_item_uuid: UUID4,
        order_item_data: OrderItemsUpdate,
        db: AsyncSession,
    ) -> OrderItemsRes:
        """
        Updates an existing order item with the provided data.

        This method updates the specified order item in the database based on the provided UUIDs
        and order item data.

        :param order_uuid: The UUID of the order to which the order item belongs.
        :type order_uuid: UUID4
        :param order_item_uuid: The UUID of the specific order item to be updated.
        :type order_item_uuid: UUID4
        :param order_item_data: The updated data for the order item.
        :type order_item_data: OrderItemsUpdate
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The updated order item data.
        :rtype: OrderItemsRes
        :raises OrderItemNotExist: If the order item does not exist or the update fails.
        """
        statement = self._statements.update_order_item(
            order_uuid=order_uuid,
            order_item_uuid=order_item_uuid,
            order_item_data=order_item_data,
        )
        order_item: OrderItemsRes = await self._db_ops.return_one_row(
            service=cnst.ORDERS_ITEMS_UPDATE_SERVICE, statement=statement, db=db
        )
        return record_not_exist(instance=order_item, exception=OrderItemNotExist)


class DelSrvc:
    """
    Service for soft-deleting order items in the system.

    This class provides methods for performing soft deletion of order items,
    which typically involves marking them as deleted without actually removing them from the database.

    :param statements: The SQL statements used for updating order items for soft deletion.
    :type statements: OrderItemsStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(self, statements: OrderItemsStms, db_operations: Operations) -> None:
        """
        Initializes the DelSrvc class with the provided statements and database operations.

        :param statements: The SQL statements used for updating order items for soft deletion.
        :type statements: OrderItemsStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: OrderItemsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> OrderItemsStms:
        """
        Returns the instance of OrderItemsStms.

        :returns: The SQL statements for soft-deleting order items.
        :rtype: OrderItemsStms
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

    async def soft_del_order_item(
        self,
        order_uuid: UUID4,
        order_item_uuid: UUID4,
        order_item_data: OrderItemsDel,
        db: AsyncSession,
    ) -> OrderItemsDelRes:
        """
        Soft deletes an order item by updating its status in the database.

        This method marks the specified order item as deleted without removing it entirely from the database.

        :param order_uuid: The UUID of the order to which the order item belongs.
        :type order_uuid: UUID4
        :param order_item_uuid: The UUID of the specific order item to be soft-deleted.
        :type order_item_uuid: UUID4
        :param order_item_data: The data to be updated for the soft-deletion process.
        :type order_item_data: OrderItemsDel
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The result of the soft deletion operation.
        :rtype: OrderItemsDelRes
        :raises OrderItemNotExist: If the order item does not exist or the deletion fails.
        """
        statement = self._statements.update_order_item(
            order_uuid=order_uuid,
            order_item_uuid=order_item_uuid,
            order_item_data=order_item_data,
        )
        order_item: OrderItemsDelRes = await self._db_ops.return_one_row(
            service=cnst.ORDERS_ITEMS_DEL_SERVICE, statement=statement, db=db
        )
        return record_not_exist(instance=order_item, exception=OrderItemNotExist)
