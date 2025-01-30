from typing import List

from pydantic import UUID4
from sqlalchemy import Select, Update, and_, func, update

from ..models import ProductListItems
from ..utilities.data import set_empty_strs_null


class ProductListItemsStms:
    def __init__(self, model: ProductListItems) -> None:
        self._model: ProductListItems = model

    @property
    def model(self) -> ProductListItems:
        return self._model

    def get_product_list_item(
        self, product_list_uuid: UUID4, product_list_item_uuid: UUID4
    ) -> Select:
        product_list_items = self._model
        return Select(product_list_items).where(
            and_(
                product_list_items.product_list_uuid == product_list_uuid,
                product_list_items.uuid == product_list_item_uuid,
                product_list_items.sys_deleted_at == None,
            )
        )

    def get_product_list_items(
        self, product_list_uuid: UUID4, limit: int, offset: int
    ) -> Select:
        product_list_items = self._model
        return (
            Select(product_list_items)
            .where(
                and_(
                    product_list_items.product_list_uuid == product_list_uuid,
                    product_list_items.sys_deleted_at == None,
                )
            )
            .offset(offset=offset)
            .limit(limit=limit)
        )

    def get_product_list_items_ct(self, product_list_uuid: UUID4) -> Select:
        product_list_items = self._model
        return (
            Select(func.count())
            .select_from(product_list_items)
            .where(
                and_(
                    product_list_items.product_list_uuid == product_list_uuid,
                    product_list_items.sys_deleted_at == None,
                )
            )
        )

    def get_product_list_items(
        self, product_list_uuid: UUID4, product_uuid_list: List[UUID4]
    ) -> Select:
        product_list_items = self._model
        return Select(product_list_items).where(
            and_(
                product_list_items.product_list_uuid == product_list_uuid,
                product_list_items.product_uuid.in_(product_uuid_list),
                product_list_items.sys_deleted_at == None,
            ),
        )

    def update_product_list_item(
        self,
        product_list_uuid: UUID4,
        product_list_item_uuid: UUID4,
        product_list_item_data: object,
    ) -> Update:
        product_list_items = self._model
        return (
            update(product_list_items)
            .where(
                and_(
                    product_list_items.product_list_uuid == product_list_uuid,
                    product_list_items.uuid == product_list_item_uuid,
                    product_list_items.sys_deleted_at == None,
                )
            )
            .values(set_empty_strs_null(product_list_item_data))
            .returning(product_list_items)
        )
