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
    def __init__(
        self, statements: ProductListItemsStms, db_operations: Operations
    ) -> None:
        self._statements: ProductListItemsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> ProductListItemsStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def get_product_list_item(
        self,
        product_list_uuid: UUID4,
        product_list_item_uuid: UUID4,
        db: AsyncSession,
    ) -> ProductListItemsRes:
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
        statement = self._statements.get_product_list_items_ct(
            product_list_uuid=product_list_uuid
        )
        return await self._db_ops.return_count(
            service=cnst.PRODUCT_LIST_ITEMS_READ_SERV, statement=statement, db=db
        )

    async def paginated_product_list_items(
        self, product_list_uuid: UUID4, page: int, limit: int, db: AsyncSession
    ) -> ProductListItemsPgRes:
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
    def __init__(
        self,
        statements: ProductListItemsStms,
        db_operations: Operations,
        model: ProductListItems,
    ) -> None:
        self._statements: ProductListItemsStms = statements
        self._db_ops: Operations = db_operations
        self._model: ProductListItems = model

    @property
    def statements(self) -> ProductListItemsStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    @property
    def model(self) -> ProductListItems:
        return self._model

    async def create_product_list_items(
        self,
        product_list_uuid: UUID4,
        product_list_item_data: List[ProductListItemsCreate],
        db: AsyncSession,
    ) -> List[ProductListItemsRes]:
        product_list_items = self._model

        list_data = [*product_list_item_data]
        product_uuid_list = [dict.product_uuid for dict in list_data]

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
        product_list_items: List[ProductListItemsRes] = (
            await self._db_ops.add_instances(
                service=cnst.PRODUCT_LIST_ITEMS_CREATE_SERV,
                model=product_list_items,
                data=product_list_item_data,
                db=db,
            )
        )
        return record_not_exist(
            instance=product_list_items, exception=ProductListItemNotExist
        )


class UpdateSrvc:
    def __init__(
        self, statements: ProductListItemsStms, db_operations: Operations
    ) -> None:
        self._statements: ProductListItemsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> ProductListItemsStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def update_product_list_item(
        self,
        product_list_uuid: UUID4,
        product_list_item_uuid: UUID4,
        product_list_item_data: ProductListItemsUpdate,
        db: AsyncSession,
    ) -> ProductListItemsRes:
        statement = self._statements.update_product_list_item(
            product_list_uuid=product_list_uuid,
            product_list_item_uuid=product_list_item_uuid,
            product_list_item_data=product_list_item_data,
        )
        product_list_item: ProductListItemsRes = await self._db_ops.return_one_row(
            service=cnst.PRODUCT_LIST_ITEMS_UPDATE_SERV, statement=statement, db=db
        )
        return record_not_exist(
            instance=product_list_item, exception=ProductListItemNotExist
        )


class DelSrvc:
    def __init__(
        self, statements: ProductListItemsStms, db_operations: Operations
    ) -> None:
        self._statements: ProductListItemsStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> ProductListItemsStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def soft_del_product_list_item(
        self,
        product_list_uuid: UUID4,
        product_list_item_uuid: UUID4,
        product_list_item_data: ProductListItemsDel,
        db: AsyncSession,
    ) -> ProductListItemsDelRes:
        statement = self._statements.update_product_list_item(
            product_list_uuid=product_list_uuid,
            product_list_item_uuid=product_list_item_uuid,
            product_list_item_data=product_list_item_data,
        )
        product_list_item: ProductListItemsDelRes = await self._db_ops.return_one_row(
            service=cnst.PRODUCT_LIST_ITEMS_UPDATE_SERV, statement=statement, db=db
        )
        return record_not_exist(
            instance=product_list_item, exception=ProductListItemNotExist
        )
