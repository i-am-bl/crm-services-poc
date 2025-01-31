from pydantic import UUID4
from sqlalchemy import Select, Update, and_, func, update
from ..models.account_products import AccountProducts

from ..utilities.data import set_empty_strs_null


class AccountProductsStms:
    """
    A class responsible for constructing SQLAlchemy queries and statements for managing account products.

    ivars:
    ivar: _model: AccountProducts: An instance of AccountProducts
    """

    def __init__(self, model: AccountProducts) -> None:
        """
        Initializes the AccountProductsStms class.

        :param model: AccountProducts: An instance of AccountProducts.
        :return None
        """
        self._model: AccountProducts = model

    def get_account_product(
        self, account_uuid: UUID4, account_product_uuid: UUID4
    ) -> Select:
        """
        Selects an account product by account_uuid and account_product_uuid.

        :param account_uuid: UUID4: The account_uuid of the account product.
        :param account_product_uuid: UUID4: The account_product_uuid of the account product.
        :return: Select: A Select statement.
        """
        account_products = self._model
        return Select(account_products).where(
            and_(
                account_products.account_uuid == account_uuid,
                account_products.uuid == account_product_uuid,
                account_products.sys_deleted_at == None,
            )
        )

    def validate_account_product(
        self, account_uuid: UUID4, product_uuid: UUID4
    ) -> Select:
        """
        Validates if an account product exists by account_uuid and product_uuid.

        :param account_uuid: UUID4: The account_uuid of the account product.
        :param product_uuid: UUID4: The product_uuid of the account product.
        :return: Select: A Select statement.
        """
        account_products = self._model
        return Select(account_products).where(
            and_(
                account_products.account_uuid == account_uuid,
                account_products.product_uuid == product_uuid,
                account_products.sys_deleted_at == None,
            )
        )

    def get_account_products(
        self, account_uuid: UUID4, limit: int, offset: int
    ) -> Select:
        """
        Selects account products by account_uuid with pagination support.

        :param account_uuid: UUID4: The account_uuid of the account products.
        :param limit: int: The number of records to return.
        :param offset: int: The number of records to skip.
        :return: Select: A Select statement.
        """
        account_products = self._model
        return (
            Select(account_products)
            .where(
                and_(
                    account_products.account_uuid == account_uuid,
                    account_products.sys_deleted_at == None,
                )
            )
            .offset(offset=offset)
            .limit(limit=limit)
        )

    def get_account_products_ct(self, account_uuid: UUID4) -> Select:
        """
        Selects the count of account products by account_uuid.

        :param account_uuid: UUID4: The account_uuid of the account products.
        :return: Select: A Select statement with a count of account products.
        """
        account_products = self._model
        return (
            Select(func.count())
            .select_from(account_products)
            .where(
                and_(
                    account_products.account_uuid == account_uuid,
                    account_products.sys_deleted_at == None,
                )
            )
        )

    def update_account_product(
        self,
        account_uuid: UUID4,
        account_product_uuid: UUID4,
        account_product_data: object,
    ) -> Update:
        """
        Updates an account product by account_uuid and account_product_uuid.

        :param account_uuid: UUID4: The account_uuid of the account product.
        :param account_product_uuid: UUID4: The account_product_uuid of the account product.
        :param account_product_data: object: The data to update the account product with.
        :return: Update: An Update statement.
        """
        account_products = self._model
        return (
            update(account_products)
            .where(
                and_(
                    account_products.account_uuid == account_uuid,
                    account_products.uuid == account_product_uuid,
                    account_products.sys_deleted_at == None,
                )
            )
            .values(set_empty_strs_null(values=account_product_data))
            .returning(account_products)
        )
