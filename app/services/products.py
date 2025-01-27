from turtle import mode
from typing import List, Optional

from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ..constants import constants as cnst
from ..database.operations import Operations
from ..exceptions import ProductsExists, ProductsNotExist
from ..models.products import Products
from ..schemas.products import (
    ProductsCreate,
    ProductsDel,
    ProductsDelRes,
    ProductsPgRes,
    ProductsRes,
    ProductsUpdate,
)
from ..statements.products import ProductsStms
from ..utilities import pagination
from ..utilities.utilities import DataUtils as di


class ReadSrvc:
    def __init__(self, statements: ProductsStms, db_operations: Operations) -> None:
        self._statements: ProductsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> ProductsStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def get_product(self, product_uuid: UUID4, db: AsyncSession):
        statement = self._statements.get_product(product_uuid=product_uuid)
        product = await self._db_ops.return_one_row(
            service=cnst.PRODUCTS_READ_SERV, statement=statement, db=db
        )
        return di.record_not_exist(instance=product, exception=ProductsNotExist)

    async def get_products(self, limit: int, offset: int, db: AsyncSession):
        statemenet = self._statements.get_products(limit=limit, offset=offset)
        products = await self._db_ops.return_all_rows(
            service=cnst.PRODUCTS_READ_SERV, statement=statemenet, db=db
        )
        return di.record_not_exist(instance=products, exception=ProductsNotExist)

    async def get_product_by_uuids(
        self, product_uuids: List[UUID4], db: AsyncSession
    ) -> List[ProductsRes]:
        statemenet = self._statements.get_products_by_uuids(product_uuids=product_uuids)
        products: List[ProductsRes] = await self._db_ops.return_all_rows(
            service=cnst.PRODUCTS_READ_SERV, statement=statemenet, db=db
        )
        return di.record_not_exist(instance=products, exception=ProductsNotExist)

    async def get_products_ct(self, db: AsyncSession):
        statemenet = self._statements.get_product_count()
        return await self._db_ops.return_count(
            service=cnst.PRODUCTS_READ_SERV, statement=statemenet, db=db
        )

    async def paginated_products(
        self, page: int, limit: int, db: AsyncSession
    ) -> ProductsPgRes:
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
    def __init__(
        self, statements: ProductsStms, db_operations: Operations, model: Products
    ) -> None:
        self._statements: ProductsStms = statements
        self._db_ops: Operations = db_operations
        self._model: Products = model

    @property
    def statements(self) -> ProductsStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    @property
    def model(self) -> Products:
        return self._model

    async def create_product(
        self,
        product_data: ProductsCreate,
        db: AsyncSession,
        transaction_type: Optional[bool] = True,
    ) -> ProductsRes:
        products = self._model

        if transaction_type:
            statement = self._statements.get_products_by_name(
                product_name=product_data.name
            )
            product_exists = await self._db_ops.return_one_row(
                service=cnst.PRODUCTS_CREATE_SERV, statement=statement, db=db
            )
            di.record_exists(instance=product_exists, exception=ProductsExists)
            product = await self._db_ops.add_instance(
                service=cnst.PRODUCTS_CREATE_SERV,
                model=products,
                data=product_data,
                db=db,
            )
            return product
        # TODO: Review this for additional attention on how we are doing this
        product: ProductsRes = await self._db_ops.add_instance(
            service=cnst.PRODUCTS_CREATE_SERV,
            model=products,
            data=product_data,
            db=db,
        )
        return di.record_not_exist(instance=product, exception=ProductsNotExist)


class UpdateSrvc:
    def __init__(self, statements: ProductsStms, db_operations: Operations) -> None:
        self._statements: ProductsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> ProductsStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def update_product(
        self,
        product_uuid: UUID4,
        product_data: ProductsUpdate,
        db: AsyncSession,
    ) -> ProductsRes:
        statement = self._statements.update_product(
            product_uuid=product_uuid, product_data=product_data
        )
        product: ProductsRes = await self._db_ops.return_one_row(
            service=cnst.PRODUCTS_UPDATE_SERV, statement=statement, db=db
        )
        return di.record_not_exist(instance=product, exception=ProductsNotExist)


class DelSrvc:
    def __init__(self, statements: ProductsStms, db_operations: Operations) -> None:
        self._statements: ProductsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> ProductsStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def soft_del_product(
        self,
        product_uuid: UUID4,
        product_data: ProductsDel,
        db: AsyncSession,
    ) -> ProductsDelRes:
        statement = self._statements.update_product(
            product_uuid=product_uuid, product_data=product_data
        )
        product: ProductsDelRes = await self._db_ops.return_one_row(
            service=cnst.PRODUCTS_DEL_SERV, statement=statement, db=db
        )
        return di.record_not_exist(instance=product, exception=ProductsNotExist)
