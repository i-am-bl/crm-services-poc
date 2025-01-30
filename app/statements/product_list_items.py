from typing import List

from pydantic import UUID4
from sqlalchemy import Select, Update, and_, func, update

from ..models import ProductListItems
from ..utilities.data import set_empty_strs_null


class ProductListItemsStms:
    """
    A class responsible for constructing SQLAlchemy queries and statements for managing product list items.

    ivars:
    ivar: _model: ProductListItems: An instance of the ProductListItems model.
    """

    def __init__(self, model: ProductListItems) -> None:
        """
        Initializes the ProductListItemsStms class.

        :param model: ProductListItems: An instance of the ProductListItems model.
        :return: None
        """
        self._model: ProductListItems = model

    def get_product_list_item(
        self, product_list_uuid: UUID4, product_list_item_uuid: UUID4
    ) -> Select:
        """
        Selects a specific product list item by its product list UUID and product list item UUID.

        :param product_list_uuid: UUID4: The UUID of the product list.
        :param product_list_item_uuid: UUID4: The UUID of the product list item.
        :return: Select: A Select statement for the specific product list item.
        """
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
        """
        Selects product list items for a given product list UUID with pagination support.

        :param product_list_uuid: UUID4: The UUID of the product list.
        :param limit: int: The maximum number of records to return.
        :param offset: int: The number of records to skip.
        :return: Select: A Select statement for the product list items with pagination.
        """
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
        """
        Selects the count of product list items for a given product list UUID.

        :param product_list_uuid: UUID4: The UUID of the product list.
        :return: Select: A Select statement for the count of product list items.
        """
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

    def get_product_list_items_by_uuids(
        self, product_list_uuid: UUID4, product_uuid_list: List[UUID4]
    ) -> Select:
        """
        Selects product list items by product list UUID and a list of product UUIDs.

        :param product_list_uuid: UUID4: The UUID of the product list.
        :param product_uuid_list: List[UUID4]: A list of product UUIDs.
        :return: Select: A Select statement for the product list items.
        """
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
        """
        Updates a product list item by its product list UUID and product list item UUID.

        :param product_list_uuid: UUID4: The UUID of the product list.
        :param product_list_item_uuid: UUID4: The UUID of the product list item.
        :param product_list_item_data: object: The data to update the product list item with.
        :return: Update: An Update statement for the product list item.
        """
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
