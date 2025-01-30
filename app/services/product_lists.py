from typing import List

from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ..constants import constants as cnst
from ..database.operations import Operations
from ..exceptions import ProductListExists, ProductListNotExist
from ..models.product_lists import ProductLists
from ..schemas.product_lists import (
    ProductListsCreate,
    ProductListsDel,
    ProductListsDelRes,
    ProductListsPgRes,
    ProductListsRes,
    ProductListsUpdate,
)
from ..statements.product_lists import ProductListsStms
from ..utilities import pagination
from ..utilities.data import record_exists, record_not_exist


class ReadSrvc:
    """
    Service for reading and retrieving product list data from the database.

    This class provides methods to fetch product lists by various criteria, including single product list UUID, multiple UUIDs, and paginated results.

    :param statements: The SQL statements used for product list-related queries.
    :type statements: ProductListsStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(self, statements: ProductListsStms, db_operations: Operations) -> None:
        """
        Initializes the ReadSrvc class with the provided SQL statements and database operations.

        :param statements: The SQL statements used for product list-related queries.
        :type statements: ProductListsStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: ProductListsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> ProductListsStms:
        """
        Returns the instance of ProductListsStms.

        :returns: The SQL statements handler for product lists.
        :rtype: ProductListsStms
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

    async def get_product_list(
        self, product_list_uuid: UUID4, db: AsyncSession
    ) -> ProductListsRes:
        """
        Retrieves a single product list by its UUID.

        :param product_list_uuid: The UUID of the product list to retrieve.
        :type product_list_uuid: UUID4
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The requested product list.
        :rtype: ProductListsRes
        :raises ProductListNotExist: If the product list does not exist.
        """
        statement = self._statements.get_product_list(
            product_list_uuid=product_list_uuid
        )
        product_list: ProductListsRes = await self._db_ops.return_one_row(
            service=cnst.PRODUCT_LISTS_READ_SERV, statement=statement, db=db
        )
        return record_not_exist(instance=product_list, exception=ProductListNotExist)

    async def get_product_lists_by_uuids(
        self, product_list_uuids: List[UUID4], db: AsyncSession
    ) -> List[ProductListsRes]:
        """
        Retrieves multiple product lists by their UUIDs.

        :param product_list_uuids: The list of UUIDs for the product lists to retrieve.
        :type product_list_uuids: List[UUID4]
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: A list of product lists corresponding to the provided UUIDs.
        :rtype: List[ProductListsRes]
        :raises ProductListNotExist: If no product lists are found.
        """
        statement = self._statements.sel_prod_lists_by_uuids(
            product_list_uuids=product_list_uuids
        )
        product_lists: List[ProductListsRes] = await self._db_ops.return_all_rows(
            service=cnst.PRODUCT_LISTS_READ_SERV, statement=statement, db=db
        )
        return record_not_exist(instance=product_lists, exception=ProductListNotExist)

    async def get_product_lists(
        self, limit: int, offset: int, db: AsyncSession
    ) -> List[ProductListsRes]:
        """
        Retrieves product lists with pagination using a limit and offset.

        :param limit: The number of product lists to retrieve.
        :type limit: int
        :param offset: The offset to use for pagination.
        :type offset: int
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: A list of product lists based on the provided pagination parameters.
        :rtype: List[ProductListsRes]
        :raises ProductListNotExist: If no product lists are found.
        """
        statement = self._statements.sel_prod_lists(limit=limit, offset=offset)
        product_lists = await self._db_ops.return_all_rows(
            service=cnst.PRODUCT_LISTS_READ_SERV, statement=statement, db=db
        )
        return record_not_exist(instance=product_lists, exception=ProductListNotExist)

    async def get_product_lists_ct(self, db: AsyncSession):
        """
        Retrieves the total count of product lists in the database.

        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The total count of product lists.
        :rtype: int
        :raises ProductListNotExist: If no product lists exist.
        """
        statement = self._statements.get_product_lists_count()
        product_lists: List[ProductListsRes] = await self._db_ops.return_count(
            service=cnst.PRODUCT_LISTS_READ_SERV, statement=statement, db=db
        )

        return record_not_exist(instance=product_lists, exception=ProductListNotExist)

    async def paginated_product_lists(
        self, page: int, limit: int, db: AsyncSession
    ) -> ProductListsPgRes:
        """
        Retrieves paginated product lists along with metadata like total count and whether there are more items.

        :param page: The page number to retrieve.
        :type page: int
        :param limit: The number of product lists to retrieve per page.
        :type limit: int
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: A paginated response containing the product lists and metadata.
        :rtype: ProductListsPgRes
        """
        total_count = await self.get_product_lists_ct(db=db)
        offset = pagination.page_offset(page=page, limit=limit)
        has_more = pagination.has_more_items(
            total_count=total_count, page=page, limit=limit
        )
        product_lists = await self.get_product_lists(offset=offset, limit=limit, db=db)
        return ProductListsPgRes(
            total=total_count,
            page=page,
            limit=limit,
            has_more=has_more,
            product_lists=product_lists,
        )


class CreateSrvc:
    """
    Service for creating and adding new product lists to the database.

    This class provides functionality to check for the existence of a product list by name
    and then create a new product list if it doesn't already exist.

    :param statements: The SQL statements used for product list-related queries.
    :type statements: ProductListsStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    :param model: The model used for product list data.
    :type model: ProductLists
    """

    def __init__(
        self,
        statements: ProductListsStms,
        db_operations: Operations,
        model: ProductLists,
    ) -> None:
        """
        Initializes the CreateSrvc class with the provided SQL statements, database operations, and model.

        :param statements: The SQL statements used for product list-related queries.
        :type statements: ProductListsStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        :param model: The model used for product list data.
        :type model: ProductLists
        """
        self._statements: ProductListsStms = statements
        self._db_ops: Operations = db_operations
        self._model: ProductLists = model

    @property
    def statements(self) -> ProductListsStms:
        """
        Returns the instance of ProductListsStms.

        :returns: The SQL statements handler for product lists.
        :rtype: ProductListsStms
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
    def model(self) -> ProductLists:
        """
        Returns the model instance for product lists.

        :returns: The model used for product list data.
        :rtype: ProductLists
        """
        return self._model

    async def create_product_list(
        self,
        product_list_data: ProductListsCreate,
        db: AsyncSession,
    ) -> ProductListsRes:
        """
        Creates a new product list in the database.

        This method first checks if a product list with the same name already exists.
        If it does, it raises a `ProductListExists` exception. If it does not exist,
        it proceeds to create the new product list.

        :param product_list_data: The data required to create a new product list.
        :type product_list_data: ProductListsCreate
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The newly created product list.
        :rtype: ProductListsRes
        :raises ProductListExists: If a product list with the same name already exists.
        :raises ProductListNotExist: If the product list was not created successfully.
        """
        product_lists = self._model

        # Check if the product list already exists by name
        statement = self._statements.get_product_list_by_name(
            product_list_name=product_list_data.name
        )
        product_list_exists = await self._db_ops.return_one_row(
            service=cnst.PRODUCT_LISTS_CREATE_SERV, statement=statement, db=db
        )
        record_exists(instance=product_list_exists, exception=ProductListExists)

        # Create the new product list
        product_list: ProductListsRes = await self._db_ops.add_instance(
            service=cnst.PRODUCT_LISTS_CREATE_SERV,
            model=product_lists,
            data=product_list_data,
            db=db,
        )
        return record_not_exist(instance=product_list, exception=ProductListNotExist)


