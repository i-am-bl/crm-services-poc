from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import UUID4

from ..schemas.account_lists import AccountListsOrchPgRes
from ..services import account_lists as account_lists_srvcs
from ..services import product_lists as product_lists_srvcs
from ..utilities import pagination


class AccountListsReadOrch:
    def __init__(
        self,
        account_lists_read_srvc: account_lists_srvcs.ReadSrvc,
        product_lists_read_srvc: product_lists_srvcs.ReadSrvc,
    ):
        self._account_lists_read_srvc: account_lists_srvcs.ReadSrvc = (
            account_lists_read_srvc
        )
        self._product_lists_read_srvc: product_lists_srvcs.ReadSrvc = (
            product_lists_read_srvc
        )

    @property
    def account_lists_read_srvc(self) -> account_lists_srvcs.ReadSrvc:
        return self._account_lists_read_srvc

    @property
    def product_lists_read_srvc(self) -> product_lists_srvcs.ReadSrvc:
        return self._product_lists_read_srvc

    async def paginated_product_lists(
        self, account_uuid: UUID4, page: int, limit: int, db: AsyncSession
    ) -> AccountListsOrchPgRes:
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
