from typing import List
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ..constants import constants as cnst
from ..database.operations import Operations
from ..exceptions import WebsitesExists, WebsitesNotExist
from ..models.websites import Websites
from ..schemas.websites import (
    WebsiteDelRes,
    WebsitesCreate,
    WebsitesPgRes,
    WebsitesRes,
    WebsitesDel,
    WebsitesUpdate,
)
from ..statements.websites import WebsitesStms
from ..utilities import pagination
from ..utilities.data import record_exists, record_not_exist


class ReadSrvc:
    def __init__(self, statements: WebsitesStms, db_operations: Operations) -> None:
        self._statements: WebsitesStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> WebsitesStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def get_website(
        self,
        entity_uuid: UUID4,
        website_uuid: UUID4,
        db: AsyncSession,
    ) -> WebsitesRes:

        statement = self._statements.get_website(
            entity_uuid=entity_uuid, website_uuid=website_uuid
        )
        website: WebsitesRes = await self._db_ops.return_one_row(
            service=cnst.WEBSITES_READ_SERVICE, statement=statement, db=db
        )
        return record_not_exist(instance=website, exception=WebsitesNotExist)

    async def get_websites(
        self,
        entity_uuid: UUID4,
        offset: int,
        limit: int,
        db: AsyncSession,
    ) -> List[WebsitesRes]:

        statement = self._statements.get_websites(
            entity_uuid=entity_uuid, offset=offset, limit=limit
        )
        websites: List[WebsitesRes] = await self._db_ops.return_all_rows(
            service=cnst.WEBSITES_READ_SERVICE, statement=statement, db=db
        )
        return record_not_exist(instance=websites, exception=WebsitesNotExist)

    async def get_websites_ct(
        self,
        entity_uuid: UUID4,
        db: AsyncSession,
    ) -> int:

        statement = self._statements.get_websites_ct(entity_uuid=entity_uuid)
        return await self._db_ops.return_count(
            service=cnst.WEBSITES_READ_SERVICE, statement=statement, db=db
        )

    async def paginated_websites(
        self, entity_uuid: UUID4, page: int, limit: int, db: AsyncSession
    ) -> WebsitesPgRes:
        total_count = self.get_websites_ct(db=db)
        offset = pagination.page_offset(page=page, limit=limit)
        has_more = pagination.has_more_items(
            total_count=total_count, page=page, limit=limit
        )
        websites = await self.get_websites(
            entity_uuid=entity_uuid, offset=offset, limit=limit, db=db
        )
        return WebsitesPgRes(
            total=total_count,
            page=page,
            has_more=has_more,
            limit=limit,
            websites=websites,
        )


class CreateSrvc:
    def __init__(
        self, statements: WebsitesStms, db_operations: Operations, model: Websites
    ) -> None:
        self._statements: WebsitesStms = statements
        self._db_ops: Operations = db_operations
        self._model: Websites = model

    @property
    def statements(self) -> WebsitesStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    @property
    def model(self) -> Websites:
        return self._model

    async def create_website(
        self,
        website_data: WebsitesCreate,
        db: AsyncSession,
    ) -> WebsitesRes:

        statement = self._statements.get_website_by_url(
            entity_uuid=website_data.entity_uuid, website_name=website_data.url
        )
        websites = self._model
        website_exists = await self._db_ops.return_one_row(
            service=cnst.WEBSITES_CREATE_SERVICE, statement=statement, db=db
        )
        record_exists(instance=website_exists, exception=WebsitesExists)
        website: WebsitesRes = await self._db_ops.add_instance(
            service=cnst.WEBSITES_CREATE_SERVICE,
            model=websites,
            data=website_data,
            db=db,
        )
        return record_not_exist(instance=website, exception=WebsitesNotExist)


class UpdateSrvc:
    def __init__(self, statements: WebsitesStms, db_operations: Operations) -> None:
        self._statements: WebsitesStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> WebsitesStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def update_website(
        self,
        entity_uuid: UUID4,
        website_uuid: UUID4,
        website_data: WebsitesUpdate,
        db: AsyncSession,
    ) -> WebsitesRes:

        statement = self._statements.update_website(
            entity_uuid=entity_uuid,
            website_uuid=website_uuid,
            website_data=website_data,
        )
        website: WebsitesRes = await self._db_ops.return_one_row(
            service=cnst.WEBSITES_UPDATE_SERVICE, statement=statement, db=db
        )
        return record_not_exist(instance=website, exception=WebsitesNotExist)


class DelSrvc:
    def __init__(self, statements: WebsitesStms, db_operations: Operations) -> None:
        self._statements: WebsitesStms = statements
        self._db_ops: Operations = db_operations

    @property
    def statements(self) -> WebsitesStms:
        return self._statements

    @property
    def db_operations(self) -> Operations:
        return self._db_ops

    async def soft_del_website(
        self,
        entity_uuid: UUID4,
        website_uuid: UUID4,
        website_data: WebsitesDel,
        db: AsyncSession,
    ) -> WebsiteDelRes:

        statement = self._statements.update_web(
            entity_uuid=entity_uuid,
            website_uuid=website_uuid,
            website_data=website_data,
        )
        website: WebsiteDelRes = await self._db_ops.return_one_row(
            service=cnst.WEBSITES_DEL_SERVICE, statement=statement, db=db
        )
        return record_not_exist(instance=website, exception=WebsitesNotExist)
