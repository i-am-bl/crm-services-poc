from pydantic import UUID4
from sqlalchemy import Select, Update, and_, func, update
from ..models.account_products import AccountProducts

from ..utilities.data import set_empty_strs_null


class AccountProductsStms:
    def __init__(self, model: AccountProducts) -> None:
        self._model: AccountProducts = model

    @property
    def model(self) -> AccountProducts:
        return self._model

    def get_accout_product(
        self, account_uuid: UUID4, account_product_uuid: UUID4
    ) -> Select:
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
