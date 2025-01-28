from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ..services.account_products import ReadSrvc as AccountProductsReadSrvc
from ..services.products import ReadSrvc as ProductsReadSrvc
from ..schemas.account_products import AccountProductsOrchPgRes
from ..utilities import pagination


class AccountProductsReadOrch:
    def __init__(
        self,
        products_read_srvc: ProductsReadSrvc,
        account_products_read_srvc: AccountProductsReadSrvc,
    ):
        self._products_read_srvc: ProductsReadSrvc = products_read_srvc
        self._account_products_read_srvc: AccountProductsReadSrvc = (
            account_products_read_srvc
        )

    @property
    def products_read_srvc(self) -> ProductsReadSrvc:
        return self._products_read_srvc

    @property
    def account_products_read_srvc(self):
        return self._account_products_read_srvc

    async def paginated_products(
        self, account_uuid: UUID4, page: int, limit: int, db: AsyncSession
    ) -> AccountProductsOrchPgRes:
        total_count = await self._account_products_read_srvc.get_account_product_ct(
            account_uuid=account_uuid, db=db
        )
        offset = pagination.page_offset(page=page, limit=limit)
        has_more = pagination.has_more_items(
            total_count=total_count, page=page, limit=limit
        )
        account_products = await self._account_products_read_srvc.get_account_products(
            account_uuid=account_uuid, offset=offset, limit=limit, db=db
        )
        product_uuids = [
            account_product.product_uuid for account_product in account_products
        ]
        products = await self._products_read_srvc.get_product_by_uuids(
            product_uuids=product_uuids, db=db
        )
        if not isinstance(products, list):
            products = [products]

        return AccountProductsOrchPgRes(
            total=total_count, page=page, limit=limit, has_more=has_more, data=products
        )
