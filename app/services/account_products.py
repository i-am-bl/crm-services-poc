from typing import List
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ..statements.accounts_products import AccountProductsStms
from ..constants import constants as cnst
from ..database.operations import Operations
from ..exceptions import AccProductsExists, AccProductstNotExist
from ..models.account_products import AccountProducts
from ..schemas.account_products import (
    AccountProductsCreate,
    AccountProductsDel,
    AccountProductsDelRes,
    AccountProductsPgRes,
    AccountProductsRes,
    AccountProductsUpdate,
)
from ..utilities import pagination
from ..utilities.data import record_not_exist, record_exists


class ReadSrvc:
    """
    Read service class for account products.

    Expects an instance of a database connection to be passed in for each method.

    ivars:
    ivar: _statements: An instance of AccountProductsStms.
    varType: AccountProductsStms
    ivar: _db_ops: A utility class for database operations.
    varType: Operations
    """

    def __init__(
        self, statements: AccountProductsStms, db_operations: Operations
    ) -> None:
        """
        Initializes the ReadService class for account products.

        :param statements: An instance of AccountProductsStms.
        :type statements: AccountProductsStms
        :param db_operations: A utility class for database operations.
        :type db_operations: Operations
        :return: None
        :rtype: None
        """
        self._statements = statements
        self._db_ops = db_operations

    async def get_account_product(
        self,
        account_uuid: UUID4,
        account_product_uuid: UUID4,
        db: AsyncSession,
    ) -> AccountProductsRes:
        """
        Retrieves a specific account product from the database.

        :param account_uuid: The UUID of the account.
        :type account_uuid: UUID4
        :param account_product_uuid: The UUID of the account product.
        :type account_product_uuid: UUID4
        :param db: The database session.
        :type db: AsyncSession
        :return: The requested account product.
        :rtype: AccountProductsRes
        :raises AccProductstNotExist: If the account product does not exist.
        """
        statement = self._statements.get_accout_product(
            account_uuid=account_uuid, account_product_uuid=account_product_uuid
        )
        account_product = await self._db_ops.return_one_row(
            service=cnst.ACCOUNTS_PRODUCTS_READ_SERVICE, statement=statement, db=db
        )
        return record_not_exist(
            instance=account_product, exception=AccProductstNotExist
        )

    async def get_account_products(
        self,
        account_uuid: UUID4,
        limit: int,
        offset: int,
        db: AsyncSession,
    ) -> List[AccountProductsRes]:
        """
        Retrieves a list of account products with pagination.

        :param account_uuid: The UUID of the account.
        :type account_uuid: UUID4
        :param limit: The maximum number of account products to retrieve.
        :type limit: int
        :param offset: The starting point for pagination.
        :type offset: int
        :param db: The database session.
        :type db: AsyncSession
        :return: A list of account products.
        :rtype: List[AccountProductsRes]
        :raises AccProductstNotExist: If no account products exist.
        """
        statement = self._statements.get_account_products(
            account_uuid=account_uuid, limit=limit, offset=offset
        )
        account_products: List[AccountProductsRes] = await self._db_ops.return_all_rows(
            service=cnst.ACCOUNTS_PRODUCTS_READ_SERVICE, statement=statement, db=db
        )
        return record_not_exist(
            instance=account_products, exception=AccProductstNotExist
        )

    async def get_account_product_ct(
        self, account_uuid: UUID4, db: AsyncSession
    ) -> int:
        """
        Retrieves the total count of account products for a specific account.

        :param account_uuid: The UUID of the account.
        :type account_uuid: UUID4
        :param db: The database session.
        :type db: AsyncSession
        :return: The count of account products.
        :rtype: int
        """
        statement = self._statements.get_account_products_ct(account_uuid=account_uuid)
        return await self._db_ops.return_count(
            service=cnst.ACCOUNTS_PRODUCTS_READ_SERVICE, statement=statement, db=db
        )

    async def paginated_products(
        self,
        account_uuid: UUID4,
        page: int,
        limit: int,
        db: AsyncSession,
    ) -> AccountProductsPgRes:
        """
        Retrieves paginated account products for a specific account.

        :param account_uuid: The UUID of the account.
        :type account_uuid: UUID4
        :param page: The current page number.
        :type page: int
        :param limit: The maximum number of products per page.
        :type limit: int
        :param db: The database session.
        :type db: AsyncSession
        :return: A paginated response with account products.
        :rtype: AccountProductsPgRes
        """
        total_count = await self.get_account_product_ct(
            account_uuid=account_uuid, db=db
        )
        offset = pagination.page_offset(page=page, limit=limit)
        has_more = pagination.has_more_items(
            total_count=total_count, page=page, limit=limit
        )
        account_products = await self.get_account_products(
            account_uuid=account_uuid, offset=offset, limit=limit, db=db
        )
        return AccountProductsPgRes(
            total=total_count,
            page=page,
            limit=limit,
            has_more=has_more,
            products=account_products,
        )


