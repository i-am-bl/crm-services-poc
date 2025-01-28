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
from ..utilities.utilities import DataUtils as di


class ReadSrvc:
    def __init__(
        self, statements: AccountProductsStms, db_operations: Operations
    ) -> None:
        self._statements: AccountProductsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> AccountProductsStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def get_account_product(
        self,
        account_uuid: UUID4,
        account_product_uuid: UUID4,
        db: AsyncSession,
    ) -> AccountProductsRes:
        statement = self._statements.get_accout_product(
            account_uuid=account_uuid, account_product_uuid=account_product_uuid
        )
        account_product = await self._db_ops.return_one_row(
            service=cnst.ACCOUNTS_PRODUCTS_READ_SERVICE, statement=statement, db=db
        )
        return di.record_not_exist(
            instance=account_product, exception=AccProductstNotExist
        )

    async def get_account_products(
        self,
        account_uuid: UUID4,
        limit: int,
        offset: int,
        db: AsyncSession,
    ) -> List[AccountProductsRes]:
        statement = self._statements.get_account_products(
            account_uuid=account_uuid, limit=limit, offset=offset
        )
        account_products: List[AccountProductsRes] = await self._db_ops.return_all_rows(
            service=cnst.ACCOUNTS_PRODUCTS_READ_SERVICE, statement=statement, db=db
        )
        return di.record_not_exist(
            instance=account_products, exception=AccProductstNotExist
        )

    async def get_account_product_ct(
        self, account_uuid: UUID4, db: AsyncSession
    ) -> int:
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
    def __init__(
        self,
        statements: AccountProductsStms,
        db_operations: Operations,
        model: AccountProducts,
    ) -> None:
        self._statements: AccountProductsStms = statements
        self._db_ops: Operations = db_operations
        self._model: AccountProducts = model

    @property
    def statements(self) -> AccountProductsStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    @property
    def model(self) -> AccountProducts:
        return self._model

    async def create_account_product(
        self,
        account_uuid: UUID4,
        account_product_data: AccountProductsCreate,
        db: AsyncSession,
    ) -> AccountProductsRes:
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
        di.record_exists(instance=account_product_exists, exception=AccProductsExists)
        account_product: AccountProductsRes = await self._db_ops.add_instance(
            service=cnst.ACCOUNTS_PRODUCTS_CREATE_SERVICE,
            model=accont_products,
            data=account_product_data,
            db=db,
        )
        return di.record_not_exist(
            instance=account_product, exception=AccProductstNotExist
        )


class UpdateSrvc:
    def __init__(
        self, statements: AccountProductsStms, db_operations: Operations
    ) -> None:
        self._statements: AccountProductsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> AccountProductsStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def update_account_product(
        self,
        account_uuid: UUID4,
        account_product_uuid: UUID4,
        account_product_data: AccountProductsUpdate,
        db: AsyncSession,
    ) -> AccountProductsRes:
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
        return di.record_not_exist(
            instance=account_product, exception=AccProductstNotExist
        )


class DelSrvc:
    def __init__(
        self, statements: AccountProductsStms, db_operations: Operations
    ) -> None:
        self._statements: AccountProductsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> AccountProductsStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def soft_del_account_product(
        self,
        account_uuid: UUID4,
        account_product_uuid: UUID4,
        account_product_data: AccountProductsDel,
        db: AsyncSession,
    ) -> AccountProductsDelRes:
        statement = self._statements.update_account_product(
            account_uuid=account_uuid,
            account_product_uuid=account_product_uuid,
            account_product_data=account_product_data,
        )
        account_product: AccountProductsDelRes = await self._db_ops.return_one_row(
            service=cnst.ACCOUNTS_PRODUCTS_DEL_SERVICE, statement=statement, db=db
        )
        return di.record_not_exist(
            instance=account_product, exception=AccProductstNotExist
        )
