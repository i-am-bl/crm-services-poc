from typing import List

from pydantic import UUID4
from sqlalchemy import Select, Update, and_, func, update

from ..models.product_lists import ProductLists
from ..utilities.data import set_empty_strs_null


class ProductListsStms:
    def __init__(self, model: ProductLists):
        self._model: ProductLists = model

    def model(self) -> ProductLists:
        return self._model

    def get_product_list(self, product_list_uuid: UUID4):
        product_lists = self._model
        return Select(product_lists).where(
            product_lists.uuid == product_list_uuid,
            product_lists.sys_deleted_at == None,
        )

    def get_product_list_by_name(self, product_list_name: str):
        product_lists = self._model
        return Select(product_lists).where(
            and_(
                product_lists.name == product_list_name,
                product_lists.sys_deleted_at == None,
            )
        )

    def sel_prod_lists(self, limit: int, offset: int):
        product_lists = self._model
        return (
            Select(product_lists)
            .where(product_lists.sys_deleted_at == None)
            .offset(offset=offset)
            .limit(limit=limit)
        )

    def sel_prod_lists_by_uuids(self, product_list_uuids: List[UUID4]):
        product_lists = self._model
        return Select(product_lists).where(
            and_(
                product_lists.uuid.in_(product_list_uuids),
                product_lists.sys_deleted_at == None,
            )
        )

    def get_product_lists_count(self):
        product_lists = self._model
        return (
            Select(func.count())
            .select_from(product_lists)
            .where(product_lists.sys_deleted_at == None)
        )

    def update_product_list(
        self, product_list_uuid: UUID4, product_list_data: object
    ) -> Update:
        product_lists = self._model
        return (
            Update(product_lists)
            .where(
                and_(
                    product_lists.uuid == product_list_uuid,
                    product_lists.sys_deleted_at == None,
                )
            )
            .values(set_empty_strs_null(values=product_list_data))
            .returning(product_lists)
        )
