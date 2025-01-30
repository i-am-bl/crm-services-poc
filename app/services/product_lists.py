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
    def __init__(self, statements: ProductListsStms, db_operations: Operations) -> None:
        self._statements: ProductListsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> ProductListsStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def get_product_list(
        self, product_list_uuid: UUID4, db: AsyncSession
    ) -> ProductListsRes:

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

        statement = self._statements.sel_prod_lists(limit=limit, offset=offset)
        product_lists = await self._db_ops.return_all_rows(
            service=cnst.PRODUCT_LISTS_READ_SERV, statement=statement, db=db
        )
        return record_not_exist(instance=product_lists, exception=ProductListNotExist)

    async def get_product_lists_ct(self, db: AsyncSession):

        statement = self._statements.get_product_lists_count()
        product_lists: List[ProductListsRes] = await self._db_ops.return_count(
            service=cnst.PRODUCT_LISTS_READ_SERV, statement=statement, db=db
        )

        return record_not_exist(instance=product_lists, exception=ProductListNotExist)

    async def paginated_product_lists(
        self, page: int, limit: int, db: AsyncSession
    ) -> ProductListsPgRes:
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
    def __init__(
        self,
        statements: ProductListsStms,
        db_operations: Operations,
        model: ProductLists,
    ) -> None:
        self._statements: ProductListsStms = statements
        self._db_ops: Operations = db_operations
        self._model: ProductLists = model

    @property
    def statements(self) -> ProductListsStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    @property
    def model(self) -> ProductLists:
        return self._model

    async def create_product_list(
        self,
        product_list_data: ProductListsCreate,
        db: AsyncSession,
    ) -> ProductListsRes:
        product_lists = self._model

        statement = self._statements.get_product_list_by_name(
            product_list_name=product_list_data.name
        )
        product_list_exists = await self._db_ops.return_one_row(
            service=cnst.PRODUCT_LISTS_CREATE_SERV, statement=statement, db=db
        )
        record_exists(instance=product_list_exists, exception=ProductListExists)

        product_list: ProductListsRes = await self._db_ops.add_instance(
            service=cnst.PRODUCT_LISTS_CREATE_SERV,
            model=product_lists,
            data=product_list_data,
            db=db,
        )
        return record_not_exist(instance=product_list, exception=ProductListNotExist)


class UpdateSrvc:
    def __init__(self, statements: ProductListsStms, db_operations: Operations) -> None:
        self._statements: ProductListsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> ProductListsStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def update_product_list(
        self,
        product_list_uuid: UUID4,
        product_list_data: ProductListsUpdate,
        db: AsyncSession,
    ) -> ProductListsRes:
        statement = self._statements.update_product_list(
            product_list_uuid=product_list_uuid, product_list_data=product_list_data
        )
        product_list: ProductListsRes = await self._db_ops.return_one_row(
            service=cnst.PRODUCT_LISTS_UPDATE_SERV, statement=statement, db=db
        )
        return record_not_exist(instance=product_list, exception=ProductListNotExist)


class DelSrvc:
    def __init__(self, statements: ProductListsStms, db_operations: Operations) -> None:
        self._statements: ProductListsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> ProductListsStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def soft_del_product_list(
        self,
        product_list_uuid: UUID4,
        product_list_data: ProductListsDel,
        db: AsyncSession,
    ) -> ProductListsDelRes:
        statement = self._statements.update_product_list(
            product_list_uuid=product_list_uuid, product_list_data=product_list_data
        )
        product_list: ProductListsDelRes = await self._db_ops.return_one_row(
            service=cnst.PRODUCT_LISTS_DEL_SERV, statement=statement, db=db
        )
        return record_not_exist(instance=product_list, exception=ProductListNotExist)