class UpdateSrvc:
    """
    Service for updating existing product lists in the database.

    This class provides functionality to update the details of a product list
    identified by its unique identifier (UUID).

    :param statements: The SQL statements used for product list-related queries.
    :type statements: ProductListsStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(self, statements: ProductListsStms, db_operations: Operations) -> None:
        """
        Initializes the UpdateSrvc class with the provided SQL statements and database operations.

        :param statements: The SQL statements used for product list-related queries.
        :type statements: ProductListsStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: ProductListsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> ProductListsStms:
        """
        Returns the instance of ProductListsStms.

        :returns: The SQL statements handler for product lists.
        :rtype: ProductListsStms
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

    async def update_product_list(
        self,
        product_list_uuid: UUID4,
        product_list_data: ProductListsUpdate,
        db: AsyncSession,
    ) -> ProductListsRes:
        """
        Updates the product list in the database.

        This method takes a product list UUID and the new data for the product list,
        and updates the corresponding record in the database. If the product list does not exist,
        it raises a `ProductListNotExist` exception.

        :param product_list_uuid: The UUID of the product list to update.
        :type product_list_uuid: UUID4
        :param product_list_data: The updated data for the product list.
        :type product_list_data: ProductListsUpdate
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The updated product list data.
        :rtype: ProductListsRes
        :raises ProductListNotExist: If the product list does not exist in the database.
        """
        # Prepare the SQL statement to update the product list
        statement = self._statements.update_product_list(
            product_list_uuid=product_list_uuid, product_list_data=product_list_data
        )

        # Execute the query to update the product list
        product_list: ProductListsRes = await self._db_ops.return_one_row(
            service=cnst.PRODUCT_LISTS_UPDATE_SERV, statement=statement, db=db
        )

        # Return the updated product list, raising an exception if it doesn't exist
        return record_not_exist(instance=product_list, exception=ProductListNotExist)


class DelSrvc:
    """
    Service for performing soft deletion of product lists in the database.

    This class handles the logic for marking a product list as deleted in the database
    by updating its relevant status or properties, without physically removing the record.

    :param statements: The SQL statements used for product list-related queries.
    :type statements: ProductListsStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(self, statements: ProductListsStms, db_operations: Operations) -> None:
        """
        Initializes the DelSrvc class with the provided SQL statements and database operations.

        :param statements: The SQL statements used for product list-related queries.
        :type statements: ProductListsStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: ProductListsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> ProductListsStms:
        """
        Returns the instance of ProductListsStms.

        :returns: The SQL statements handler for product lists.
        :rtype: ProductListsStms
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

    async def soft_del_product_list(
        self,
        product_list_uuid: UUID4,
        product_list_data: ProductListsDel,
        db: AsyncSession,
    ) -> ProductListsDelRes:
        """
        Soft deletes a product list by updating its status or relevant data in the database.

        This method marks a product list as deleted in the database, based on the provided
        product list UUID and data, without physically removing the record. If the product list
        does not exist, it raises a `ProductListNotExist` exception.

        :param product_list_uuid: The UUID of the product list to be soft-deleted.
        :type product_list_uuid: UUID4
        :param product_list_data: The data representing the product list to be soft-deleted.
        :type product_list_data: ProductListsDel
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The updated product list data after soft deletion.
        :rtype: ProductListsDelRes
        :raises ProductListNotExist: If the product list does not exist in the database.
        """
        # Prepare the SQL statement to soft-delete the product list
        statement = self._statements.update_product_list(
            product_list_uuid=product_list_uuid, product_list_data=product_list_data
        )

        # Execute the query to soft-delete the product list
        product_list: ProductListsDelRes = await self._db_ops.return_one_row(
            service=cnst.PRODUCT_LISTS_DEL_SERV, statement=statement, db=db
        )

        # Return the updated product list, raising an exception if it doesn't exist
        return record_not_exist(instance=product_list, exception=ProductListNotExist)