class CreateSrvc:
    """
    Service class for creating account products.

    Expects an instance of a database connection to be passed in for each method.

    ivars:
    ivar: _statements: An instance of AccountProductsStms.
    varType: AccountProductsStms
    ivar: _db_ops: A utility class for database operations.
    varType: Operations
    ivar: _model: The AccountProducts model used for interacting with the database.
    varType: AccountProducts
    """

    def __init__(
        self,
        statements: AccountProductsStms,
        db_operations: Operations,
        model: AccountProducts,
    ) -> None:
        """
        Initializes the CreateSrvc class for account products.

        :param statements: An instance of AccountProductsStms.
        :type statements: AccountProductsStms
        :param db_operations: A utility class for database operations.
        :type db_operations: Operations
        :param model: The AccountProducts model used for interacting with the database.
        :type model: AccountProducts
        :return: None
        :rtype: None
        """
        self._statements = statements
        self._db_ops = db_operations
        self._model = model

    async def create_account_product(
        self,
        account_uuid: UUID4,
        account_product_data: AccountProductsCreate,
        db: AsyncSession,
    ) -> AccountProductsRes:
        """
        Creates a new account product in the database.

        :param account_uuid: The UUID of the account.
        :type account_uuid: UUID4
        :param account_product_data: The data for the new account product.
        :type account_product_data: AccountProductsCreate
        :param db: The database session.
        :type db: AsyncSession
        :return: The newly created account product.
        :rtype: AccountProductsRes
        :raises AccProductsExists: If the account product already exists.
        :raises AccProductstNotExist: If the account product could not be created.
        """
        accont_products = self._model
        statement = self._statements.validate_account_product(
            account_uuid=account_uuid,
            product_uuid=account_product_data.product_uuid,
        )
        account_product_exists: AccountProductsRes = await self._db_ops.return_one_row(
            service=cnst.ACCOUNTS_PRODUCTS_CREATE_SERVICE,
            statement=statement,
            db=db,
        )
        record_exists(instance=account_product_exists, exception=AccProductsExists)
        account_product: AccountProductsRes = await self._db_ops.add_instance(
            service=cnst.ACCOUNTS_PRODUCTS_CREATE_SERVICE,
            model=accont_products,
            data=account_product_data,
            db=db,
        )
        return record_not_exist(
            instance=account_product, exception=AccProductstNotExist
        )


class UpdateSrvc:
    """
    Service class for updating account products.

    Expects an instance of a database connection to be passed in for each method.

    ivars:
    ivar: _statements: An instance of AccountProductsStms.
    varType: AccountProductsStms
    ivar: _db_ops: A utility class for database operations.
    varType: Operations
    """

    def __init__(
        self,
        statements: AccountProductsStms,
        db_operations: Operations,
    ) -> None:
        """
        Initializes the UpdateSrvc class for updating account products.

        :param statements: An instance of AccountProductsStms.
        :type statements: AccountProductsStms
        :param db_operations: A utility class for database operations.
        :type db_operations: Operations
        :return: None
        :rtype: None
        """
        self._statements = statements
        self._db_ops = db_operations

    async def update_account_product(
        self,
        account_uuid: UUID4,
        account_product_uuid: UUID4,
        account_product_data: AccountProductsUpdate,
        db: AsyncSession,
    ) -> AccountProductsRes:
        """
        Updates an existing account product in the database.

        :param account_uuid: The UUID of the account.
        :type account_uuid: UUID4
        :param account_product_uuid: The UUID of the account product.
        :type account_product_uuid: UUID4
        :param account_product_data: The updated data for the account product.
        :type account_product_data: AccountProductsUpdate
        :param db: The database session.
        :type db: AsyncSession
        :return: The updated account product.
        :rtype: AccountProductsRes
        :raises AccProductstNotExist: If the account product to be updated does not exist.
        """
        statement = self._statements.update_account_product(
            account_uuid=account_uuid,
            account_product_uuid=account_product_uuid,
            account_product_data=account_product_data,
        )
        account_product: AccountProductsRes = await self._db_ops.return_one_row(
            service=cnst.ACCOUNTS_PRODUCTS_UPDATE_SERVICE,
            statement=statement,
            db=db,
        )
        return record_not_exist(
            instance=account_product, exception=AccProductstNotExist
        )


class DelSrvc:
    """
    Service class for handling the soft deletion of account products.

    ivars:
    ivar: _statements: An instance of AccountProductsStms for executing queries.
    varType: AccountProductsStms
    ivar: _db_ops: A utility class for database operations.
    varType: Operations
    """

    def __init__(
        self,
        statements: AccountProductsStms,
        db_operations: Operations,
    ) -> None:
        """
        Initializes the DelSrvc class for performing soft deletions of account products.

        :param statements: An instance of AccountProductsStms for query execution.
        :type statements: AccountProductsStms
        :param db_operations: A utility class for handling database operations.
        :type db_operations: Operations
        :return: None
        :rtype: None
        """
        self._statements = statements
        self._db_ops = db_operations

    async def soft_del_account_product(
        self,
        account_uuid: UUID4,
        account_product_uuid: UUID4,
        account_product_data: AccountProductsDel,
        db: AsyncSession,
    ) -> AccountProductsDelRes:
        """
        Performs a soft deletion of an account product in the database.

        :param account_uuid: The UUID of the account.
        :type account_uuid: UUID4
        :param account_product_uuid: The UUID of the account product.
        :type account_product_uuid: UUID4
        :param account_product_data: The data required to mark the account product as deleted.
        :type account_product_data: AccountProductsDel
        :param db: The database session.
        :type db: AsyncSession
        :return: The result of the soft deletion operation.
        :rtype: AccountProductsDelRes
        :raises AccProductstNotExist: If the account product does not exist to be deleted.
        """
        statement = self._statements.update_account_product(
            account_uuid=account_uuid,
            account_product_uuid=account_product_uuid,
            account_product_data=account_product_data,
        )
        account_product: AccountProductsDelRes = await self._db_ops.return_one_row(
            service=cnst.ACCOUNTS_PRODUCTS_DEL_SERVICE, statement=statement, db=db
        )
        return record_not_exist(
            instance=account_product, exception=AccProductstNotExist
        )
