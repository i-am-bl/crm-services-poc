from typing import List

from pydantic import UUID4
from sqlalchemy import Select, Update, and_, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..constants import constants as cnst
from ..database.operations import Operations
from ..exceptions import ProductListItemExists, ProductListItemNotExist
from ..models import ProductListItems
from ..schemas.product_list_items import (
    ProductListItemsCreate,
    ProductListItemsDel,
    ProductListItemsDelRes,
    ProductListItemsPgRes,
    ProductListItemsRes,
    ProductListItemsUpdate,
)
from ..statements.product_list_items import ProductListItemsStms
from ..utilities import pagination
from ..utilities.data import record_not_exist, record_exists


class ReadSrvc:
    """
    Service for reading product list items from the database.

    This class provides methods to retrieve product list items, including paginated results
    and a method to fetch a single product list item.

    :param statements: The SQL statements used for product list item-related queries.
    :type statements: ProductListItemsStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(
        self, statements: ProductListItemsStms, db_operations: Operations
    ) -> None:
        """
        Initializes the ReadSrvc class with the provided SQL statements and database operations.

        :param statements: The SQL statements used for product list item-related queries.
        :type statements: ProductListItemsStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: ProductListItemsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> ProductListItemsStms:
        """
        Returns the instance of ProductListItemsStms.

        :returns: The SQL statements handler for product list items.
        :rtype: ProductListItemsStms
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

    async def get_product_list_item(
        self,
        product_list_uuid: UUID4,
        product_list_item_uuid: UUID4,
        db: AsyncSession,
    ) -> ProductListItemsRes:
        """
        Fetches a single product list item by its UUID.

        :param product_list_uuid: The UUID of the product list to which the item belongs.
        :type product_list_uuid: UUID4
        :param product_list_item_uuid: The UUID of the product list item to fetch.
        :type product_list_item_uuid: UUID4
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The product list item data.
        :rtype: ProductListItemsRes
        :raises ProductListItemNotExist: If the product list item does not exist.
        """
        statement = self._statements.get_product_list_item(
            product_list_uuid=product_list_uuid,
            product_list_item_uuid=product_list_item_uuid,
        )
        product_list_item: ProductListItemsRes = await self._db_ops.return_one_row(
            service=cnst.PRODUCT_LIST_ITEMS_READ_SERV, statement=statement, db=db
        )
        return record_not_exist(
            instance=product_list_item, exception=ProductListItemNotExist
        )

    async def get_product_list_items(
        self,
        product_list_uuid: UUID4,
        limit: int,
        offset: int,
        db: AsyncSession,
    ) -> List[ProductListItemsRes]:
        """
        Fetches a list of product list items with pagination support.

        :param product_list_uuid: The UUID of the product list to fetch items from.
        :type product_list_uuid: UUID4
        :param limit: The maximum number of items to return.
        :type limit: int
        :param offset: The offset from which to start fetching items.
        :type offset: int
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: A list of product list items.
        :rtype: List[ProductListItemsRes]
        :raises ProductListItemNotExist: If no product list items exist.
        """
        statement = self._statements.get_product_list_items(
            product_list_uuid=product_list_uuid, limit=limit, offset=offset
        )
        product_list_items: List[ProductListItemsRes] = (
            await self._db_ops.return_all_rows(
                service=cnst.PRODUCT_LIST_ITEMS_READ_SERV, statement=statement, db=db
            )
        )
        return record_not_exist(
            instance=product_list_items, exception=ProductListItemNotExist
        )

    async def get_product_list_items_ct(
        self,
        product_list_uuid: UUID4,
        db: AsyncSession,
    ) -> int:
        """
        Gets the total count of product list items for a given product list.

        :param product_list_uuid: The UUID of the product list to count items for.
        :type product_list_uuid: UUID4
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The total count of product list items.
        :rtype: int
        """
        statement = self._statements.get_product_list_items_ct(
            product_list_uuid=product_list_uuid
        )
        return await self._db_ops.return_count(
            service=cnst.PRODUCT_LIST_ITEMS_READ_SERV, statement=statement, db=db
        )

    async def paginated_product_list_items(
        self, product_list_uuid: UUID4, page: int, limit: int, db: AsyncSession
    ) -> ProductListItemsPgRes:
        """
        Fetches paginated product list items, including metadata such as total count and whether
        there are more items to fetch.

        :param product_list_uuid: The UUID of the product list to fetch items from.
        :type product_list_uuid: UUID4
        :param page: The page number to fetch.
        :type page: int
        :param limit: The number of items per page.
        :type limit: int
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: A paginated response containing the total count, page number, and product list items.
        :rtype: ProductListItemsPgRes
        """
        total_count = await self.get_product_list_items_ct(
            product_list_uuid=product_list_uuid, db=db
        )
        offset = pagination.page_offset(page=page, limit=limit)
        has_more = pagination.has_more_items(
            total_count=total_count, page=page, limit=limit
        )
        product_list_items = await self.get_product_list_items(
            product_list_uuid=product_list_uuid, offset=offset, limit=limit, db=db
        )

        return ProductListItemsPgRes(
            total=total_count,
            page=page,
            limit=limit,
            has_more=has_more,
            product_list_items=product_list_items,
        )


class CreateSrvc:
    """
    Service for creating product list items in the database.

    This class provides a method for creating multiple product list items in a product list.

    :param statements: The SQL statements used for product list item-related queries.
    :type statements: ProductListItemsStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    :param model: The model representing the product list items.
    :type model: ProductListItems
    """

    def __init__(
        self,
        statements: ProductListItemsStms,
        db_operations: Operations,
        model: ProductListItems,
    ) -> None:
        """
        Initializes the CreateSrvc class with the provided SQL statements, database operations,
        and model for product list items.

        :param statements: The SQL statements used for product list item-related queries.
        :type statements: ProductListItemsStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        :param model: The model representing the product list items.
        :type model: ProductListItems
        """
        self._statements: ProductListItemsStms = statements
        self._db_ops: Operations = db_operations
        self._model: ProductListItems = model

    @property
    def statements(self) -> ProductListItemsStms:
        """
        Returns the instance of ProductListItemsStms.

        :returns: The SQL statements handler for product list items.
        :rtype: ProductListItemsStms
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
    def model(self) -> ProductListItems:
        """
        Returns the instance of ProductListItems model.

        :returns: The model for product list items.
        :rtype: ProductListItems
        """
        return self._model

    async def create_product_list_items(
        self,
        product_list_uuid: UUID4,
        product_list_item_data: List[ProductListItemsCreate],
        db: AsyncSession,
    ) -> List[ProductListItemsRes]:
        """
        Creates multiple product list items in a specified product list.

        :param product_list_uuid: The UUID of the product list to add items to.
        :type product_list_uuid: UUID4
        :param product_list_item_data: A list of data for the product list items to create.
        :type product_list_item_data: List[ProductListItemsCreate]
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: A list of created product list items.
        :rtype: List[ProductListItemsRes]
        :raises ProductListItemExists: If the product list item already exists in the product list.
        :raises ProductListItemNotExist: If the product list items do not exist after creation.
        """
        product_list_items = self._model

        # Prepare the data for checking if items already exist
        list_data = [*product_list_item_data]
        product_uuid_list = [dict.product_uuid for dict in list_data]

        # Check if the product list item already exists
        statement = self._statements.get_product_list_items(
            product_list_uuid=product_list_uuid,
            product_uuid_list=product_uuid_list,
        )
        product_list_item_exists: ProductListItemsRes = (
            await self._db_ops.return_one_row(
                service=cnst.PRODUCT_LIST_ITEMS_CREATE_SERV,
                statement=statement,
                db=db,
            )
        )
        record_exists(
            instance=product_list_item_exists, exception=ProductListItemExists
        )

        # Add the new product list items to the database
        product_list_items: List[ProductListItemsRes] = (
            await self._db_ops.add_instances(
                service=cnst.PRODUCT_LIST_ITEMS_CREATE_SERV,
                model=product_list_items,
                data=product_list_item_data,
                db=db,
            )
        )

        # Ensure that records exist after the creation attempt
        return record_not_exist(
            instance=product_list_items, exception=ProductListItemNotExist
        )


