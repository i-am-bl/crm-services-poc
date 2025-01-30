from typing import List

from pydantic import UUID4
from sqlalchemy import Select, Update, and_, func, update

from ..models.products import Products
from ..utilities.data import set_empty_strs_null


class ProductsStms:
    def __init__(self, model: Products) -> None:
        self._model: Products = model

    @property
    def model(self) -> Products:
        return self._model

    def get_product(self, product_uuid: UUID4) -> Select:
        products = self._model
        return Select(products).where(
            and_(products.uuid == product_uuid, products.sys_deleted_at == None)
        )

    def get_products_by_name(self, product_name: str) -> Select:
        products = self._model
        return Select(products).where(
            and_(products.name == product_name, products.sys_deleted_at == None)
        )

    def get_products(self, limit: int, offset: int) -> Select:
        products = self._model
        return (
            Select(products)
            .where(products.sys_deleted_at == None)
            .offset(offset=offset)
            .limit(limit=limit)
        )

    def get_products_by_uuids(self, product_uuids: List[UUID4]) -> Select:
        products = self._model
        return Select(products).where(
            and_(products.uuid.in_(product_uuids), products.sys_deleted_at == None)
        )

    def get_product_count(
        self,
    ) -> Select:
        products = self._model
        return (
            Select(func.count())
            .select_from(products)
            .where(products.sys_deleted_at == None)
        )

    def update_product(self, product_uuid: UUID4, product_data: object) -> Update:
        products = self._model
        return (
            update(products)
            .where(and_(products.uuid == product_uuid, products.sys_deleted_at == None))
            .values(set_empty_strs_null(product_data))
            .returning(products)
        )
