from turtle import mode
from typing import List, Optional

from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ..constants import constants as cnst
from ..database.operations import Operations
from ..exceptions import ProductsExists, ProductsNotExist
from ..models.products import Products
from ..schemas.products import (
    ProductsInternalCreate,
    ProductsDel,
    ProductsDelRes,
    ProductsPgRes,
    ProductsRes,
    ProductsInternalUpdate,
)
from ..statements.products import ProductsStms
from ..utilities import pagination
from ..utilities.data import record_not_exist, record_exists


class ReadSrvc:
    """
    Service for reading and retrieving product data from the database.

    This class handles operations for fetching product information from the database,
    including single product retrieval, multiple products retrieval, and paginated results.

    :param statements: The SQL statements used for product-related queries.
    :type statements: ProductsStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(self, statements: ProductsStms, db_operations: Operations) -> None:
        """
        Initializes the ReadSrvc class with the provided SQL statements and database operations.

        :param statements: The SQL statements used for product-related queries.
        :type statements: ProductsStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: ProductsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> ProductsStms:
        """
        Returns the instance of ProductsStms.

        :returns: The SQL statements handler for products.
        :rtype: ProductsStms
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

    async def get_product(self, product_uuid: UUID4, db: AsyncSession):
        """
        Retrieves a product from the database based on its UUID.

        If the product does not exist, it raises a `ProductsNotExist` exception.

        :param product_uuid: The UUID of the product to retrieve.
        :type product_uuid: UUID4
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The retrieved product data.
        :rtype: ProductsRes
        :raises ProductsNotExist: If the product does not exist in the database.
        """
        statement = self._statements.get_product(product_uuid=product_uuid)
        product = await self._db_ops.return_one_row(
            service=cnst.PRODUCTS_READ_SERV, statement=statement, db=db
        )
        return record_not_exist(instance=product, exception=ProductsNotExist)

    async def get_products(self, limit: int, offset: int, db: AsyncSession):
        """
        Retrieves a list of products with pagination (limit and offset).

        If no products are found, it raises a `ProductsNotExist` exception.

        :param limit: The maximum number of products to retrieve.
        :type limit: int
        :param offset: The offset from which to start retrieving products.
        :type offset: int
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: A list of retrieved products.
        :rtype: List[ProductsRes]
        :raises ProductsNotExist: If no products are found.
        """
        statement = self._statements.get_products(limit=limit, offset=offset)
        products = await self._db_ops.return_all_rows(
            service=cnst.PRODUCTS_READ_SERV, statement=statement, db=db
        )
        return record_not_exist(instance=products, exception=ProductsNotExist)

    async def get_product_by_uuids(
        self, product_uuids: List[UUID4], db: AsyncSession
    ) -> List[ProductsRes]:
        """
        Retrieves a list of products based on their UUIDs.

        If no products are found, it raises a `ProductsNotExist` exception.

        :param product_uuids: A list of UUIDs of the products to retrieve.
        :type product_uuids: List[UUID4]
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: A list of retrieved products.
        :rtype: List[ProductsRes]
        :raises ProductsNotExist: If no products are found.
        """
        statement = self._statements.get_products_by_uuids(product_uuids=product_uuids)
        products = await self._db_ops.return_all_rows(
            service=cnst.PRODUCTS_READ_SERV, statement=statement, db=db
        )
        return record_not_exist(instance=products, exception=ProductsNotExist)

    async def get_products_ct(self, db: AsyncSession):
        """
        Retrieves the total count of products in the database.

        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The total count of products in the database.
        :rtype: int
        """
        statement = self._statements.get_product_count()
        return await self._db_ops.return_count(
            service=cnst.PRODUCTS_READ_SERV, statement=statement, db=db
        )

    async def paginated_products(
        self, page: int, limit: int, db: AsyncSession
    ) -> ProductsPgRes:
        """
        Retrieves a paginated list of products along with the total count and pagination status.

        :param page: The page number to retrieve.
        :type page: int
        :param limit: The maximum number of products per page.
        :type limit: int
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: A paginated response containing total count, current page, and product list.
        :rtype: ProductsPgRes
        """
        total_count = await self.get_products_ct(db=db)
        offset = pagination.page_offset(page=page, limit=limit)
        has_more = pagination.has_more_items(
            total_count=total_count, page=page, limit=limit
        )
        products = await self.get_products(limit=limit, offset=offset, db=db)
        return ProductsPgRes(
            total=total_count,
            page=page,
            limit=limit,
            has_more=has_more,
            products=products,
        )


class CreateSrvc:
    """
    Service for creating new product entries in the database.

    This class handles operations for adding new products, with validation to ensure
    products with the same name do not exist before creation, and supports both
    transactional and non-transactional product creation processes.

    :param statements: The SQL statements used for product-related queries.
    :type statements: ProductsStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    :param model: The Products model used for creating product entries in the database.
    :type model: Products
    """

    def __init__(
        self, statements: ProductsStms, db_operations: Operations, model: Products
    ) -> None:
        """
        Initializes the CreateSrvc class with the provided SQL statements, database operations,
        and model.

        :param statements: The SQL statements used for product-related queries.
        :type statements: ProductsStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        :param model: The Products model used for creating product entries in the database.
        :type model: Products
        """
        self._statements: ProductsStms = statements
        self._db_ops: Operations = db_operations
        self._model: Products = model

    @property
    def statements(self) -> ProductsStms:
        """
        Returns the instance of ProductsStms.

        :returns: The SQL statements handler for products.
        :rtype: ProductsStms
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
    def model(self) -> Products:
        """
        Returns the instance of Products model.

        :returns: The Products model used for product-related database operations.
        :rtype: Products
        """
        return self._model

    async def create_product(
        self,
        product_data: ProductsInternalCreate,
        db: AsyncSession,
        transaction_type: Optional[bool] = True,
    ) -> ProductsRes:
        """
        Creates a new product entry in the database.

        If `transaction_type` is set to `True`, it first checks whether a product with
        the same name already exists in the database. If such a product exists, it raises
        a `ProductsExists` exception. If no such product exists, it creates the new product.
        If `transaction_type` is `False`, the product is created directly without checking
        for duplicates.

        :param product_data: The data used to create the new product.
        :type product_data: ProductsInternalCreate
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession
        :param transaction_type: A flag indicating whether to check for existing products
            before creating. Defaults to `True`.
        :type transaction_type: Optional[bool], default=True

        :returns: The created product data.
        :rtype: ProductsRes
        :raises ProductsExists: If the product already exists in the database (when `transaction_type=True`).
        :raises ProductsNotExist: If the product could not be created.
        """
        products = self._model

        # If transaction_type is True, check if product already exists
        if transaction_type:
            statement = self._statements.get_products_by_name(
                product_name=product_data.name
            )
            product_exists = await self._db_ops.return_one_row(
                service=cnst.PRODUCTS_CREATE_SERV, statement=statement, db=db
            )
            record_exists(instance=product_exists, exception=ProductsExists)

            # Create the new product
            product = await self._db_ops.add_instance(
                service=cnst.PRODUCTS_CREATE_SERV,
                model=products,
                data=product_data,
                db=db,
            )
            return product

        # If transaction_type is False, create the product directly
        product: ProductsRes = await self._db_ops.add_instance(
            service=cnst.PRODUCTS_CREATE_SERV,
            model=products,
            data=product_data,
            db=db,
        )
        return record_not_exist(instance=product, exception=ProductsNotExist)