class UpdateSrvc:
    """
    Service for updating a product list item in the database.

    This class provides a method to update a product list item in a specified product list.

    :param statements: The SQL statements used for product list item-related queries.
    :type statements: ProductListItemsStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(
        self, statements: ProductListItemsStms, db_operations: Operations
    ) -> None:
        """
        Initializes the UpdateSrvc class with the provided SQL statements and database operations.

        :param statements: The SQL statements used for product list item-related queries.
        :type statements: ProductListItemsStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: ProductListItemsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> ProductListItemsStms:
        """
        Returns the instance of ProductListItemsStms.

        :returns: The SQL statements handler for product list items.
        :rtype: ProductListItemsStms
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

    async def update_product_list_item(
        self,
        product_list_uuid: UUID4,
        product_list_item_uuid: UUID4,
        product_list_item_data: ProductListItemsUpdate,
        db: AsyncSession,
    ) -> ProductListItemsRes:
        """
        Updates a product list item in the specified product list.

        :param product_list_uuid: The UUID of the product list where the item belongs.
        :type product_list_uuid: UUID4
        :param product_list_item_uuid: The UUID of the product list item to update.
        :type product_list_item_uuid: UUID4
        :param product_list_item_data: The new data for the product list item.
        :type product_list_item_data: ProductListItemsUpdate
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The updated product list item.
        :rtype: ProductListItemsRes
        :raises ProductListItemNotExist: If the product list item does not exist.
        """
        # Create the update statement
        statement = self._statements.update_product_list_item(
            product_list_uuid=product_list_uuid,
            product_list_item_uuid=product_list_item_uuid,
            product_list_item_data=product_list_item_data,
        )

        # Execute the statement and return the updated product list item
        product_list_item: ProductListItemsRes = await self._db_ops.return_one_row(
            service=cnst.PRODUCT_LIST_ITEMS_UPDATE_SERV, statement=statement, db=db
        )

        # Ensure that the product list item exists after the update
        return record_not_exist(
            instance=product_list_item, exception=ProductListItemNotExist
        )


class DelSrvc:
    """
    Service for performing soft deletion of a product list item in the database.

    This class provides a method to perform a soft delete on a product list item by updating its status or related attributes in the database.

    :param statements: The SQL statements used for product list item-related queries.
    :type statements: ProductListItemsStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(
        self, statements: ProductListItemsStms, db_operations: Operations
    ) -> None:
        """
        Initializes the DelSrvc class with the provided SQL statements and database operations.

        :param statements: The SQL statements used for product list item-related queries.
        :type statements: ProductListItemsStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: ProductListItemsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> ProductListItemsStms:
        """
        Returns the instance of ProductListItemsStms.

        :returns: The SQL statements handler for product list items.
        :rtype: ProductListItemsStms
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

    async def soft_del_product_list_item(
        self,
        product_list_uuid: UUID4,
        product_list_item_uuid: UUID4,
        product_list_item_data: ProductListItemsDel,
        db: AsyncSession,
    ) -> ProductListItemsDelRes:
        """
        Soft deletes a product list item in the specified product list by updating its status or related attributes.

        :param product_list_uuid: The UUID of the product list containing the item to be deleted.
        :type product_list_uuid: UUID4
        :param product_list_item_uuid: The UUID of the product list item to be soft deleted.
        :type product_list_item_uuid: UUID4
        :param product_list_item_data: The data used for soft deleting the product list item, such as status changes.
        :type product_list_item_data: ProductListItemsDel
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The result of the soft deletion operation, including the updated product list item data.
        :rtype: ProductListItemsDelRes
        :raises ProductListItemNotExist: If the product list item does not exist after the soft delete attempt.
        """
        # Create the soft delete update statement
        statement = self._statements.update_product_list_item(
            product_list_uuid=product_list_uuid,
            product_list_item_uuid=product_list_item_uuid,
            product_list_item_data=product_list_item_data,
        )

        # Execute the statement and return the updated product list item after the soft delete
        product_list_item: ProductListItemsDelRes = await self._db_ops.return_one_row(
            service=cnst.PRODUCT_LIST_ITEMS_UPDATE_SERV, statement=statement, db=db
        )

        # Ensure that the product list item exists after the soft delete
        return record_not_exist(
            instance=product_list_item, exception=ProductListItemNotExist
        )
