from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import UUID4

from ..schemas.account_lists import AccountListsOrchPgRes
from ..services import account_lists as account_lists_srvcs
from ..services import product_lists as product_lists_srvcs
from ..utilities import pagination


class AccountListsReadOrch:
    """
    This class orchestrates the interaction between the account lists and product lists services.
    It handles the retrieval of paginated account lists and their corresponding product lists.

    :param account_lists_read_srvc: Service responsible for reading account lists.
    :type account_lists_read_srvc: account_lists_srvcs.ReadSrvc
    :param product_lists_read_srvc: Service responsible for reading product lists.
    :type product_lists_read_srvc: product_lists_srvcs.ReadSrvc

    :ivar account_lists_read_srvc: The account lists read service instance.
    :vartype account_lists_read_srvc: account_lists_srvcs.ReadSrvc
    :ivar product_lists_read_srvc: The product lists read service instance.
    :vartype product_lists_read_srvc: product_lists_srvcs.ReadSrvc
    """

    def __init__(
        self,
        account_lists_read_srvc: account_lists_srvcs.ReadSrvc,
        product_lists_read_srvc: product_lists_srvcs.ReadSrvc,
    ):
        """
        Initializes the AccountListsReadOrch instance with the provided account lists and product lists services.

        :param account_lists_read_srvc: Service responsible for reading account lists.
        :type account_lists_read_srvc: account_lists_srvcs.ReadSrvc
        :param product_lists_read_srvc: Service responsible for reading product lists.
        :type product_lists_read_srvc: product_lists_srvcs.ReadSrvc
        """
        self._account_lists_read_srvc: account_lists_srvcs.ReadSrvc = (
            account_lists_read_srvc
        )
        self._product_lists_read_srvc: product_lists_srvcs.ReadSrvc = (
            product_lists_read_srvc
        )

    @property
    def account_lists_read_srvc(self) -> account_lists_srvcs.ReadSrvc:
        """
        Returns the account lists read service instance.

        :return: The account lists read service instance.
        :rtype: account_lists_srvcs.ReadSrvc
        """
        return self._account_lists_read_srvc

    @property
    def product_lists_read_srvc(self) -> product_lists_srvcs.ReadSrvc:
        """
        Returns the product lists read service instance.

        :return: The product lists read service instance.
        :rtype: product_lists_srvcs.ReadSrvc
        """
        return self._product_lists_read_srvc

    async def paginated_product_lists(
        self, account_uuid: UUID4, page: int, limit: int, db: AsyncSession
    ) -> AccountListsOrchPgRes:
        """
        Retrieves paginated account lists along with the corresponding product lists for a given account UUID.

        This method calculates the total count of account lists, computes the offset, and checks if there
        are more items available for the next page. It then fetches the account lists and product lists based
        on the pagination parameters.

        :param account_uuid: The UUID of the account to filter the account lists by.
        :type account_uuid: UUID4
        :param page: The page number for pagination.
        :type page: int
        :param limit: The number of items per page.
        :type limit: int
        :param db: The database session for performing queries.
        :type db: AsyncSession

        :return: A paginated result containing the product lists.
        :rtype: AccountListsOrchPgRes
        """
        total_count = await self._account_lists_read_srvc.get_account_list_ct(
            account_uuid=account_uuid, db=db
        )
        offset = pagination.page_offset(page=page, limit=limit)
        has_more = pagination.has_more_items(
            total_count=total_count, page=page, limit=limit
        )
        account_lists = await self._account_lists_read_srvc.get_account_lists(
            account_uuid=account_uuid, offset=offset, limit=limit, db=db
        )
        product_list_uuids = [account_list.uuid for account_list in account_lists]
        product_lists = await self._product_lists_read_srvc.get_product_lists_by_uuids(
            product_list_uuids=product_list_uuids, db=db
        )
        if not isinstance(product_lists, list):
            product_lists = [product_lists]

        return AccountListsOrchPgRes(
            total=total_count,
            page=page,
            limit=limit,
            has_more=has_more,
            data=product_lists,
        )