class UpdateSrvc:
    """
    Service for updating existing product entries in the database.

    This class provides functionality to update product data based on a given product UUID.
    It ensures that the product being updated exists in the database before performing any updates.

    :param statements: The SQL statements used for product-related queries.
    :type statements: ProductsStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(self, statements: ProductsStms, db_operations: Operations) -> None:
        """
        Initializes the UpdateSrvc class with the provided SQL statements and database operations.

        :param statements: The SQL statements used for product-related queries.
        :type statements: ProductsStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: ProductsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> ProductsStms:
        """
        Returns the instance of ProductsStms.

        :returns: The SQL statements handler for products.
        :rtype: ProductsStms
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

    async def update_product(
        self,
        product_uuid: UUID4,
        product_data: ProductsInternalUpdate,
        db: AsyncSession,
    ) -> ProductsRes:
        """
        Updates an existing product's information in the database based on the provided UUID.

        This method checks whether the product exists in the database and performs the update if
        the product is found. If the product does not exist, it raises a `ProductsNotExist` exception.

        :param product_uuid: The UUID of the product to update.
        :type product_uuid: UUID4
        :param product_data: The data used to update the product.
        :type product_data: ProductsInternalUpdate
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The updated product data.
        :rtype: ProductsRes
        :raises ProductsNotExist: If the product with the given UUID does not exist.
        """
        statement = self._statements.update_product(
            product_uuid=product_uuid, product_data=product_data
        )
        product: ProductsRes = await self._db_ops.return_one_row(
            service=cnst.PRODUCTS_UPDATE_SERV, statement=statement, db=db
        )
        return record_not_exist(instance=product, exception=ProductsNotExist)


class DelSrvc:
    """
    Service for handling the deletion of product entries in the database.

    This class provides functionality for soft-deleting a product from the database, updating its
    status rather than physically removing the record.

    :param statements: The SQL statements used for product-related queries.
    :type statements: ProductsStms
    :param db_operations: The database operations object used for executing queries.
    :type db_operations: Operations
    """

    def __init__(self, statements: ProductsStms, db_operations: Operations) -> None:
        """
        Initializes the DelSrvc class with the provided SQL statements and database operations.

        :param statements: The SQL statements used for product-related queries.
        :type statements: ProductsStms
        :param db_operations: The database operations object used for executing queries.
        :type db_operations: Operations
        """
        self._statements: ProductsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> ProductsStms:
        """
        Returns the instance of ProductsStms.

        :returns: The SQL statements handler for products.
        :rtype: ProductsStms
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

    async def soft_del_product(
        self,
        product_uuid: UUID4,
        product_data: ProductsDel,
        db: AsyncSession,
    ) -> ProductsDelRes:
        """
        Soft-deletes a product from the database by updating its status based on the provided UUID.

        This method updates the product's status to indicate deletion (without removing it from the database).
        If the product does not exist, it raises a `ProductsNotExist` exception.

        :param product_uuid: The UUID of the product to soft-delete.
        :type product_uuid: UUID4
        :param product_data: The data used to update the product's status.
        :type product_data: ProductsDel
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession

        :returns: The result of the soft-deletion operation.
        :rtype: ProductsDelRes
        :raises ProductsNotExist: If the product with the given UUID does not exist.
        """
        statement = self._statements.update_product(
            product_uuid=product_uuid, product_data=product_data
        )
        product: ProductsDelRes = await self._db_ops.return_one_row(
            service=cnst.PRODUCTS_DEL_SERV, statement=statement, db=db
        )
        return record_not_exist(instance=product, exception=ProductsNotExist)
