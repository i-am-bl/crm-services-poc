from typing import List

from pydantic import UUID4
from sqlalchemy import Select, Update, and_, func, update

from ..models.product_lists import ProductLists
from ..utilities.data import set_empty_strs_null


class ProductListsStms:
    """
    A class responsible for constructing SQLAlchemy queries and statements for managing product lists.

    ivars:
    ivar: _model: ProductLists: An instance of the ProductLists model.
    """

    def __init__(self, model: ProductLists) -> None:
        """
        Initializes the ProductListsStms class.

        :param model: ProductLists: An instance of the ProductLists model.
        :return: None
        """
        self._model: ProductLists = model

    def model(self) -> ProductLists:
        """
        Returns the instance of the ProductLists model.

        :return: ProductLists: The ProductLists model instance.
        """
        return self._model

    def get_product_list(self, product_list_uuid: UUID4):
        """
        Selects a product list by its UUID.

        :param product_list_uuid: UUID4: The UUID of the product list.
        :return: Select: A Select statement for the specific product list.
        """
        product_lists = self._model
        return Select(product_lists).where(
            product_lists.uuid == product_list_uuid,
            product_lists.sys_deleted_at == None,
        )

    def get_product_list_by_name(self, product_list_name: str):
        """
        Selects a product list by its name.

        :param product_list_name: str: The name of the product list.
        :return: Select: A Select statement for the specific product list by name.
        """
        product_lists = self._model
        return Select(product_lists).where(
            and_(
                product_lists.name == product_list_name,
                product_lists.sys_deleted_at == None,
            )
        )

    def get_product_lists(self, limit: int, offset: int):
        """
        Selects product lists with pagination support.

        :param limit: int: The maximum number of product lists to return.
        :param offset: int: The number of product lists to skip.
        :return: Select: A Select statement for product lists with pagination.
        """
        product_lists = self._model
        return (
            Select(product_lists)
            .where(product_lists.sys_deleted_at == None)
            .offset(offset=offset)
            .limit(limit=limit)
        )

    def get_product_lists_by_uuids(self, product_list_uuids: List[UUID4]):
        """
        Selects product lists by a list of product list UUIDs.

        :param product_list_uuids: List[UUID4]: A list of product list UUIDs.
        :return: Select: A Select statement for product lists with matching UUIDs.
        """
        product_lists = self._model
        return Select(product_lists).where(
            and_(
                product_lists.uuid.in_(product_list_uuids),
                product_lists.sys_deleted_at == None,
            )
        )

    def get_product_lists_count(self):
        """
        Selects the count of all product lists.

        :return: Select: A Select statement for the count of all product lists.
        """
        product_lists = self._model
        return (
            Select(func.count())
            .select_from(product_lists)
            .where(product_lists.sys_deleted_at == None)
        )

    def update_product_list(
        self, product_list_uuid: UUID4, product_list_data: object
    ) -> Update:
        """
        Updates a product list by its UUID.

        :param product_list_uuid: UUID4: The UUID of the product list.
        :param product_list_data: object: The data to update the product list with.
        :return: Update: An Update statement for the product list.
        """
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
