from typing import List

from pydantic import UUID4
from sqlalchemy import Select, Update, and_, func, update

from ..models.products import Products
from ..utilities.data import set_empty_strs_null


class ProductsStms:
    """
    A class responsible for constructing SQLAlchemy queries and statements for managing products.

    ivars:
    ivar: _model: Products: An instance of the Products model.
    """

    def __init__(self, model: Products) -> None:
        """
        Initializes the ProductsStms class.

        :param model: Products: An instance of the Products model.
        :return: None
        """
        self._model: Products = model

    @property
    def model(self) -> Products:
        """
        Returns the instance of the Products model.

        :return: Products: The Products model instance.
        """
        return self._model

    def get_product(self, product_uuid: UUID4) -> Select:
        """
        Selects a product by its UUID.

        :param product_uuid: UUID4: The UUID of the product.
        :return: Select: A Select statement for the specific product.
        """
        products = self._model
        return Select(products).where(
            and_(products.uuid == product_uuid, products.sys_deleted_at == None)
        )

    def get_products_by_name(self, product_name: str) -> Select:
        """
        Selects products by their name.

        :param product_name: str: The name of the product(s).
        :return: Select: A Select statement for products with the specified name.
        """
        products = self._model
        return Select(products).where(
            and_(products.name == product_name, products.sys_deleted_at == None)
        )

    def get_products(self, limit: int, offset: int) -> Select:
        """
        Selects products with pagination support.

        :param limit: int: The maximum number of products to return.
        :param offset: int: The number of products to skip.
        :return: Select: A Select statement for products with pagination.
        """
        products = self._model
        return (
            Select(products)
            .where(products.sys_deleted_at == None)
            .offset(offset=offset)
            .limit(limit=limit)
        )

    def get_products_by_uuids(self, product_uuids: List[UUID4]) -> Select:
        """
        Selects products by a list of product UUIDs.

        :param product_uuids: List[UUID4]: A list of product UUIDs.
        :return: Select: A Select statement for products with matching UUIDs.
        """
        products = self._model
        return Select(products).where(
            and_(products.uuid.in_(product_uuids), products.sys_deleted_at == None)
        )

    def get_product_count(self) -> Select:
        """
        Selects the count of all products.

        :return: Select: A Select statement for the count of all products.
        """
        products = self._model
        return (
            Select(func.count())
            .select_from(products)
            .where(products.sys_deleted_at == None)
        )

    def update_product(self, product_uuid: UUID4, product_data: object) -> Update:
        """
        Updates a product by its UUID.

        :param product_uuid: UUID4: The UUID of the product.
        :param product_data: object: The data to update the product with.
        :return: Update: An Update statement for the product.
        """
        products = self._model
        return (
            update(products)
            .where(and_(products.uuid == product_uuid, products.sys_deleted_at == None))
            .values(set_empty_strs_null(product_data))
            .returning(products)
        )
