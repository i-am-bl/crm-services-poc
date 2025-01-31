from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ..services.account_products import ReadSrvc as AccountProductsReadSrvc
from ..services.products import ReadSrvc as ProductsReadSrvc
from ..schemas.account_products import AccountProductsOrchPgRes
from ..utilities import pagination


class AccountProductsReadOrch:
    """
    Orchestrates the retrieval of paginated account products and their corresponding product data
    by interacting with the account products and product services.

    :param products_read_srvc: Service responsible for reading products data.
    :type products_read_srvc: ProductsReadSrvc
    :param account_products_read_srvc: Service responsible for reading account products data.
    :type account_products_read_srvc: AccountProductsReadSrvc

    :ivar products_read_srvc: The products read service instance.
    :vartype products_read_srvc: ProductsReadSrvc
    :ivar account_products_read_srvc: The account products read service instance.
    :vartype account_products_read_srvc: AccountProductsReadSrvc
    """

    def __init__(
        self,
        products_read_srvc: ProductsReadSrvc,
        account_products_read_srvc: AccountProductsReadSrvc,
    ):
        """
        Initializes the AccountProductsReadOrch instance with the provided product and account products services.

        :param products_read_srvc: Service responsible for reading product data.
        :type products_read_srvc: ProductsReadSrvc
        :param account_products_read_srvc: Service responsible for reading account products data.
        :type account_products_read_srvc: AccountProductsReadSrvc
        """
        self._products_read_srvc: ProductsReadSrvc = products_read_srvc
        self._account_products_read_srvc: AccountProductsReadSrvc = (
            account_products_read_srvc
        )

    @property
    def products_read_srvc(self) -> ProductsReadSrvc:
        """
        Returns the products read service instance.

        :return: The products read service instance.
        :rtype: ProductsReadSrvc
        """
        return self._products_read_srvc

    @property
    def account_products_read_srvc(self) -> AccountProductsReadSrvc:
        """
        Returns the account products read service instance.

        :return: The account products read service instance.
        :rtype: AccountProductsReadSrvc
        """
        return self._account_products_read_srvc

    async def paginated_products(
        self, account_uuid: UUID4, page: int, limit: int, db: AsyncSession
    ) -> AccountProductsOrchPgRes:
        """
        Retrieves paginated account products along with the corresponding product data for a given account UUID.

        This method calculates the total count of account products, computes the offset, and checks if there
        are more items available for the next page. It then fetches the account products and their associated
        product data based on the pagination parameters.

        :param account_uuid: The UUID of the account to filter the account products by.
        :type account_uuid: UUID4
        :param page: The page number for pagination.
        :type page: int
        :param limit: The number of items per page.
        :type limit: int
        :param db: The database session for performing queries.
        :type db: AsyncSession

        :return: A paginated result containing the corresponding product data for account products.
        :rtype: AccountProductsOrchPgRes
        """
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
